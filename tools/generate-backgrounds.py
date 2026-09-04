"""Genera los fondos SVG de cada división.

Uso:
    python3 tools/generate-backgrounds.py

Escribe en public/assets/backgrounds/. Las semillas son fijas: regenerar
produce exactamente los mismos archivos.

Todos comparten sistema: negro de base, campo de estrellas blanco con acentos
amarillos, trazos finos en gris y un velo de oscurecimiento inferior-izquierdo
que protege el contraste del texto. Cambia sólo el motivo central.

El motivo se coloca en la banda vertical y=[300,700]: el page-hero es mucho
más ancho que alto, así que con background-size:cover sólo se ve esa franja.
"""
import math
import pathlib
import random

SALIDA = pathlib.Path(__file__).resolve().parent.parent / 'public' / 'assets' / 'backgrounds'

W, H = 1600, 1000
GRIS = '#333333'
GRIS_2 = '#242424'
AMAR = '#f7ca45'
BLANCO = '#ffffff'


def cabecera():
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" role="presentation">',
        '  <defs>',
        '    <radialGradient id="velo" cx="16%" cy="60%" r="70%">',
        '      <stop offset="0%" stop-color="#0a0a0a" stop-opacity="0.9"/>',
        '      <stop offset="100%" stop-color="#0a0a0a" stop-opacity="0"/>',
        '    </radialGradient>',
        '  </defs>',
    ]


def estrellas(semilla, n=185, evitar=None):
    """Campo de estrellas con separación mínima. `evitar` son zonas del motivo."""
    rnd = random.Random(semilla)
    puestas, intentos = [], 0
    while len(puestas) < n and intentos < 9000:
        intentos += 1
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        if any((x - ex) ** 2 + (y - ey) ** 2 < 29 ** 2 for ex, ey, *_ in puestas):
            continue
        if evitar and any((x - cx) ** 2 + (y - cy) ** 2 < r ** 2 for cx, cy, r in evitar):
            continue
        rad = round(rnd.choice([0.6, 0.7, 0.8, 1.0, 1.2, 1.5]), 1)
        op = round(rnd.uniform(0.22, 0.82), 2)
        amarilla = rnd.random() < 0.07
        if amarilla:
            op = round(min(0.95, op + 0.15), 2)
        puestas.append((x, y, rad, op, amarilla))

    out = ['  <!-- Campo de estrellas -->']
    for x, y, rad, op, amarilla in puestas:
        out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" '
                   f'fill="{AMAR if amarilla else BLANCO}" opacity="{op}"/>')
    return out


def limbo(cx=W * 0.44, cy=H * 2.55, r=H * 1.82):
    return [
        '  <!-- Limbo planetario -->',
        f'  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" '
        f'stroke="{GRIS}" stroke-width="1.5"/>',
        f'  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r + 50:.0f}" fill="none" '
        f'stroke="{GRIS_2}" stroke-width="1"/>',
    ]


def velo():
    return [f'  <rect width="{W}" height="{H}" fill="url(#velo)"/>']


def cerrar():
    return ['</svg>']


def cruz(x, y, s=5, col=BLANCO, op=0.45, sw=1):
    return (f'  <path d="M{x - s:.1f} {y:.1f}h{s * 2}M{x:.1f} {y - s:.1f}v{s * 2}" '
            f'stroke="{col}" stroke-width="{sw}" opacity="{op}"/>')


def escribir(nombre, cuerpo):
    ruta = SALIDA / nombre
    ruta.write_text('\n'.join(cuerpo) + '\n')
    print(f'  {nombre:24s} {len(chr(10).join(cuerpo)):>6d} bytes')


# ---------------------------------------------------------------- cohetería
def coheteria():
    """Braquistócrona (cicloide) contra la cuerda recta, con un cohete sobre ella."""
    p = cabecera()
    p += limbo()
    p += ['  <!-- Braquistócrona: cicloide, curva de descenso más rápido -->']

    r = 190
    x0, y0 = 400, 250

    def punto(t):
        return x0 + r * (t - math.sin(t)), y0 + r * (1 - math.cos(t))

    # Cuerda recta de referencia (el camino más corto, no el más rápido)
    xa, ya = punto(0)
    xb, yb = punto(math.pi)
    p.append(f'  <path d="M{xa:.1f} {ya:.1f}L{xb:.1f} {yb:.1f}" fill="none" '
             f'stroke="{GRIS_2}" stroke-width="1" stroke-dasharray="5 9"/>')

    # La cicloide
    pts = [punto(math.pi * i / 120) for i in range(121)]
    d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    p.append(f'  <path d="{d}" fill="none" stroke="{GRIS}" stroke-width="1.5"/>')

    # Tramo resaltado en acento
    pts_a = [punto(math.pi * i / 120) for i in range(72, 112)]
    d_a = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts_a)
    p.append(f'  <path d="{d_a}" fill="none" stroke="{AMAR}" stroke-width="1.5" opacity="0.5"/>')

    # Marcas de descenso, perpendiculares a la curva
    p.append('  <!-- Marcas de descenso -->')
    for i in range(1, 10):
        t = math.pi * i / 10
        x, y = punto(t)
        dx, dy = r * (1 - math.cos(t)), r * math.sin(t)
        n = math.hypot(dx, dy)
        nx, ny = -dy / n, dx / n
        p.append(f'  <path d="M{x - nx * 7:.1f} {y - ny * 7:.1f}L{x + nx * 7:.1f} {y + ny * 7:.1f}" '
                 f'stroke="{GRIS}" stroke-width="1" opacity="0.7"/>')

    # Cohete sobre la curva, alineado a la tangente
    t = math.pi * 0.86
    x, y = punto(t)
    ang = math.degrees(math.atan2(r * math.sin(t), r * (1 - math.cos(t))))
    p.append('  <!-- Cohete -->')
    p.append(f'  <g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale(1.35)" fill="none" '
             f'stroke="{BLANCO}" stroke-width="1.2" opacity="0.9">')
    p.append('    <path d="M-26 -9 L14 -9 L30 0 L14 9 L-26 9 Z"/>')          # fuselaje
    p.append('    <path d="M-26 -9 L-38 -19 L-16 -9"/>')                      # aleta superior
    p.append('    <path d="M-26 9 L-38 19 L-16 9"/>')                         # aleta inferior
    p.append(f'    <path d="M14 -9 L14 9" stroke="{AMAR}" opacity="0.9"/>')   # mamparo
    p.append('  </g>')
    # Estela
    p.append(f'  <g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale(1.35)">')
    for i, (dx2, op) in enumerate([(-46, 0.55), (-58, 0.38), (-70, 0.22), (-82, 0.12)]):
        p.append(f'    <circle cx="{dx2}" cy="0" r="{2.4 - i * 0.4:.1f}" fill="{AMAR}" opacity="{op}"/>')
    p.append('  </g>')

    p += estrellas(101, evitar=[(x, y, 130)])
    p += velo()
    p += cerrar()
    return p


# ---------------------------------------------------------------- satelital
def satelital():
    """CubeSat sobre su órbita, con enlace a tierra."""
    p = cabecera()
    p += limbo()

    CX, CY, RX, RY, ROT = 880, 480, 540, 195, -14
    rot = math.radians(ROT)

    def en_orbita(t):
        ex, ey = RX * math.cos(t), RY * math.sin(t)
        return (CX + ex * math.cos(rot) - ey * math.sin(rot),
                CY + ex * math.sin(rot) + ey * math.cos(rot))

    p.append('  <!-- Órbitas -->')
    for rx, ry, col, op, dash in [(RX, RY, GRIS, 1.0, None),
                                  (RX - 175, RY - 63, GRIS_2, 1.0, None),
                                  (RX + 190, RY + 68, AMAR, 0.3, '5 11')]:
        d = f' stroke-dasharray="{dash}"' if dash else ''
        p.append(f'  <ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" '
                 f'stroke="{col}" stroke-width="1" opacity="{op}" '
                 f'transform="rotate({ROT} {CX} {CY})"{d}/>')

    # CubeSat alineado a la tangente
    t = 1.15
    x, y = en_orbita(t)
    dx, dy = -RX * math.sin(t), RY * math.cos(t)
    ang = math.degrees(math.atan2(dy * math.cos(rot) + dx * math.sin(rot),
                                  dx * math.cos(rot) - dy * math.sin(rot)))
    p.append('  <!-- CubeSat 3U con paneles solares -->')
    p.append(f'  <g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale(1.35)" fill="none" '
             f'stroke="{BLANCO}" stroke-width="1.2" opacity="0.9">')
    p.append('    <rect x="-15" y="-15" width="30" height="30"/>')
    p.append('    <path d="M-15 -5h30M-15 5h30" opacity="0.5"/>')            # divisiones 3U
    p.append(f'    <rect x="-46" y="-9" width="28" height="18" stroke="{GRIS}"/>')
    p.append(f'    <rect x="18" y="-9" width="28" height="18" stroke="{GRIS}"/>')
    p.append(f'    <path d="M0 -15 L0 -30" stroke="{AMAR}" opacity="0.9"/>')  # antena
    p.append('  </g>')

    # Enlace descendente hacia la superficie
    p.append('  <!-- Enlace descendente -->')
    gx, gy = 700, 905
    p.append(f'  <path d="M{x:.1f} {y:.1f}L{gx} {gy}" stroke="{AMAR}" stroke-width="1" '
             f'opacity="0.28" stroke-dasharray="3 8"/>')
    p.append(cruz(gx, gy, 6, AMAR, 0.5))
    for rr, op in ((26, 0.3), (42, 0.18), (58, 0.1)):
        p.append(f'  <path d="M{gx - rr} {gy}a{rr} {rr} 0 0 1 {rr * 2} 0" fill="none" '
                 f'stroke="{AMAR}" stroke-width="1" opacity="{op}"/>')

    p += estrellas(202, evitar=[(CX, CY, 200)])
    p += velo()
    p += cerrar()
    return p


# ------------------------------------------------------- sistemas aeronáuticos
def aeronauticos():
    """Cuadricóptero en planta con su plan de vuelo y curvas de nivel."""
    p = cabecera()

    p.append('  <!-- Curvas de nivel -->')
    for i, (cy, rr, op) in enumerate([(880, 620, 0.9), (880, 760, 0.6), (880, 900, 0.35)]):
        p.append(f'  <ellipse cx="620" cy="{cy}" rx="{rr}" ry="{rr * 0.34:.0f}" fill="none" '
                 f'stroke="{GRIS_2}" stroke-width="1" opacity="{op}"/>')

    # Plan de vuelo con waypoints
    p.append('  <!-- Plan de vuelo -->')
    wps = [(210, 620), (470, 430), (760, 505), (1010, 355), (1310, 430)]
    d = 'M' + 'L'.join(f'{x} {y}' for x, y in wps)
    p.append(f'  <path d="{d}" fill="none" stroke="{GRIS}" stroke-width="1" stroke-dasharray="7 7"/>')
    for i, (x, y) in enumerate(wps):
        col = AMAR if i == 3 else BLANCO
        op = 0.7 if i == 3 else 0.35
        p.append(f'  <rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="none" '
                 f'stroke="{col}" stroke-width="1" opacity="{op}"/>')

    # Cuadricóptero en el waypoint activo
    cx, cy = 1010, 355
    p.append('  <!-- Cuadricóptero -->')
    p.append(f'  <g transform="translate({cx} {cy})" fill="none" stroke="{BLANCO}" '
             f'stroke-width="1.5" opacity="0.85">')
    p.append('    <path d="M-11 -11 L11 11M11 -11 L-11 11"/>')               # chasis
    p.append('    <rect x="-11" y="-11" width="22" height="22"/>')
    brazos = [(-62, -62), (62, -62), (62, 62), (-62, 62)]
    for bx, by in brazos:
        p.append(f'    <path d="M{bx * 0.18:.0f} {by * 0.18:.0f}L{bx} {by}"/>')
        p.append(f'    <circle cx="{bx}" cy="{by}" r="30" stroke="{GRIS}" '
                 f'stroke-dasharray="4 6" opacity="0.9"/>')
        p.append(f'    <circle cx="{bx}" cy="{by}" r="3.5" fill="{BLANCO}" stroke="none" opacity="0.5"/>')
    p.append(f'    <path d="M0 -11 L0 -34" stroke="{AMAR}" opacity="0.9"/>')  # mástil
    p.append('  </g>')

    # Haz del sensor hacia el suelo
    p.append(f'  <path d="M{cx} {cy + 14}L{cx - 105} {cy + 300}M{cx} {cy + 14}L{cx + 105} {cy + 300}" '
             f'fill="none" stroke="{AMAR}" stroke-width="1" opacity="0.2"/>')

    p += estrellas(303, evitar=[(cx, cy, 130)])
    p += velo()
    p += cerrar()
    return p


# ---------------------------------------------------------- propulsor iónico
def ionico():
    """Tobera en corte con rejillas de óptica iónica y pluma de plasma."""
    p = cabecera()

    ex, ey = 700, 480          # plano de salida
    p.append('  <!-- Cámara y tobera en corte -->')
    p.append(f'  <g fill="none" stroke="{BLANCO}" stroke-width="1.5" opacity="0.8">')
    p.append(f'    <path d="M{ex - 250} {ey - 52} L{ex - 96} {ey - 52} L{ex - 58} {ey - 26} '
             f'L{ex} {ey - 74}"/>')                                            # pared superior
    p.append(f'    <path d="M{ex - 250} {ey + 52} L{ex - 96} {ey + 52} L{ex - 58} {ey + 26} '
             f'L{ex} {ey + 74}"/>')                                            # pared inferior
    p.append(f'    <path d="M{ex - 250} {ey - 52} L{ex - 250} {ey + 52}"/>')   # fondo de cámara
    p.append('  </g>')

    # Rejillas de óptica iónica
    p.append('  <!-- Rejillas de óptica iónica -->')
    for gx, op in ((ex - 74, 0.85), (ex - 58, 0.5)):
        p.append(f'  <path d="M{gx} {ey - 34}L{gx} {ey + 34}" stroke="{AMAR}" '
                 f'stroke-width="1" opacity="{op}" stroke-dasharray="3 4"/>')

    # Líneas de campo dentro de la cámara
    p.append('  <!-- Líneas de campo -->')
    for off in (-34, -17, 0, 17, 34):
        p.append(f'  <path d="M{ex - 232} {ey + off} Q{ex - 150} {ey + off * 0.45:.0f} '
                 f'{ex - 86} {ey + off * 0.3:.0f}" fill="none" stroke="{GRIS}" '
                 f'stroke-width="1" opacity="0.55"/>')

    # Pluma: iones acelerados, cono divergente
    p.append('  <!-- Pluma de plasma -->')
    rnd = random.Random(404)
    for _ in range(420):
        u = rnd.random() ** 0.55
        x = ex + u * 780
        media = 74 + u * 210
        y = ey + rnd.gauss(0, media / 2.6)
        if abs(y - ey) > media:
            continue
        op = round(max(0.07, 0.9 * (1 - u * 0.82) * rnd.uniform(0.55, 1.0)), 2)
        col = AMAR if rnd.random() < 0.5 else BLANCO
        p.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([0.8, 1.0, 1.3]):.1f}" '
                 f'fill="{col}" opacity="{op}"/>')

    # Envolvente del cono
    p.append(f'  <path d="M{ex} {ey - 74}L{ex + 780} {ey - 284}" stroke="{GRIS_2}" stroke-width="1"/>')
    p.append(f'  <path d="M{ex} {ey + 74}L{ex + 780} {ey + 284}" stroke="{GRIS_2}" stroke-width="1"/>')

    p += estrellas(404, n=120, evitar=[(ex + 300, ey, 330)])
    p += velo()
    p += cerrar()
    return p


# ------------------------------------------------- sputnik y medios creativos
def sputnik():
    """Planetas, el Sputnik y sus ondas de transmisión."""
    p = cabecera()

    p.append('  <!-- Planetas -->')
    p.append(f'  <circle cx="1230" cy="430" r="235" fill="none" stroke="{GRIS}" stroke-width="1.5"/>')
    p.append(f'  <ellipse cx="1230" cy="430" rx="330" ry="82" fill="none" stroke="{GRIS}" '
             f'stroke-width="1" opacity="0.75" transform="rotate(-20 1230 430)"/>')
    p.append(f'  <ellipse cx="1230" cy="430" rx="300" ry="70" fill="none" stroke="{GRIS_2}" '
             f'stroke-width="1" transform="rotate(-20 1230 430)"/>')
    p.append(f'  <circle cx="470" cy="330" r="86" fill="none" stroke="{GRIS_2}" stroke-width="1.5"/>')
    p.append(f'  <circle cx="905" cy="760" r="48" fill="none" stroke="{GRIS_2}" stroke-width="1"/>')

    # Terminador del planeta grande
    p.append(f'  <path d="M1230 195 a235 235 0 0 0 0 470" fill="none" stroke="{GRIS_2}" '
             f'stroke-width="1" opacity="0.8"/>')

    # Sputnik con sus cuatro antenas
    sx, sy = 700, 520
    p.append('  <!-- Sputnik -->')
    p.append(f'  <g transform="translate({sx} {sy})" fill="none" stroke="{BLANCO}" '
             f'stroke-width="1.5" opacity="0.85">')
    p.append('    <circle cx="0" cy="0" r="15"/>')
    for a in (198, 232, 322, 356):
        rad = math.radians(a)
        p.append(f'    <path d="M{15 * math.cos(rad):.1f} {15 * math.sin(rad):.1f}'
                 f'L{62 * math.cos(rad):.1f} {62 * math.sin(rad):.1f}"/>')
    p.append('  </g>')

    # Ondas de transmisión
    p.append('  <!-- Ondas de transmisión -->')
    for rr, op in ((58, 0.42), (96, 0.3), (140, 0.2), (192, 0.12), (250, 0.07)):
        p.append(f'  <circle cx="{sx}" cy="{sy}" r="{rr}" fill="none" stroke="{AMAR}" '
                 f'stroke-width="1" opacity="{op}"/>')

    # Trayectoria del Sputnik
    p.append(f'  <ellipse cx="860" cy="500" rx="600" ry="215" fill="none" stroke="{AMAR}" '
             f'stroke-width="1" opacity="0.22" stroke-dasharray="5 11" '
             f'transform="rotate(-12 860 500)"/>')

    p += estrellas(505, evitar=[(1230, 430, 250), (sx, sy, 150)])
    p += velo()
    p += cerrar()
    return p


print('Fondos generados:')
escribir('bg-coheteria.svg', coheteria())
escribir('bg-satelital.svg', satelital())
escribir('bg-aeronauticos.svg', aeronauticos())
escribir('bg-ionico.svg', ionico())
escribir('bg-sputnik.svg', sputnik())
