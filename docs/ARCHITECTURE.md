# Arquitectura

## Panorama

Sitio estático sin proceso de build, con una carpeta de funciones serverless
lista para cuando haga falta backend. Se publica en dos sitios a la vez:

```
                    ┌─────────────────────────┐
   push a main ───► │  GitHub Actions         │
                    │  deploy-pages.yml       │
                    └───────────┬─────────────┘
                                │ sube public/
                                ▼
                    ┌─────────────────────────┐
                    │  GitHub Pages           │  spacetech.lat
                    │  (sólo frontend)        │  estático
                    └─────────────────────────┘

                    ┌─────────────────────────┐
   push a main ───► │  Vercel                 │  frontend + /api/*
                    │  vercel.json            │
                    └─────────────────────────┘
```

La diferencia importante: **Pages sirve sólo el frontend**. Las funciones de
`api/` únicamente existen en Vercel. Mientras el sitio no dependa de `/api/*`,
los dos despliegues son equivalentes.

## Estructura

```
.
├── public/                  Todo lo que se publica. Es la raíz del sitio.
│   ├── index.html           Portada
│   ├── charlas.html         Charlas y eventos
│   ├── divisiones/          Una página por división, ruta propia
│   ├── assets/
│   │   ├── css/main.css     Hoja de estilos única
│   │   ├── js/              Un módulo por responsabilidad
│   │   ├── img/             Logos y fotografía
│   │   └── backgrounds/     Fondos SVG generados por tools/
│   ├── CNAME                Dominio propio de Pages
│   └── .nojekyll            Evita el procesado Jekyll
│
├── api/                     Backend: funciones serverless de Vercel
│   └── health.js            GET /api/health
│
├── tools/                   Utilidades de desarrollo, no se publican
│   ├── generate-backgrounds.py
│   └── check-links.py
│
├── docs/                    Esta documentación
├── .github/workflows/       CI y despliegue
├── vercel.json              Configuración de Vercel
└── package.json             Scripts de desarrollo
```

`public/` es la frontera: lo que está dentro se sirve al navegador, lo que
está fuera no. Por eso los scripts de `tools/` pueden vivir en el repositorio
sin acabar expuestos.

## Frontend

Sin framework y sin dependencias. Tres piezas:

| Archivo | Responsabilidad |
|---|---|
| `assets/css/main.css` | Variables de diseño, layout, tipografía, animaciones |
| `assets/js/nav.js` | Header fijo, menú móvil, mega menú, año del footer |
| `assets/js/scroll.js` | IntersectionObserver, scroll suave, parallax |
| `assets/js/carousel.js` | Carruseles de tarjetas (historia, benchmark) |

Reglas del proyecto:

- **Cero JavaScript embebido en el HTML.** Toda la lógica vive en `assets/js/`.
- El CSS es sólo presentación, nunca lógica.
- Rutas siempre relativas, para que el sitio funcione igual en el dominio
  propio, en una preview de Vercel o bajo una subruta.

### Rutas

Cada división es una página independiente bajo `public/divisiones/`, no una
sección de la portada. Se llega a ellas desde el mega menú del header.

| Ruta | Página |
|---|---|
| `/` | Portada |
| `/charlas.html` | Charlas y eventos |
| `/divisiones/teorica-computacional.html` | División Teórica y Computacional |
| `/divisiones/coheteria.html` | División de Cohetería |
| `/divisiones/satelital.html` | División Satelital |
| `/divisiones/sistemas-aeronauticos.html` | División de Sistemas Aeronáuticos |
| `/divisiones/propulsor-ionico.html` | División de Propulsor Iónico |
| `/divisiones/sputnik-medios-creativos.html` | División Sputnik y Medios Creativos |

Los enlaces conservan la extensión `.html` a propósito: así funcionan igual en
Pages y en Vercel, sin depender de reescrituras del servidor.

## Backend

`api/` sigue la convención de Vercel: un archivo por endpoint, la ruta sale
del nombre. Hoy sólo hay `health.js`; ver [api/README.md](../api/README.md).

## Generación de assets

Los fondos SVG no se dibujan a mano: los produce
`tools/generate-backgrounds.py` con semillas fijas, así que regenerarlos da
exactamente los mismos bytes. El CI lo comprueba en cada cambio, para que el
archivo del repositorio nunca se desincronice del script que lo genera.

```bash
npm run backgrounds
```

## Verificaciones automáticas

`.github/workflows/ci.yml` corre en cada push y pull request:

- Toda referencia local (`src`, `href`, `url()`) resuelve a un archivo real
- El JavaScript del sitio y de `api/` es sintácticamente válido
- Los SVG del repositorio coinciden con los que genera el script

`.github/workflows/deploy-pages.yml` repite la verificación de enlaces antes
de publicar, de modo que un enlace roto no llega a producción.

## Carruseles

Los bloques de historia y benchmark son carruseles de tarjetas de noticia.
Cada bloque es un `[data-carousel]` que contiene su cabecera con controles y
una pista `[data-carousel-track]` con las tarjetas.

Para añadir un hito basta con copiar un `<article class="card">` dentro de la
pista: `carousel.js` recalcula el contador y habilita los controles solo. Con
una tarjeta o ninguna los oculta, de modo que un carrusel a medio llenar no
se ve roto — por eso el bloque de benchmark, todavía sin tarjetas, muestra su
marco reservado en lugar de una pista vacía.
