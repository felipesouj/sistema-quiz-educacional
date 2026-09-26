"""Níveis de dificuldade previstos para as perguntas."""

from enum import Enum


class NivelDificuldade(Enum):
    """Restringe a dificuldade aos três níveis do projeto."""

    FACIL = "fácil"
    MEDIO = "médio"
    DIFICIL = "difícil"