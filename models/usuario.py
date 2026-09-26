"""Definição inicial de usuário."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .quiz import Quiz
    from .tentativa import Tentativa


class Usuario:
    """Identifica quem responde aos quizzes e mantém suas tentativas."""

    nome: str
    email: str
    matricula_ou_id: str
    tentativas: list[Tentativa]

    def iniciar_quiz(self, quiz: Quiz) -> Tentativa:
        """Iniciará uma tentativa em uma etapa futura."""
        raise NotImplementedError