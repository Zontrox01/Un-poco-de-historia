"""Genera datos.json (solo campos públicos) a partir del Excel.
Uso: python build_site.py Un_poco_de_historia_11.xlsx"""
import sys, json, openpyxl
SRC = sys.argv[1] if len(sys.argv) > 1 else "Un_poco_de_historia_11.xlsx"
# Solo nombre de pila para terceros (decisión del autor)
NOMBRES = {"Josep Enric Rizo Solanes": "Josep Enric", "Xavier Altès": "Xavier",
           "Javier de la Fuente Martínez": "Javier"}
def t(v):
    s = "" if v is None else str(v).strip()
    for a, b in NOMBRES.items(): s = s.replace(a, b)
    return s
wb = openpyxl.load_workbook(SRC)
def filas(hoja):
    ws = wb[hoja]; cab = [str(c.value or "").strip() for c in ws[1]]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if any(r): yield dict(zip(cab, r))
anios = []
for f in filas("Hoja1"):
    a = f.get("Año")
    if a is None: continue
    reg = {"anio": int(a), "historia": t(f.get("Historia")), "vida": t(f.get("Mi vida")),
           "informatica": t(f.get("Hitos, proyectos y eventos informáticos")), "so": t(f.get("S.O.")),
           "programas": t(f.get("Programas")), "enlaces": t(f.get("Enlace público (archivo / galería)")),
           "fuente": t(f.get("Estado de la fila Historia")).startswith("Verificado")}
    if any(reg[k] for k in ("historia", "vida", "informatica", "so", "programas", "enlaces")): anios.append(reg)
datos = {"anios": anios,
 "hilos": [{"hilo": t(f["Hilo"]), "texto": t(f["En palabras del autor"]), "anios": t(f["Años clave"])} for f in filas("Hilos del relato") if f.get("Hilo")],
 "obras": [{"obra": t(f["Obra"]), "tipo": t(f["Tipo"]), "fecha": t(f["Fecha de publicación (autor)"]), "plataforma": t(f["Plataforma"]), "enlace": t(f["Enlace"]).split()[0] if t(f["Enlace"]) else ""} for f in filas("Obras publicadas") if f.get("Obra")],
 "programas": [{"programa": t(f["Programa"]), "fabricante": t(f["Fabricante"]), "uso": t(f["Para qué lo usé / proyecto"]), "versiones": t(f["Versiones que usé (autor)"]), "anios": t(f["Años de uso (autor)"])} for f in filas("Programas") if f.get("Programa") and not str(f["Programa"]).startswith("(")]}
json.dump(datos, open("datos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(anios), "años;", len(datos["hilos"]), "hilos;", len(datos["obras"]), "obras;", len(datos["programas"]), "programas")
