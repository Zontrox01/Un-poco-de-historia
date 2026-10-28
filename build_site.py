"""Genera datos.json (solo campos públicos) a partir del Excel.
Uso: python build_site.py Un_poco_de_historia_11.xlsx
Las columnas se localizan por el principio del encabezado, así que pequeños cambios de nombre no lo rompen."""
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
def campo(f, *pref):
    for k, v in f.items():
        if any(k.lower().startswith(p) for p in pref): return t(v)
    return ""
cab1 = [str(c.value or "").strip().lower() for c in wb["Hoja1"][1]]
for p in ("año", "historia", "mi vida personal", "mi vida laboral", "mi formación", "hitos", "s.o.", "programas", "enlace", "estado"):
    if not any(c.startswith(p) for c in cab1): print("Aviso: no encuentro una columna que empiece por", repr(p))
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
print(len(anios), "años;", len(datos["hilos"]), "hilos;", len(datos["obras"]), "obras;", len(datos["programas"]), "programas")
