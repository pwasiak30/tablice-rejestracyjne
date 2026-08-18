#!/usr/bin/env python3
"""
build_html.py — składa finalny, samodzielny plik index.html z:
  - shell.html   (struktura HTML, znaczniki __STYLE__ / __DATA__ / __SCRIPT__)
  - style.css    (cały CSS, zgodny z claude/styl-wizualny.md tego projektu)
  - script.js    (cała logika JS, motyw + wyszukiwanie)
  - data.json    (dane krajów, generowane przez build_poland.py / build_all.py)

Aplikacja ma świadomie pozostać jednym plikiem HTML działającym offline
(zobacz README.md) — ten skrypt tylko automatyzuje sklejanie źródeł,
żeby style.css/script.js dało się edytować i wersjonować osobno.

Użycie:
    python3 build_html.py
"""
from pathlib import Path

ROOT = Path(__file__).parent

def main():
    shell = (ROOT / "shell.html").read_text(encoding="utf-8")
    style = (ROOT / "style.css").read_text(encoding="utf-8")
    script = (ROOT / "script.js").read_text(encoding="utf-8")
    data = (ROOT / "data.json").read_text(encoding="utf-8")

    out = shell.replace("/*__STYLE__*/", style, 1)
    out = out.replace("__DATA__", data, 1)
    out = out.replace("/*__SCRIPT__*/", script, 1)

    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"Zbudowano index.html ({len(out.encode('utf-8'))} bajtów).")

if __name__ == "__main__":
    main()
