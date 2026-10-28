"""Crea una galería: miniaturas, imágenes para web y su entrada en galerias.json.
Uso:  python crear_galeria.py CARPETA_FOTOS nombre-galeria --titulo "Ciberdromo: inauguración" --fecha 2002
Requiere Pillow:  pip install pillow
Las fotos originales no se tocan. Las copias web no llevan metadatos (ni GPS)."""
import argparse, json, re, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageOps
EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
def anio_exif(im):
    try:
        e = im.getexif(); v = e.get_ifd(0x8769).get(36867) or e.get(306)
        return str(v)[:4] if v and str(v)[:4].isdigit() else ""
    except Exception:
        return ""
def natural(p): return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", p.name)]
ap = argparse.ArgumentParser()
ap.add_argument("carpeta"); ap.add_argument("nombre")
ap.add_argument("--titulo"); ap.add_argument("--descripcion")
ap.add_argument("--tipo", default="Fotografía"); ap.add_argument("--fecha", default="")
ap.add_argument("--miniatura", type=int, default=400); ap.add_argument("--maximo", type=int, default=2000)
ap.add_argument("--forzar", action="store_true", help="regenera las imágenes aunque ya existan")
a = ap.parse_args()
if not re.fullmatch(r"[a-z0-9-]+", a.nombre): sys.exit("El nombre solo puede llevar minúsculas, números y guiones (ej.: ciberdromo-2002).")
fotos = sorted((p for p in Path(a.carpeta).iterdir() if p.suffix.lower() in EXT), key=natural)
if not fotos: sys.exit("No hay imágenes en esa carpeta.")
base = Path(__file__).resolve().parent
destino = base / "img" / a.nombre; destino.mkdir(parents=True, exist_ok=True)
jpath = base / "galerias.json"
datos = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else {}
g = datos.setdefault(a.nombre, {"titulo": a.titulo or a.nombre, "descripcion": a.descripcion or "", "items": []})
if a.titulo: g["titulo"] = a.titulo
if a.descripcion is not None: g["descripcion"] = a.descripcion
previos = {it.get("origen"): it for it in g["items"] if it.get("origen")}
items, validos = [], set()
for i, p in enumerate(fotos, 1):
    stem = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", p.stem).encode("ascii", "ignore").decode().lower()).strip("-") or "foto"
    nom = f"{i:03d}-{stem}"; full, mini = destino / f"{nom}.jpg", destino / f"{nom}-m.jpg"
    validos |= {full.name, mini.name}
    with Image.open(p) as im:
        año = a.fecha or anio_exif(im)
        if a.forzar or not (full.exists() and mini.exists()):
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((a.maximo, a.maximo)); im.save(full, "JPEG", quality=85, optimize=True)
            im.thumbnail((a.miniatura, a.miniatura)); im.save(mini, "JPEG", quality=80, optimize=True)
    it = previos.get(p.name) or {"titulo": re.sub(r"[_-]+", " ", p.stem).strip(), "detalle": "", "tipo": a.tipo, "fecha": año}
    it.update({"origen": p.name, "miniatura": f"img/{a.nombre}/{mini.name}", "imagen": f"img/{a.nombre}/{full.name}"})
    items.append(it)
for viejo in destino.glob("*.jpg"):
    if viejo.name not in validos: viejo.unlink()
g["items"] = items
jpath.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Galería '{a.nombre}': {len(items)} fotos.\nEnlace para el Excel: galeria.html?g={a.nombre}\nSube la carpeta img/{a.nombre} y galerias.json a GitHub.")
