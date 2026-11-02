"""Modelos de domínio do Sistema de Quiz Educacional."""

from .nivel_dificuldade import NivelDificuldade
from .pergunta import Pergunta, PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso
from .pessoa import Pessoa
from .quiz import Quiz
from .quiz_tematico import QuizTematico
from .tentativa import Tentativa
from .usuario import Usuario

__all__ = [
    "NivelDificuldade",
    "Pergunta",
    "PerguntaMultiplaEscolha",
    "PerguntaVerdadeiroFalso",
    "Pessoa",
    "Quiz",
    "QuizTematico",
    "Tentativa",
    "Usuario",
]
