"""Crea galerías: copias web, miniaturas y entradas en galerias.json, leyendo la hoja "Galerías" del Excel.

Uso habitual (todas las galerías de la hoja, una carpeta de fotos por galería con el mismo nombre):
    python crear_galeria.py --excel Un_poco_de_historia_13.xlsx
Otras formas:
    python crear_galeria.py --solo Ciberdromo        solo esa galería de la hoja
    python crear_galeria.py Ciberdromo               carpeta Ciberdromo (el nombre sale de la carpeta)
    python crear_galeria.py CARPETA nombre-galeria   carpeta y nombre explícitos
Dónde busca la carpeta de cada galería (la primera que exista, sin distinguir mayúsculas):
    --fotos RUTA, o bien la carpeta "fotos", la carpeta de este script y la de arriba.
Requiere:  pip install pillow openpyxl
Los originales no se tocan. Las copias web no llevan metadatos (ni GPS).
Prioridad de datos: Excel, luego lo que ya hubiera en galerias.json, luego las opciones de la línea de comandos."""
import argparse, json, re, shutil, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageOps
import openpyxl
EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
VID = {".mp4"}
BASE = Path(__file__).resolve().parent
def anio_exif(im):
    try:
        e = im.getexif(); v = e.get_ifd(0x8769).get(36867) or e.get(306)
        return str(v)[:4] if v and str(v)[:4].isdigit() else ""
    except Exception:
        return ""
def natural(p): return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", p.name)]
def slug(s): return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()).strip("-") or "foto"
def buscar_excel(arg):
    if arg: return Path(arg)
    c = [p for d in (BASE, BASE.parent) for p in d.glob("*.xlsx") if not p.name.startswith("~$")]
    return max(c, key=lambda p: p.stat().st_mtime) if c else None
def leer_hoja(ruta):
    """{slug: {"nombre", "cab", "filas"}} desde la hoja Galerías."""
    gs = {}
    if not ruta or not Path(ruta).exists(): return gs
    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    hoja = next((n for n in wb.sheetnames if n.lower().replace("í", "i") == "galerias"), None)
    if not hoja: return gs
    for r in wb[hoja].iter_rows(min_row=2, values_only=True):
        gal, arch, tit, det, tipo, fecha = [("" if v is None else str(v).strip()) for v in (list(r) + [None] * 6)[:6]]
        if not gal: continue
        g = gs.setdefault(slug(gal), {"nombre": gal, "cab": {}, "filas": {}})
        if not arch: g["cab"] = {"titulo": tit, "descripcion": det}
        else: g["filas"][arch.lower()] = {"titulo": tit, "detalle": det, "tipo": tipo, "fecha": fecha}
    return gs
def buscar_carpeta(nombre, bases):
    for b in bases:
        if b.is_dir():
            for d in sorted(b.iterdir()):
                if d.is_dir() and d.name.lower() not in {"img", ".git"} and slug(d.name) == slug(nombre): return d
    return None

def miniatura_video(p, mini, ancho):
    """Miniatura = primer fotograma (necesita opencv-python). Si ya existe, no se toca: puedes cambiarla a mano."""
    try:
        import cv2
        cap = cv2.VideoCapture(str(p)); ok, fr = cap.read(); cap.release()
        if not ok: raise RuntimeError("no se pudo leer el primer fotograma")
        im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
    except Exception as e:
        print(f"  Aviso: miniatura genérica para {p.name} ({e}). Instala opencv-python para usar el primer fotograma.")
        im = Image.new("RGB", (ancho, ancho * 3 // 4), (40, 40, 40))
    im.thumbnail((ancho, ancho)); im.save(mini, "JPEG", quality=80, optimize=True)

def crear(nombre, carpeta, cab, filas, a, datos):
    fotos = sorted((p for p in carpeta.iterdir() if p.suffix.lower() in EXT | VID), key=natural)
    if not fotos: print(f"Aviso: no hay imágenes ni vídeos en {carpeta}"); return
    clave = lambda p: {p.name.lower(), p.stem.lower()}
    listadas = [p for k in filas for p in fotos if k in clave(p)]
    fotos = list(dict.fromkeys(listadas + fotos))   # manda el orden de la hoja
    destino = BASE / "img" / nombre; destino.mkdir(parents=True, exist_ok=True)
    g = datos.setdefault(nombre, {"titulo": cab.get("nombre", nombre), "descripcion": "", "items": []})
    g["titulo"] = a.titulo or cab.get("titulo") or g["titulo"]
    g["descripcion"] = a.descripcion if a.descripcion is not None else (cab.get("descripcion") or g["descripcion"])
    previos = {it.get("origen"): it for it in g["items"] if it.get("origen")}
    items, validos, usados = [], set(), set()
    for p in fotos:
        nom, n = slug(p.stem), 2
        while nom in usados: nom, n = f"{slug(p.stem)}-{n}", n + 1
        usados.add(nom); video = p.suffix.lower() in VID
        full, mini = destino / f"{nom}{'.mp4' if video else '.jpg'}", destino / f"{nom}-m.jpg"
        validos |= {full.name, mini.name}; exif = ""
        if video:
            mb = p.stat().st_size / 1048576
            if mb > 100: print(f"  Aviso: {p.name} pesa {mb:.0f} MB: GitHub no admite archivos de más de 100 MB. Reduce el vídeo antes de subirlo.")
            elif mb > 50: print(f"  Aviso: {p.name} pesa {mb:.0f} MB: GitHub avisa a partir de 50 MB. Conviene reducirlo.")
            if a.forzar or not full.exists() or full.stat().st_size != p.stat().st_size: shutil.copy2(p, full)
            if a.forzar or not mini.exists(): miniatura_video(p, mini, a.miniatura)
        else:
            with Image.open(p) as im:
                exif = anio_exif(im)
                if a.forzar or not (full.exists() and mini.exists()):
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    im.thumbnail((a.maximo, a.maximo)); im.save(full, "JPEG", quality=85, optimize=True)
                    im.thumbnail((a.miniatura, a.miniatura)); im.save(mini, "JPEG", quality=80, optimize=True)
        prev = previos.get(p.name, {}); fila = filas.get(p.name.lower()) or filas.get(p.stem.lower()) or {}
        items.append({"titulo": fila.get("titulo") or prev.get("titulo") or re.sub(r"[_-]+", " ", p.stem).strip(),
                      "detalle": fila.get("detalle") or prev.get("detalle") or "",
                      "tipo": fila.get("tipo") or prev.get("tipo") or ("Vídeo" if video else a.tipo),
                      "fecha": fila.get("fecha") or prev.get("fecha") or a.fecha or exif,
                      "medio": "video" if video else "imagen", "origen": p.name,
                      "miniatura": f"img/{nombre}/{mini.name}", "imagen": f"img/{nombre}/{full.name}"})
    for viejo in destino.iterdir():
        if viejo.suffix.lower() in {".jpg", ".mp4"} and viejo.name not in validos: viejo.unlink()
    g["items"] = items
    sin_foto = [k for k in filas if not any(k in clave(p) for p in fotos)]
    if sin_foto: print("  Aviso: filas del Excel sin foto en la carpeta:", ", ".join(sin_foto))
    sin_fila = [p.name for p in fotos if not (clave(p) & set(filas))]
    if filas and sin_fila: print(f"  Aviso: {len(sin_fila)} foto(s) sin fila en el Excel (llevan el título del nombre del archivo): " + ", ".join(sin_fila[:5]) + ("…" if len(sin_fila) > 5 else ""))
    print(f"  '{g['titulo']}': {len(items)} elementos  →  enlace: galeria.html?g={nombre}  (sube img/{nombre} y galerias.json)")

ap = argparse.ArgumentParser(description="Crea galerías a partir de la hoja Galerías del Excel.")
ap.add_argument("carpeta", nargs="?"); ap.add_argument("nombre", nargs="?")
ap.add_argument("--excel"); ap.add_argument("--fotos"); ap.add_argument("--solo")
ap.add_argument("--titulo"); ap.add_argument("--descripcion")
ap.add_argument("--tipo", default="Fotografía"); ap.add_argument("--fecha", default="")
ap.add_argument("--miniatura", type=int, default=400); ap.add_argument("--maximo", type=int, default=2000)
ap.add_argument("--forzar", action="store_true", help="regenera las imágenes aunque ya existan")
a = ap.parse_args()
excel = buscar_excel(a.excel)
try: hoja = leer_hoja(excel)
except Exception as e:
    print("Aviso: no he podido leer el Excel (¿está dañado?):", e); hoja = {}
bases = [Path(a.fotos)] if a.fotos else [BASE / "fotos", BASE, BASE.parent]
jpath = BASE / "galerias.json"
datos = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else {}
print("Excel:", excel if hoja else "sin hoja Galerías")
if a.carpeta:                      # modo manual o por nombre de carpeta
    carpeta = Path(a.carpeta) if Path(a.carpeta).is_dir() else buscar_carpeta(a.carpeta, bases)
    if not carpeta: sys.exit(f"No encuentro la carpeta '{a.carpeta}' (busqué en: {', '.join(str(b) for b in bases)}).")
    nombre = slug(a.nombre or carpeta.name); h = hoja.get(nombre, {"nombre": carpeta.name, "cab": {}, "filas": {}})
    trabajos = [(nombre, carpeta, {**h["cab"], "nombre": h["nombre"]}, h["filas"])]
else:                              # modo automático: todas las galerías de la hoja
    if not hoja: sys.exit("No hay hoja Galerías con datos. Indica el Excel con --excel o una carpeta de fotos.")
    trabajos = []
    for nombre, h in hoja.items():
        if a.solo and slug(a.solo) != nombre: continue
        carpeta = buscar_carpeta(h["nombre"], bases)
        if not carpeta: print(f"- {h['nombre']}: no encuentro una carpeta con ese nombre (busqué en: {', '.join(str(b) for b in bases)}). Se omite."); continue
        trabajos.append((nombre, carpeta, {**h["cab"], "nombre": h["nombre"]}, h["filas"]))
for nombre, carpeta, cab, filas in trabajos:
    print(f"- {cab['nombre']}  (carpeta: {carpeta})"); crear(nombre, carpeta, cab, filas, a, datos)
jpath.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
print("Hecho." if trabajos else "No se ha creado ninguna galería.")
