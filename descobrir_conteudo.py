"""Ponto de entrada do aplicativo."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from cli_app import modo_cli

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Descobrir a Extensao do Arquivo pelo Conteudo By Jair Lima"
    )
    parser.add_argument("alvo", nargs="?", default=None, help="Arquivo ou pasta para analisar")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Varrer subpastas")
    parser.add_argument("-y", "--sim", action="store_true", help="Renomear automaticamente sem perguntar")
    parser.add_argument("--cli", action="store_true", help="Forcar modo linha de comando")

    args = parser.parse_args()

    if args.alvo or args.cli:
        alvo = Path(args.alvo or os.getcwd())
        sys.exit(modo_cli(alvo, args.recursivo, args.sim))

    from gui_app import executar_gui

    executar_gui()


if __name__ == "__main__":
    main()
