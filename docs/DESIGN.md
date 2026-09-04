# Sistema de diseño

Registro editorial y técnico: composición deliberada, jerarquía clara y el
acento usado con moderación. Sin adornos, sin plantillas genéricas.

## Color

La paleta sale del isotipo (`public/assets/img/logo.png`): negro y oro.

| Variable | Valor | Uso |
|---|---|---|
| `--color-bg-primary` | `#0a0a0a` | Fondo base |
| `--color-bg-secondary` | `#121212` | Secciones alternas |
| `--color-accent` | `#f7ca45` | Oro del isotipo: etiquetas, tags, estados activos |
| `--color-accent-hover` | `#d4a92e` | Estados `:hover` |
| `--color-text-primary` | `#f0f0f0` | Todo el texto |
| `--color-border` | `#2a2a2a` | Líneas divisorias |
| `--color-border-faint` | `#1a1a1a` | Retícula técnica |

**No se usa gris para texto.** Todo va en blanco o en el oro de marca. Esa fue
una decisión explícita: el gris apagaba la página.

## Tipografía

Dos familias con roles separados:

- **Albert Sans** — titulares, cuerpo, nombres de división. La voz editorial.
- **IBM Plex Mono** — marca, navegación, eyebrows, tags, índices, cifras y
  datos de las fichas. Todo lo que es dato técnico.

El contraste entre ambas es el recurso principal: los datos se leen como
instrumentación y el discurso como texto editorial.

Sólo se cargan los pesos **400 y 500**, sin itálicas. Antes de añadir un peso,
comprueba que se use de verdad: cada variante extra es descarga que paga el
visitante.

| Elemento | Tamaño |
|---|---|
| Titular del hero | `clamp(2.4rem, 3.6vw, 3.6rem)`, peso 500 |
| Títulos de sección | `clamp(1.6rem, 3vw, 2.8rem)`, peso 500 |
| Etiquetas | `0.7rem`, mayúsculas, `letter-spacing: 0.05em` |
| Cuerpo | `1rem`, peso 400, `line-height: 1.6` |

El tracking de las etiquetas es `0.05em` y no `0.08em` porque la mono ya trae
sus propios espacios laterales.

## Reglas visuales

- **Cero `border-radius`.** Esquinas rectas siempre.
- **Cero sombras decorativas.**
- **Cero degradados de color.** Sólo se permite oscurecimiento en negro con
  alfa, para proteger la legibilidad sobre los fondos.
- Fondo casi negro como base; las secciones alternan entre `--color-bg-primary`
  y `--color-bg-secondary` para dar ritmo.
- Divisorias finas de 1px en vez de espacio vacío excesivo.
- El oro nunca como fondo de sección completa.

## Fondos SVG

Cada división tiene su propio fondo generado por código. Todos comparten el
mismo sistema: campo de estrellas blanco con acentos en oro, trazos finos en
gris y un velo de oscurecimiento. Cambia sólo el motivo.

| Archivo | División | Motivo |
|---|---|---|
| `space-backdrop.svg` | Portada y Teórica | Órbitas y limbo planetario |
| `bg-coheteria.svg` | Cohetería | Curva braquistócrona con un cohete |
| `bg-satelital.svg` | Satelital | CubeSat en órbita con enlace a tierra |
| `bg-aeronauticos.svg` | Sistemas Aeronáuticos | Cuadricóptero y plan de vuelo |
| `bg-ionico.svg` | Propulsor Iónico | Tobera en corte y pluma de plasma |
| `bg-sputnik.svg` | Sputnik y Medios Creativos | Planetas y ondas de transmisión |

Nada de imágenes de stock: todo es vectorial y generado, así que pesa poco y
se ve nítido en cualquier pantalla.

### Dónde colocar un motivo nuevo

El `page-hero` es mucho más ancho que alto, y con `background-size: cover`
**sólo se ve la banda vertical central del SVG**. Coloca el motivo entre
`y = 300` y `y = 700` del `viewBox` de 1600×1000, o no se verá.

Mantenlo además a la derecha de `x ≈ 700`: la columna izquierda es donde va el
texto.

### Contraste

Los motivos llevan trazos claros que pueden cruzar la columna de texto. Un
velo lateral en CSS (`.page-hero::before`) garantiza el contraste sobre
cualquier fondo, actual o futuro. Medido sobre los seis: el peor caso queda en
**7.2:1**, muy por encima del 4.5:1 que pide AA.

Si añades un fondo, vuelve a medir antes de mezclar.

## Responsive

Mobile first. Breakpoints en `768px`, `1024px` y `1440px`.

El hero de la portada mide **exactamente una pantalla** a cualquier altura de
viewport: la fotografía absorbe el espacio sobrante mediante flex, de modo que
la franja de fichas siempre cierra justo en el borde inferior. Verificado a
663, 713, 813 y 913 px de alto.

## Tamaño de las tarjetas

`--card-scale` controla el ancho de las tarjetas del carrusel. Vale `1` en
móvil y `0.7071` (1/√2) desde 768px, lo que deja **la mitad de área**
conservando la proporción 4:3: el encuadre de la fotografía no cambia, sólo
su tamaño.

En móvil no se reduce a propósito. La tarjeta ya es estrecha y encogerla deja
el texto en líneas de pocas letras.

Para ajustar el tamaño de todas las tarjetas a la vez basta con cambiar esa
variable; no hay medidas duplicadas por breakpoint.
