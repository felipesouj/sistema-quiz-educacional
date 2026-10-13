"""Modelo de usuário do Sistema de Quiz Educacional."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .pessoa import Pessoa

if TYPE_CHECKING:
    from .quiz import Quiz
    from .tentativa import Tentativa


class Usuario(Pessoa):
    """Identifica quem responde aos quizzes e mantém seu histórico."""

    _matricula_ou_id: str
    _tentativas: list[Tentativa]

    def __init__(self, nome: str, email: str, matricula_ou_id: str) -> None:
        super().__init__(nome, email)
        if not isinstance(matricula_ou_id, str) or not matricula_ou_id.strip():
            raise ValueError("A matrícula ou o ID não pode ficar vazio.")

        self._matricula_ou_id = matricula_ou_id
        self._tentativas: list[Tentativa] = []

    @property
    def matricula_ou_id(self) -> str:
        return self._matricula_ou_id

    @property
    def tentativas(self) -> list[Tentativa]:
        """Histórico exposto como uma cópia da lista interna."""
        return self._tentativas.copy()

    def iniciar_quiz(self, quiz: Quiz) -> Tentativa:
        """Cria uma tentativa e a adiciona ao histórico do usuário."""
        from .tentativa import Tentativa

        if not isinstance(quiz, Quiz):
            raise TypeError("O usuário só pode iniciar um objeto Quiz.")
        tentativas_no_quiz = sum(tentativa.quiz is quiz for tentativa in self._tentativas)
        if tentativas_no_quiz >= quiz.limite_tentativas:
            raise ValueError("O limite de tentativas para este quiz foi atingido.")
        if not quiz.perguntas:
            raise ValueError("Não é possível iniciar um quiz sem perguntas.")

        tentativa = Tentativa(self, quiz)
        self._tentativas.append(tentativa)
        return tentativa

    def consultar_historico(self) -> list[Tentativa]:
        return self._tentativas.copy()
