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

## 8. Enlazar una palabra a una o varias fotos, vídeos, audios o PDF

En una celda de la línea temporal, pon entre corchetes las palabras que quieres enlazar y, justo detrás, la marca con la galería y el archivo:

```
Tuve un [ZX81]{foto: Hardware/zx81.jpg} con cassette.
Compro el iPhone 4 [ver más fotos]{foto: Teléfonos móviles/01-iphone4.jpg, Teléfonos móviles/02-iphone4.jpg, Teléfonos móviles/03-iphone4.jpg}
```

En la web, las palabras son **un solo enlace**. Al hacer clic se abre una página con el estilo de la galería y **solo las tarjetas de esas fotos** (una, o todas las que hayas puesto), cada una con miniatura, título, detalle, tipo y fecha. Desde una tarjeta se abre la imagen a tamaño completo sobre fondo negro; un PDF se abre en una pestaña nueva. **La página principal no muestra ninguna imagen.**

- Galería y archivo se escriben **como los tienes en el Excel**: con espacios, tildes, mayúsculas o guiones bajos. Vale con o sin extensión. Para varias, sepáralas con comas (un nombre de archivo no puede llevar comas).
- Sin corchetes, `{foto: …}` también funciona. Con una sola foto, el enlace lleva el **título de la foto**; con varias, dice «Ver N fotos».
- La página de las fotos incluye un enlace a la galería completa de la que salen.
- El botón **Volver** de esas páginas te lleva de vuelta al sitio de la historia desde el que entraste, en el mismo punto (no al inicio).
- Si una foto no existe, sale «\[foto no encontrada: …\]» junto al enlace y `build_site.py` te avisa.
- Las fotos deben estar ya en una galería, con su fila en la hoja Galerías.
- **Alias a una galería completa** (hoja Enlaces): el destino lleva el nombre de la galería tal como sale en el Excel, por ejemplo `galeria.html?g=Teléfonos móviles`, no el de una foto.
- Los archivos de `img/` se guardan con otro nombre (minúsculas, sin tildes, con guiones), pero eso es interno: no se escribe nunca en el Excel.
- Para que funcione hay que subir `index.html`, `galeria.js`, `galeria.html` y `estilo.css`.
- El título y la descripción de la galería salen de la fila de galería del Excel (Archivo vacío) o, si no la hay, del propio nombre de la galería. Cada vez que ejecutas `crear_galeria.py` se recalculan.

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

## 12. Formatos admitidos: audio y PDF

Los archivos se convierten antes a estos formatos. Los otros tipos (wav, mov, webm…) no se admiten.

| Tipo | Formatos | En la web |
| --- | --- | --- |
| Imagen | jpg, png (y webp, bmp, tif) | Miniatura; al hacer clic, la imagen sobre fondo negro |
| Vídeo | mp4 | Pantalla completa y en bucle |
| Audio | mp3 | Reproductor sobre fondo negro, **una sola vez** |
| Documento | pdf | Se abre en una **pestaña nueva**, con la etiqueta PDF en la miniatura |

- **Audio:** la miniatura es un recuadro gris con una nota ♪. Si quieres otra, sustituye a mano el archivo `-m.jpg` de esa galería. Para que el audio se repita en bucle, en `visor.js` cambia `const BUCLE_AUDIO=false;` por `true`.
- **PDF:** la miniatura es la primera página. Necesita `pip install pymupdf`; sin ello sale un recuadro gris con «PDF». En el visor, las flechas saltan los PDF.
- Un PDF o un mp3 se usan igual que una foto: fila en la hoja Galerías y, dentro del texto, `{foto: Galería/archivo.pdf}`.

## 13. Orden, títulos y estilo de los apartados de cada año

**Orden y nombre de los apartados (Historia, Mi vida laboral…):** se definen en `index.html`, en la línea que empieza por `const CAMPOS=`. Cada pareja es `["clave","Título visible"]` y el orden de la lista es el orden en la web. Cambiar el orden de las columnas del Excel **no** cambia la web, y cambiar un encabezado del Excel tampoco cambia el título visible.

**Lo que sí puedes hacer en el Excel:** mover columnas de sitio libremente. `build_site.py` las encuentra por el **principio** de su encabezado, así que no cambies el principio de estos: Año, Historia, Mi vida personal, Mi vida laboral, Mi formación, Hitos, S.O., Programas, Enlace y Estado. Si lo cambias, el script te avisa de que no encuentra la columna.

**Color y tamaño de los títulos:** en `estilo.css`.

- Los títulos de apartado («Historia», «Mi vida personal»…) son la regla `h3`. El tamaño está en `font:600 .75rem` y el color en `color:var(--mut)`. Para que cambie solo dentro de las fichas, y no en el título «Años» de la columna derecha, usa `article h3`.
- El año grande de cada ficha es la regla `h2` (`font:700 1.5rem` y `color:var(--acc)`).
- Los colores generales están al principio del archivo, en `:root`, y la versión para modo oscuro justo debajo. `--acc` es el color de acento y `--mut` el gris de los títulos.

Ejemplo, títulos más grandes y azules, también en modo oscuro (se añade al final de `estilo.css`):

```
article h3{font-size:.95rem;color:#1f5fa8}
@media (prefers-color-scheme:dark){article h3{color:#7fb2ff}}
```

Si quitas `text-transform:uppercase` de la regla `h3`, los títulos dejan de salir en mayúsculas.

## 14. Nombres de galería en los enlaces

En los enlaces, el nombre de la galería puede ir con mayúsculas, tildes o espacios: `galeria.html?g=Dublin`, `g=dublin` y `g=El Tricicle` valen. La web (`galeria.js`) lo convierte a minúsculas, sin tildes y con guiones antes de buscarlo, y `build_site.py` hace lo mismo al generar `datos.json`.

Si el nombre no corresponde a ninguna galería, la página muestra **«Galería no encontrada»** y la lista de las que existen, con enlace. Nunca enseña otra galería por error.

**Si todos los enlaces llevan a la misma galería** (la primera de la lista): casi seguro que la web tiene un `galeria.js` antiguo. Sube el nuevo y recarga con Ctrl+F5.

**Foto sin fila en el Excel:** `crear_galeria.py` la sube igualmente, con el nombre del archivo como título. Para darle título, añade su fila en la hoja Galerías con el nombre exacto del archivo y vuelve a ejecutar el script.
