# SpaceTech AESS — Universidad de los Andes

Landing page del capítulo estudiantil de la **IEEE Aerospace and Electronic
Systems Society** en la Universidad de los Andes.

Producción: **https://spacetech.lat**

---

## Stack

Sitio estático, sin framework ni proceso de build.

- HTML semántico
- CSS vanilla con custom properties (sin Tailwind ni Bootstrap)
- JavaScript vanilla en módulos separados (sin jQuery, GSAP ni AOS)
- Tipografía: Albert Sans y IBM Plex Mono desde Google Fonts
- Gráficos de fondo en SVG generado, sin imágenes de stock

No hay dependencias que instalar: el sitio se abre y se despliega tal cual.

---

## Estructura

```
.
├── index.html              Página principal
├── divisiones/             Una página por división (rutas propias)
│   ├── teorica-computacional.html
│   ├── coheteria.html
│   ├── satelital.html
│   ├── sistemas-aeronauticos.html
│   ├── propulsor-ionico.html
│   └── sputnik-medios-creativos.html
├── css/
│   └── main.css            Variables, layout, tipografía, animaciones
├── js/
│   ├── nav.js              Header fijo, menú móvil, mega menú, año del footer
│   └── scroll.js           IntersectionObserver, scroll suave, parallax
├── brand/                  Logos institucionales, foto de equipo y fondos SVG
├── logo.png                Isotipo del capítulo
├── vercel.json             Cabeceras y configuración de despliegue
├── CNAME                   Dominio propio de GitHub Pages
└── .nojekyll               Evita el procesado Jekyll en GitHub Pages
```

Regla del proyecto: **cero JavaScript embebido en el HTML**. Toda la lógica
vive en `js/`. El CSS es solo presentación.

---

## Desarrollo local

El sitio necesita servirse por HTTP (no `file://`) para que las rutas
relativas y las fuentes carguen bien:

```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

Cualquier servidor estático sirve (`npx serve`, `php -S`, etc.).

---

## Despliegue

### Vercel

Proyecto estático sin build. Al importar el repositorio:

- **Framework preset:** Other
- **Build command:** vacío
- **Output directory:** `.` (raíz)

`vercel.json` ya define esos valores más las cabeceras de caché y seguridad,
así que la importación no necesita ajustes manuales.

Si en el futuro se añade backend, Vercel toma las funciones desde una carpeta
`api/` en la raíz; hoy el sitio no tiene ninguna y no requiere servidor.

### GitHub Pages

Ya está configurado y activo:

- Origen: rama `main`, carpeta raíz (`/`)
- Dominio propio: `spacetech.lat` (definido en `CNAME`, con HTTPS emitido)

Cada push a `main` publica automáticamente. **No conviene añadir un workflow
de Pages**: el repositorio usa el modo de publicación desde rama, y un
workflow obligaría a cambiar esa configuración.

Todas las rutas del sitio son relativas, así que funciona igual en el dominio
propio, en `github.io/SpaceTech/` o en una preview de Vercel.

---

## Sistema de diseño

### Color

La paleta sale del isotipo (`logo.png`): negro y oro.

| Variable | Valor | Uso |
|---|---|---|
| `--color-bg-primary` | `#0a0a0a` | Fondo base |
| `--color-bg-secondary` | `#121212` | Secciones alternas |
| `--color-accent` | `#f7ca45` | Oro del isotipo: etiquetas, acentos, estados activos |
| `--color-accent-hover` | `#d4a92e` | Estados `:hover` |
| `--color-text-primary` | `#f0f0f0` | Todo el texto |
| `--color-border` | `#2a2a2a` | Líneas divisorias |

No se usa gris para texto: todo va en blanco o en el oro de marca.

### Tipografía

- **Albert Sans** — titulares, cuerpo, nombres de división
- **IBM Plex Mono** — marca, navegación, etiquetas, tags, índices y datos

Solo se cargan los pesos 400 y 500, sin itálicas.

### Reglas visuales

Estética editorial y técnica: esquinas rectas (cero `border-radius`), sin
sombras decorativas, sin degradados de color, líneas divisorias de 1px y el
oro usado con moderación.

### Fondos SVG

Cada división tiene su propio fondo generado por código, compartiendo el
mismo sistema: campo de estrellas, trazos finos en gris y acentos en oro.

| Archivo | División | Motivo |
|---|---|---|
| `space-backdrop.svg` | Portada y Teórica | Órbitas y limbo planetario |
| `bg-coheteria.svg` | Cohetería | Curva braquistócrona con un cohete |
| `bg-satelital.svg` | Satelital | CubeSat en órbita con enlace a tierra |
| `bg-aeronauticos.svg` | Sistemas Aeronáuticos | Cuadricóptero y plan de vuelo |
| `bg-ionico.svg` | Propulsor Iónico | Tobera en corte y pluma de plasma |
| `bg-sputnik.svg` | Sputnik y Medios Creativos | Planetas y ondas de transmisión |

Un velo de oscurecimiento sobre la columna de texto garantiza contraste
WCAG AA sobre cualquiera de ellos.

---

## Contenido pendiente

Estos espacios están maquetados y esperando texto del equipo:

- Descripción de cada división (`<p class="section__text">` en `divisiones/*.html`)
- Sección de historia y benchmark en `index.html` (bloques `.track__slot`)
- Visuales propios de cada división (bloques `.page-slot`)

Los párrafos vacíos no se muestran (`:empty { display: none }`), así que la
página se ve intencional mientras el contenido llega.

---

## Accesibilidad

- Enlace de salto al contenido
- Roles y `aria-expanded` en el menú móvil y el mega menú
- `alt` en todas las imágenes
- Contraste verificado por encima de AA sobre todos los fondos
- `prefers-reduced-motion` respetado en animaciones y parallax

---

## Licencia

MIT — ver [LICENSE](LICENSE).
