"""Interface de linha de comando."""

from __future__ import annotations

from pathlib import Path

from core import ResultadoAnalise, renomear_arquivo, varrer_alvo


def _imprimir_resultado(resultado: ResultadoAnalise) -> None:
    extensao = resultado.extensao or "?"
    print(
        f"{resultado.nome:<30} "
        f"{resultado.mime:<40} "
        f"{extensao:<10} "
        f"{resultado.motivo}"
    )
    if resultado.erro:
        print(f"  erro tecnico: {resultado.erro}")


def modo_cli(alvo: Path, recursivo: bool = False, automatico: bool = False) -> int:
    """Executa o fluxo da CLI e retorna codigo de saida."""
    if not alvo.exists():
        print(f"Erro: caminho nao encontrado: {alvo}")
        return 1

    print("\nDescobrir a Extensao do Arquivo pelo Conteudo By Jair Lima")
    print(f"Alvo: {alvo}")
    print(f"Tipo: {'arquivo' if alvo.is_file() else 'pasta'}")
    if alvo.is_dir():
        print(f"Recursivo: {'Sim' if recursivo else 'Nao'}")
    print()

    resultados = varrer_alvo(alvo, recursivo)
    if not resultados:
        print("Nenhum arquivo elegivel para analise foi encontrado.")
        return 0

    print(f"{'Arquivo':<30} {'MIME Type':<40} {'Extensao':<10} Observacao")
    print("-" * 120)

    elegiveis = []
    for resultado in resultados:
        _imprimir_resultado(resultado)
        if resultado.elegivel and resultado.extensao:
            elegiveis.append(resultado)

    print(f"\nTotal analisado(s): {len(resultados)}")
    print(f"Renomeavel(is): {len(elegiveis)}")

    if not elegiveis:
        print("Nenhum arquivo pode ser renomeado com seguranca.")
        return 0

    if automatico:
        confirmar = True
    else:
        try:
            resp = input("\nDeseja renomear os arquivos identificados? (s/n): ").strip().lower()
        except EOFError:
            print("Entrada interativa indisponivel. Use -y para renomear automaticamente.")
            return 3
        confirmar = resp in {"s", "sim", "y", "yes"}

    if not confirmar:
        print("Operacao cancelada.")
        return 0

    sucesso = 0
    erros = 0
    for resultado in elegiveis:
        try:
            novo_caminho = renomear_arquivo(resultado.caminho, resultado.extensao)
            print(f"  OK {resultado.nome} -> {novo_caminho.name}")
            sucesso += 1
        except Exception as exc:  # pragma: no cover - depende do filesystem real
            print(f"  ERRO {resultado.nome} -> {exc}")
            erros += 1

    print(f"\nConcluido: {sucesso} renomeado(s), {erros} erro(s)")
    return 0 if erros == 0 else 2
