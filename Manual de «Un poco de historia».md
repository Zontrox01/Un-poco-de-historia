# Manual de «Un poco de historia»

*Guía de uso del Excel, los scripts y la web · octubre de 2026*

## 1. Cómo encaja todo

Hay tres piezas:

1. **El Excel** es la fuente de todo. Ahí escribes los textos, los datos y las galerías.
2. **Dos scripts de Python** convierten el Excel en archivos para la web: `build_site.py` (textos) y `crear_galeria.py` (fotos y vídeos).
3. **La web** vive en GitHub Pages (https://zontrox01.github.io/Un-poco-de-historia/) y solo lee los archivos que subas.

El flujo es siempre el mismo: **editas el Excel → ejecutas el script → subes los archivos nuevos a GitHub.**

## 2. Qué se sube a GitHub y qué no

**Se sube:** `index.html`, `galeria.html`, `estilo.css`, `visor.js`, `galeria.js`, `datos.json`, `galerias.json` y la carpeta `img/`.

**No se sube:**

- **El Excel**: lleva notas internas, alertas y pendientes.
- **Los scripts `.py`**: `build_site.py` contiene una lista con los apellidos completos de terceros (la web pública usa solo el nombre de pila).
- **Las fotos y vídeos originales.**

## 3. Requisitos (solo la primera vez)

Python 3 instalado y, en la consola:

```
pip install pillow openpyxl opencv-python
```

`opencv-python` solo hace falta para la miniatura de los vídeos (primer fotograma).

## 4. La carpeta de trabajo

```
Web/
  index.html  galeria.html  estilo.css  visor.js  galeria.js
  datos.json  galerias.json
  build_site.py  crear_galeria.py
  Un_poco_de_historia_XX.xlsx   (el Excel; también puede estar en la carpeta de arriba)
  img/<galeria>/                (lo crea crear_galeria.py)
  Hardware/  Ciberdromo/  ...   (carpetas con tus fotos originales, una por galería)
```

## 4b. Las hojas del Excel

| Hoja | Para qué sirve | ¿Se publica? |
| --- | --- | --- |
| **Hoja1** | La línea temporal. Columnas públicas: Año, Historia, Mi vida personal, Mi vida laboral, Mi formación, Hitos proyectos y eventos informáticos, S.O., Programas más relevantes y Enlace público. Internas: Estado, Alertas y Documentación. | Solo las columnas públicas |
| **Hilos del relato** | Temas transversales (coleccionar programas, robótica…) | Sí |
| **Obras publicadas** | Libros, trabajos, modelo de utilidad, pintura | Sí |
| **Programas** | Programas importantes, con versiones y años | Sí |
| **Enlaces** | Alias para los enlaces dentro del texto | No (se usa al generar) |
| **Galerías** | Una fila por galería y por foto o vídeo | No (se usa al crear galerías) |
| **Lenguajes y proyectos, Pendientes, Reglas del proyecto** | Trabajo interno | No |

## 5. Rutina para actualizar los textos

1. Edita el Excel, **guárdalo y ciérralo**.
2. En la carpeta `Web`, ejecuta:

   ```
   python build_site.py
   ```

   Usa el `.xlsx` modificado más recientemente y escribe «Usando: …» para que veas cuál ha abierto. Para forzar uno: `python build_site.py archivo.xlsx`.
3. **Lee los avisos** (ver apartado 9).
4. Sube `datos.json` a GitHub.
5. Espera uno o dos minutos y recarga la web con **Ctrl+F5**.

Resultado esperado con el Excel completo: «N años; 7 hilos; 9 obras; 15 programas» (las cifras crecen según añadas filas).

## 6. Enlaces dentro del texto

En cualquier celda se escribe `[texto visible](alias)`. Ejemplo: `Publicado en [PC Actual nº 99](pcactual99)`.

- Los alias se definen en la hoja **Enlaces** (alias, destino, descripción).
- También valen, sin pasar por la hoja: `[texto](#a1991)` para saltar a un año y `[texto](galeria.html?g=nombre)` para una galería.
- Si el alias no existe, el script avisa y deja solo el texto. Al terminar lista los alias que aún no has usado.

## 7. Galerías de fotos y vídeos

**Hay un solo archivo `galeria.html` para todas las galerías.** Cada galería es una entrada de `galerias.json`, y el enlace `galeria.html?g=nombre` dice cuál se muestra.

### Pasos

1. **Carpeta de fotos:** crea una carpeta con el nombre de la galería (por ejemplo `Hardware`) y mete dentro las fotos (jpg, png, webp…) y los vídeos (mp4). Debe estar en `Web/fotos/`, en `Web/` o en la carpeta de arriba.
2. **Hoja Galerías:** una fila de galería (columna Archivo vacía, con el título y la descripción) y una fila por archivo.

   | Galería | Archivo | Título | Detalle | Tipo | Fecha |
   | --- | --- | --- | --- | --- | --- |
   | Hardware |  | Mi hardware | Equipos que he tenido |  |  |
   | Hardware | c64.jpg | Commodore 64 | Mi primer ordenador | Fotografía | 1985 |

   El orden de las filas es el orden de la galería. Las celdas vacías no borran nada.
3. **Ejecuta** (todas las galerías de la hoja):

   ```
   python crear_galeria.py --excel Un_poco_de_historia_13.xlsx
   ```

   Para una sola: `python crear_galeria.py --solo Hardware`. Para indicar dónde están las carpetas: `--fotos RUTA`.
4. **Sube** `galerias.json` y la carpeta `img/<galeria>` completa.
5. El script te da el enlace (`galeria.html?g=hardware`). El nombre sale en minúsculas y sin tildes. Para usarlo en un texto, escríbelo directamente o crea un alias en la hoja Enlaces.

### Qué hace el script con cada archivo

- **Foto:** crea una copia web (hasta 2000 px) y una miniatura (400 px). Corrige la orientación y no copia metadatos (se elimina el GPS). El original no se toca.
- **Vídeo (mp4):** copia el vídeo y crea la miniatura con el **primer fotograma**.
- **Las miniaturas no se regeneran** si ya existen. Si no te gusta una, sustituye a mano el archivo `img/<galeria>/<nombre>-m.jpg` por otro con el mismo nombre y no se tocará. Con `--forzar` se regeneran todas.
- **Prioridad de datos:** Excel, luego lo que ya hubiera en `galerias.json`, luego las opciones de la línea de comandos.

### Vídeos

Al hacer clic en un vídeo se abre a **pantalla completa y en bucle**, con sonido si lo tiene. Se cierra con **Esc** o con el botón Cerrar. En la miniatura aparece un triángulo ▶. Límite práctico: GitHub **avisa a partir de 50 MB y no admite archivos de más de 100 MB**, así que conviene reducir los vídeos antes.

### Añadir o quitar archivos

Añade la foto a la carpeta, su fila a la hoja y vuelve a ejecutar el script. Si quitas una foto de la carpeta, su copia web se borra sola de `img/`. Hay que volver a subir lo que cambie.

## 8. Una foto o vídeo suelto dentro del texto

En una celda de la línea temporal, en una **línea propia**:

```
Compré el Commodore 64 con mi primer sueldo.
{foto: Hardware/c64.jpg}
```

En la web sale una tarjeta con la miniatura, el título, el detalle, el tipo y la fecha. Siempre está visible debajo del párrafo; al hacer clic se abre **solo esa imagen** (o ese vídeo) sobre fondo negro.

- **Varias a la vez:** `{foto: Hardware/zx81.jpg, Hardware/zx81-cassette.jpg}` salen en fila.
- **El nombre del archivo** puede escribirse con o sin extensión.
- **Requisito:** la foto debe estar ya en una galería, con su fila en la hoja Galerías.
- Si no existe, en la web aparece «\[foto no encontrada: …\]» y `build_site.py` te avisa.

## 9. Avisos y problemas frecuentes

| Lo que ves | Qué significa y qué hacer |
| --- | --- |
| «no encuentro una columna que empiece por…» | El script ha abierto otro Excel. Mira la línea «Usando:» y ejecuta `python build_site.py archivo.xlsx` con el bueno. |
| «alias que no existen en la hoja Enlaces» | Has escrito `[texto](algo)` y `algo` no está en la hoja Enlaces. Añádelo o corrige el nombre. |
| «fotos o vídeos {foto: …} que no existen» | Esa foto no está en `galerias.json`. Revisa el nombre de la galería y del archivo, y que hayas ejecutado `crear_galeria.py`. |
| «no encuentro una carpeta con ese nombre» | La galería está en el Excel pero no hay carpeta de fotos con ese nombre. Créala, o borra las filas si es un ejemplo. |
| «foto(s) sin fila en el Excel» | Hay fotos en la carpeta sin su fila en Galerías. Salen igualmente, con el nombre del archivo como título. |
| «miniatura genérica» (vídeos) | Falta `opencv-python`: `pip install opencv-python`. |
| La web no cambia | Espera uno o dos minutos y pulsa **Ctrl+F5**. Comprueba que has subido el archivo. |
| «No se pudo cargar datos.json» abriendo la página en tu ordenador | Abrir `index.html` con doble clic no carga los datos. Usa la web publicada, o en la carpeta `Web`: `python -m http.server` y abre http://localhost:8000 |

## 10. Chuleta

**Comandos**

```
python build_site.py
python build_site.py archivo.xlsx
python crear_galeria.py --excel archivo.xlsx
python crear_galeria.py --solo Hardware
python crear_galeria.py --forzar --solo Hardware
```

**Dentro del texto del Excel**

```
[texto](alias)
[texto](#a1991)
[texto](galeria.html?g=hardware)
{foto: Hardware/c64.jpg}
```

## 11. Decisiones del proyecto

- Los nombres de terceros salen solo con el **nombre de pila**.
- Los trabajos informáticos para la fábrica **solo se nombran**: por protección de datos no se publican documentos.
- Las fechas históricas marcadas «a verificar» están pendientes de comprobar; las marcadas «fuente verificada» se contrastaron con una fuente.
- Lo interno (alertas, pendientes, reglas, documentación por escanear) no se publica.
