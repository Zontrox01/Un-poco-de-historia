"""Genera datos.json (solo campos públicos) a partir del Excel.
Uso: python build_site.py [archivo.xlsx]
Sin argumento usa el .xlsx modificado más recientemente (en esta carpeta o en la de arriba).
Las columnas se localizan por el principio del encabezado, así que pequeños cambios de nombre no lo rompen."""
import sys, json, re, openpyxl
from pathlib import Path
def elegir():
    if len(sys.argv) > 1: return sys.argv[1]
    aqui = Path(__file__).resolve().parent
    cand = [p for d in (aqui, aqui.parent) for p in d.glob("*.xlsx") if not p.name.startswith("~$")]
    if not cand: sys.exit("No encuentro ningún .xlsx. Indica el archivo: python build_site.py archivo.xlsx")
    return str(max(cand, key=lambda p: p.stat().st_mtime))
SRC = elegir()
print("Usando:", SRC)
# Solo nombre de pila para terceros (decisión del autor)
NOMBRES = {"Josep Enric Rizo Solanes": "Josep Enric", "Xavier Altès": "Xavier",
           "Javier de la Fuente Martínez": "Javier"}
wb = openpyxl.load_workbook(SRC)
# Hoja "Enlaces": alias -> destino. En el texto se escribe [texto](alias)
ALIAS, USADOS, FALTAN = {}, set(), set()
if "Enlaces" in wb.sheetnames:
    for r in wb["Enlaces"].iter_rows(min_row=2, values_only=True):
        if r[0] and r[1]: ALIAS[str(r[0]).strip().lower()] = str(r[1]).strip().replace(" ", "%20")
def enlace(m):
    txt, dest = m.group(1), m.group(2).strip()
    k = dest.lower()
    if k in ALIAS: USADOS.add(k); return f"[{txt}]({ALIAS[k]})"
    if re.match(r"(https?://|galeria\.html\?|#a\d+$)", dest): return m.group(0)
    FALTAN.add(dest); return txt
def t(v):
    s = "" if v is None else str(v).strip()
    for a, b in NOMBRES.items(): s = s.replace(a, b)
    return re.sub(r"\[([^\]]+)\]\(([^)\n]+)\)", enlace, s)
def filas(hoja):
    ws = wb[hoja]; cab = [str(c.value or "").strip() for c in ws[1]]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if any(r): yield dict(zip(cab, r))
def campo(f, *pref):
    for k, v in f.items():
        if any(k.lower().startswith(p) for p in pref): return t(v)
    return ""
cab1 = [str(c.value or "").strip().lower() for c in wb["Hoja1"][1]]
for p in ("año", "historia", "mi vida personal", "mi vida laboral", "mi formación", "hitos", "s.o.", "programas", "enlace", "estado"):
    if not any(c.startswith(p) for c in cab1):
        print("Aviso: no encuentro una columna que empiece por", repr(p), "\n  Encabezados de Hoja1 en este archivo:", cab1)
anios = []
for f in filas("Hoja1"):
    a = campo(f, "año")
    if not a[:4].isdigit(): continue
    reg = {"anio": int(a[:4]), "historia": campo(f, "historia"), "personal": campo(f, "mi vida personal"),
           "laboral": campo(f, "mi vida laboral"), "formacion": campo(f, "mi formación"),
           "informatica": campo(f, "hitos"), "so": campo(f, "s.o."), "programas": campo(f, "programas"),
           "enlaces": campo(f, "enlace"), "fuente": campo(f, "estado").startswith("Verificado")}
    if any(reg[k] for k in ("historia", "personal", "laboral", "formacion", "informatica", "so", "programas", "enlaces")): anios.append(reg)
datos = {"anios": anios,
 "hilos": [{"hilo": campo(f, "hilo"), "texto": campo(f, "en palabras"), "anios": campo(f, "años clave")} for f in filas("Hilos del relato") if campo(f, "hilo")],
 "obras": [{"obra": campo(f, "obra"), "tipo": campo(f, "tipo"), "fecha": campo(f, "fecha"), "plataforma": campo(f, "plataforma"),
            "enlace": (campo(f, "enlace").split() or [""])[0]} for f in filas("Obras publicadas") if campo(f, "obra")],
 "programas": [{"programa": campo(f, "programa"), "fabricante": campo(f, "fabricante"), "uso": campo(f, "para qué"),
                "versiones": campo(f, "versiones que usé"), "anios": campo(f, "años de uso")}
               for f in filas("Programas") if campo(f, "programa") and not campo(f, "programa").startswith("(")]}
json.dump(datos, open("datos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if FALTAN: print("Aviso: alias que no existen en la hoja Enlaces (se deja solo el texto):", sorted(FALTAN))
sin = sorted(set(ALIAS) - USADOS)
print("Enlaces:", len(USADOS), "usados" + ("; sin usar todavía: " + ", ".join(sin) if sin else ""))
print(len(anios), "años;", len(datos["hilos"]), "hilos;", len(datos["obras"]), "obras;", len(datos["programas"]), "programas")
