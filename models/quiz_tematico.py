"""Quiz especializado que só aceita perguntas de um tema."""

from __future__ import annotations

from .pergunta import Pergunta
from .quiz import Quiz


class QuizTematico(Quiz):
    """Herda o comportamento de Quiz e restringe suas perguntas a um tema."""

    _tema: str

    def __init__(
        self,
        titulo: str,
        tema: str,
        perguntas: list[Pergunta] | None = None,
        limite_tentativas: int = 1,
        tempo_limite_minutos: int | None = None,
    ) -> None:
        if not isinstance(tema, str) or not tema.strip():
            raise ValueError("O tema do quiz não pode ficar vazio.")
        if perguntas is not None and not isinstance(perguntas, list):
            raise TypeError("As perguntas devem ser informadas em uma lista.")

        self._tema = tema
        super().__init__(
            titulo=titulo,
            perguntas=[],
            limite_tentativas=limite_tentativas,
            tempo_limite_minutos=tempo_limite_minutos,
        )
        for pergunta in perguntas or []:
            self.adicionar_pergunta(pergunta)

    @property
    def tema(self) -> str:
        return self._tema

    def adicionar_pergunta(self, pergunta: Pergunta) -> None:
        if not isinstance(pergunta, Pergunta):
            raise TypeError("O quiz aceita apenas objetos Pergunta.")
        if pergunta.tema != self._tema:
            raise ValueError("A pergunta deve pertencer ao tema do quiz.")
        super().adicionar_pergunta(pergunta)
