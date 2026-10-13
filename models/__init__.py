"""Modelos de domínio do Sistema de Quiz Educacional."""

from .nivel_dificuldade import NivelDificuldade
from .pergunta import Pergunta
from .pessoa import Pessoa
from .quiz import Quiz
from .tentativa import Tentativa
from .usuario import Usuario

__all__ = [
    "NivelDificuldade",
    "Pergunta",
    "Pessoa",
    "Quiz",
    "Tentativa",
    "Usuario",
]
