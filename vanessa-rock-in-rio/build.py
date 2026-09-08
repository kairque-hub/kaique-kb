#!/usr/bin/env python3
"""Gera index.html a partir de page.template.html, embutindo as fotos como data URI."""
import base64
import pathlib

BASE = pathlib.Path(__file__).parent
FOTOS = {
    "PUBLICO": "img/publico.jpg",
    "DUO": "img/duo.jpg",
    "PB": "img/pb.jpg",
    "PERFIL": "img/perfil.jpg",
}


def data_uri(rel):
    raw = (BASE / rel).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode()


def main():
    html = (BASE / "page.template.html").read_text()
    for chave, rel in FOTOS.items():
        html = html.replace("{{" + chave + "}}", data_uri(rel))
    saida = BASE / "index.html"
    saida.write_text(html)
    print(f"index.html: {saida.stat().st_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
