"""Exemplo de uso do Sistema de Quiz Educacional."""

from models import NivelDificuldade, Pergunta, Quiz, Usuario
from persistencia import carregar_dados, salvar_dados
from relatorios import gerar_relatorio


def main() -> None:
    pergunta = Pergunta(
        enunciado="Qual é a capital do Brasil?",
        alternativas=["São Paulo", "Brasília", "Rio de Janeiro"],
        indice_resposta_correta=1,
        tema="Geografia",
        dificuldade=NivelDificuldade.FACIL,
    )
    quiz = Quiz("Geografia básica", [pergunta], limite_tentativas=3)
    usuario = Usuario("Ana Silva", "ana@example.com", "A001")

    tentativa = usuario.iniciar_quiz(quiz)
    tentativa.registrar_resposta(1)
    tentativa.finalizar(tempo_total=8)

    salvar_dados([usuario], [quiz])
    usuarios_carregados, _ = carregar_dados()
    print(gerar_relatorio(usuarios_carregados))


if __name__ == "__main__":
    main()
