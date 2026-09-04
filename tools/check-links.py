#!/usr/bin/env python3
"""Verifica que toda referencia local del sitio resuelva a un archivo real.

Recorre el HTML y el CSS de public/ buscando src, href y url(...), descarta
lo externo (http, mailto, anclas) y comprueba que el archivo exista.

Uso:
    python3 tools/check-links.py

Devuelve 1 si encuentra referencias rotas, para poder usarlo en CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUBLIC = RAIZ / "public"

# src="..." o href="..." en HTML; url(...) en CSS
PATRON_HTML = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']')
PATRON_CSS = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')

EXTERNO = ("http://", "https://", "//", "mailto:", "tel:", "data:", "#")


def es_local(ref: str) -> bool:
    return bool(ref) and not ref.startswith(EXTERNO)


def revisar(archivo: Path, patron: re.Pattern[str]) -> list[str]:
    """Devuelve la lista de referencias rotas encontradas en `archivo`."""
    rotas = []
    for ref in patron.findall(archivo.read_text(encoding="utf-8")):
        if not es_local(ref):
            continue
        destino = (archivo.parent / ref.split("?")[0].split("#")[0]).resolve()
        if not destino.exists():
            rotas.append(f"{archivo.relative_to(RAIZ)} -> {ref}")
    return rotas


def main() -> int:
    if not PUBLIC.is_dir():
        print("ERROR: no existe public/", file=sys.stderr)
        return 1

    rotas: list[str] = []
    revisados = 0

    for archivo in sorted(PUBLIC.rglob("*.html")):
        rotas += revisar(archivo, PATRON_HTML)
        revisados += 1

    for archivo in sorted(PUBLIC.rglob("*.css")):
        rotas += revisar(archivo, PATRON_CSS)
        revisados += 1

    if rotas:
        print(f"{len(rotas)} referencia(s) rota(s) en {revisados} archivo(s):\n")
        for r in rotas:
            print(f"  ✗ {r}")
        return 1

    print(f"OK: todas las referencias locales resuelven ({revisados} archivos revisados)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
