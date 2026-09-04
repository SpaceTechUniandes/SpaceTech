# Cómo contribuir

## Entorno

No hay dependencias que instalar. Sólo se necesita Python 3 (para los scripts
de `tools/`) y, si vas a tocar `api/`, Node 20 o superior.

```bash
npm run dev        # sirve public/ en http://localhost:8000
```

El sitio debe abrirse por HTTP, no con `file://`, o las rutas relativas y las
fuentes fallan.

## Ramas

| Rama | Para qué |
|---|---|
| `main` | Producción. Cada push publica en spacetech.lat. |
| `develop` | Integración. Aquí se juntan los cambios antes de producción. |
| `feat/…`, `fix/…`, `docs/…` | Trabajo puntual, sale de `develop`. |

Flujo normal:

```bash
git switch develop
git pull
git switch -c feat/descripcion-corta
# ... cambios ...
npm run check
git push -u origin feat/descripcion-corta
```

Luego abre un pull request contra `develop`. Cuando `develop` esté estable, se
mezcla a `main` y eso publica.

**No trabajes directo sobre `main`**: cada push a esa rama sale a producción.

## Antes de abrir un pull request

```bash
npm run check      # comprueba que ninguna referencia local esté rota
```

El CI repite esa comprobación y además valida la sintaxis del JavaScript y que
los fondos SVG sigan coincidiendo con su generador.

## Convenciones

### HTML

- Etiquetas semánticas: `header`, `nav`, `main`, `section`, `footer`, `article`.
- Comentarios en español en los puntos clave.
- **Nunca** JavaScript embebido: va en `public/assets/js/`.
- `alt` en toda imagen; `aria-*` donde haga falta.

### CSS

- Clases en inglés con BEM simplificado: `hero__title`, `nav__link--active`.
- Colores y medidas siempre desde las custom properties de `:root`.
- Sin frameworks. Sin `!important` salvo en `prefers-reduced-motion`.
- Indentación de 2 espacios (ver `.editorconfig`).

### JavaScript

- Vanilla, sin librerías externas.
- Un módulo por responsabilidad, envuelto en IIFE con `'use strict'`.
- Escuchadores de scroll siempre con `{ passive: true }`.

### Contenido

Si falta texto, deja el elemento vacío con un comentario HTML explicando qué
va ahí. **No escribas texto de relleno.** Los párrafos vacíos se ocultan solos
(`:empty { display: none }`), así que la página se ve intencional mientras
llega el contenido real.

## Añadir una división

1. Copia una página existente de `public/divisiones/`.
2. Ajusta título, índice, tag y la clase modificadora del fondo.
3. Añade la entrada al mega menú **en las siete páginas** (`index.html` y las
   seis de división): el menú está duplicado en cada una.
4. Si lleva fondo propio, añade el motivo a `tools/generate-backgrounds.py`,
   regenera y declara la clase `.page-hero--<nombre>` en el CSS.
5. `npm run check`.

## Accesibilidad

Antes de mezclar, revisa que se mantenga:

- Contraste por encima de AA (4.5:1) sobre los fondos
- Navegación completa con teclado, y foco visible
- `prefers-reduced-motion` respetado en animaciones y parallax
