"""Escaneo didáctico de posibles claves API expuestas en el repositorio."""
from pathlib import Path
import re
import sys

# Patrones orientativos para detectar asignaciones que podrían contener secretos.
PATRONES = [
    re.compile(r"""(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*["'][^"']{8,}["']"""),
    re.compile(r"""(?i)AKIA[0-9A-Z]{16}"""),  # Identificador típico de AWS
]

ARCHIVOS_EXCLUIDOS = {".git"}
EXTENSIONES = {".py", ".json", ".yml", ".yaml", ".txt", ".env", ".js", ".ts"}

def main():
    encontrados = []
    for ruta in Path(".").rglob("*"):
        if not ruta.is_file() or any(parte in ARCHIVOS_EXCLUIDOS for parte in ruta.parts):
            continue
        if ruta.suffix.lower() not in EXTENSIONES and ruta.name != ".env":
            continue
        try:
            contenido = ruta.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for numero, linea in enumerate(contenido.splitlines(), start=1):
            if any(patron.search(linea) for patron in PATRONES):
                encontrados.append((ruta, numero))

    if encontrados:
        print("Posibles claves o tokens expuestos:")
        for ruta, numero in encontrados:
            print(f"- {ruta}:{numero}")
        sys.exit(1)

    print("Escaneo terminado: no se han detectado posibles claves API expuestas.")

if __name__ == "__main__":
    main()
