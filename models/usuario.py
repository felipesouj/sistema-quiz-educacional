"""Modelo de usuário do Sistema de Quiz Educacional."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .quiz import Quiz
    from .tentativa import Tentativa


class Usuario:
    """Identifica quem responde aos quizzes e mantém seu histórico."""

    _nome: str
    _email: str
    _matricula_ou_id: str
    _tentativas: list[Tentativa]

    def __init__(self, nome: str, email: str, matricula_ou_id: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome não pode ficar vazio.")
        if not isinstance(email, str) or not email.strip():
            raise ValueError("O e-mail não pode ficar vazio.")
        if not isinstance(matricula_ou_id, str) or not matricula_ou_id.strip():
            raise ValueError("A matrícula ou o ID não pode ficar vazio.")

        self._nome = nome
        self._email = email
        self._matricula_ou_id = matricula_ou_id
        self._tentativas: list[Tentativa] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

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

        tentativa = Tentativa(self, quiz)
        self._tentativas.append(tentativa)
        return tentativa

    def consultar_historico(self) -> list[Tentativa]:
        return self._tentativas.copy()
