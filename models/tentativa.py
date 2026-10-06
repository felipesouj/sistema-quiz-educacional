"""Modelo de uma tentativa de um usuário em um quiz."""

from __future__ import annotations

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

        self._usuario = usuario
        self._quiz = quiz
        self._respostas: list[int] = []
        self._pontuacao_obtida = 0
        self._tempo_total = 0.0
        self._taxa_acertos = 0.0
        self._concluida = False

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
