"""Geração de um relatório textual simples de desempenho."""

from typing import Iterable

from models import Usuario


def gerar_relatorio(usuarios: Iterable[Usuario]) -> str:
    """Retorna um resumo de tentativas por usuário."""
    linhas = ["RELATÓRIO DE DESEMPENHO", "=" * 24]

    for usuario in usuarios:
        tentativas = usuario.consultar_historico()
        linhas.append(f"\n{usuario.nome} ({usuario.matricula_ou_id})")
        if not tentativas:
            linhas.append("  Nenhuma tentativa registrada.")
            continue

        for numero, tentativa in enumerate(tentativas, start=1):
            if tentativa.concluida:
                resultado = (
                    f"{tentativa.pontuacao_obtida}/{len(tentativa.quiz)} pontos, "
                    f"{tentativa.taxa_acertos:.0f}% de acertos, "
                    f"{tentativa.tempo_total:.1f} s"
                )
            else:
                resultado = f"em andamento ({len(tentativa.respostas)}/{len(tentativa.quiz)} respostas)"
            linhas.append(f"  {numero}. {tentativa.quiz.titulo}: {resultado}")

    return "\n".join(linhas)
