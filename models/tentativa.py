"""Modelo de uma tentativa de um usuário em um quiz."""

from __future__ import annotations

from math import isfinite

from .quiz import Quiz
from .usuario import Usuario


class Tentativa:
    """Registra o estado inicial de uma execução de quiz."""

    _usuario: Usuario
    _quiz: Quiz
    _respostas: list[int]
    _pontuacao_obtida: int
    _tempo_total: float
    _taxa_acertos: float
    _concluida: bool

    def __init__(self, usuario: Usuario, quiz: Quiz) -> None:
        if not isinstance(usuario, Usuario):
            raise TypeError("A tentativa deve pertencer a um Usuario.")
        if not isinstance(quiz, Quiz):
            raise TypeError("A tentativa deve se referir a um Quiz.")
        if not quiz.perguntas:
            raise ValueError("Não é possível iniciar uma tentativa em um quiz sem perguntas.")

        self._usuario = usuario
        self._quiz = quiz
        quiz._marcar_tentativa_iniciada()
        self._respostas: list[int] = []
        self._pontuacao_obtida = 0
        self._tempo_total = 0.0
        self._taxa_acertos = 0.0
        self._concluida = False

    def registrar_resposta(self, indice_alternativa: int) -> None:
        """Registra a alternativa escolhida para a próxima pergunta."""
        if self._concluida:
            raise ValueError("A tentativa já foi concluída.")
        if len(self._respostas) >= len(self._quiz):
            raise ValueError("Todas as perguntas já foram respondidas.")

        pergunta = self._quiz.perguntas[len(self._respostas)]
        if (
            not isinstance(indice_alternativa, int)
            or isinstance(indice_alternativa, bool)
            or not 0 <= indice_alternativa < pergunta.numero_opcoes
        ):
            raise ValueError("A alternativa informada não existe.")
        self._respostas.append(indice_alternativa)

    def finalizar(self, tempo_total: float = 0.0) -> None:
        """Calcula o resultado e encerra a tentativa."""
        if self._concluida:
            raise ValueError("A tentativa já foi concluída.")
        if len(self._respostas) != len(self._quiz):
            raise ValueError("Responda a todas as perguntas antes de finalizar.")
        if not isinstance(tempo_total, (int, float)) or isinstance(tempo_total, bool):
            raise ValueError("O tempo total deve ser um número finito não negativo.")
        try:
            duracao = float(tempo_total)
        except OverflowError as erro:
            raise ValueError("O tempo total deve ser um número finito não negativo.") from erro
        if not isfinite(duracao) or duracao < 0:
            raise ValueError("O tempo total deve ser um número finito não negativo.")

        acertos = sum(
            pergunta.corrigir(resposta)
            for resposta, pergunta in zip(self._respostas, self._quiz)
        )
        self._pontuacao_obtida = acertos
        self._tempo_total = duracao
        self._taxa_acertos = acertos / len(self._quiz) * 100
        self._concluida = True

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    @property
    def respostas(self) -> list[int]:
        """Respostas registradas, expostas como uma cópia da lista interna."""
        return self._respostas.copy()

    @property
    def pontuacao_obtida(self) -> int:
        return self._pontuacao_obtida

    @property
    def tempo_total(self) -> float:
        return self._tempo_total

    @property
    def taxa_acertos(self) -> float:
        return self._taxa_acertos

    @property
    def concluida(self) -> bool:
        return self._concluida
