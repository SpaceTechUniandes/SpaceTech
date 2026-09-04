# SpaceTech AESS — Universidad de los Andes

Sitio del capítulo estudiantil de la **IEEE Aerospace and Electronic Systems
Society** en la Universidad de los Andes.

**Producción:** https://spacetech.lat

---

## Qué hay aquí

Sitio estático sin proceso de build, con una carpeta de funciones serverless
lista para cuando haga falta backend.

```
.
├── public/                 Frontend. Es la raíz del sitio publicado.
│   ├── index.html
│   ├── divisiones/         Una página por división
│   └── assets/{css,js,img,backgrounds}
├── api/                    Backend: funciones serverless de Vercel
├── tools/                  Scripts de desarrollo (no se publican)
├── docs/                   Documentación
└── .github/workflows/      CI y despliegue
```

Detalle completo en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Stack

- HTML semántico, sin plantillas
- CSS vanilla con custom properties — sin Tailwind ni Bootstrap
- JavaScript vanilla en módulos separados — sin jQuery, GSAP ni AOS
- Albert Sans e IBM Plex Mono desde Google Fonts, sólo pesos 400 y 500
- Fondos SVG generados por código, sin imágenes de stock

Cero dependencias de runtime. `npm install` no instala nada porque no hace
falta nada.

## Desarrollo

```bash
npm run dev          # sirve public/ en http://localhost:8000
npm run check        # verifica que ninguna referencia local esté rota
npm run backgrounds  # regenera los fondos SVG
```

El sitio debe servirse por HTTP, no abrirse con `file://`.

## Ramas

| Rama | Para qué |
|---|---|
| `main` | Producción. Cada push publica en spacetech.lat. |
| `develop` | Integración. |
| `feat/…`, `fix/…`, `docs/…` | Trabajo puntual, sale de `develop`. |

Guía en [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Despliegue

### GitHub Pages — activo

Publicado por GitHub Actions desde `public/`
([deploy-pages.yml](.github/workflows/deploy-pages.yml)). Cada push a `main`
verifica los enlaces y republica. Dominio propio `spacetech.lat` con HTTPS.

Pages es hosting estático: sirve el frontend, **no ejecuta las funciones de
`api/`**.

### Vercel

Proyecto estático sin build. `vercel.json` ya define todo:

- **Output directory:** `public`
- **Build command:** ninguno
- Cabeceras de caché y de seguridad

Al importar el repositorio no hay que configurar nada a mano. A diferencia de
Pages, Vercel sí despliega `api/` como funciones serverless.

## Documentación

| Documento | Contenido |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Estructura, rutas, despliegues, verificaciones |
| [docs/DESIGN.md](docs/DESIGN.md) | Color, tipografía, reglas visuales, fondos |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Flujo de trabajo y convenciones |
| [api/README.md](api/README.md) | Endpoints y cómo añadir uno |

## Contenido pendiente

Estos espacios están maquetados y esperando texto del equipo:

- Descripción de cada división, en `public/divisiones/*.html`
- Historia y benchmark en la portada (bloques `.track__slot`)
- Visuales propios de cada división (bloques `.page-slot`)

Los párrafos vacíos no se muestran, así que la página se ve intencional
mientras el contenido llega.

## Accesibilidad

Enlace de salto al contenido, roles ARIA en los menús, `alt` en las imágenes,
contraste verificado por encima de AA sobre todos los fondos y
`prefers-reduced-motion` respetado.

## Licencia

MIT — ver [LICENSE](LICENSE).
