"""Modelo de um quiz e das perguntas que ele reúne."""

from __future__ import annotations

from typing import Iterator

from .pergunta import Pergunta


class Quiz:
    """Agrupa perguntas e mantém os limites definidos para o quiz."""

    _titulo: str
    _perguntas: list[Pergunta]
    _limite_tentativas: int
    _tempo_limite_minutos: int | None

    def __init__(
        self,
        titulo: str,
        perguntas: list[Pergunta] | None = None,
        limite_tentativas: int = 1,
        tempo_limite_minutos: int | None = None,
    ) -> None:
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("O título do quiz não pode ficar vazio.")
        if (
            not isinstance(limite_tentativas, int)
            or isinstance(limite_tentativas, bool)
            or limite_tentativas < 1
        ):
            raise ValueError("O limite de tentativas deve ser um inteiro positivo.")
        if tempo_limite_minutos is not None and (
            not isinstance(tempo_limite_minutos, int)
            or isinstance(tempo_limite_minutos, bool)
            or tempo_limite_minutos < 1
        ):
            raise ValueError("O tempo limite deve ser um inteiro positivo ou None.")

        self._titulo = titulo
        self._perguntas = list(perguntas) if perguntas is not None else []
        self._limite_tentativas = limite_tentativas
        self._tempo_limite_minutos = tempo_limite_minutos

        if any(not isinstance(pergunta, Pergunta) for pergunta in self._perguntas):
            raise TypeError("O quiz aceita apenas objetos Pergunta.")

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def perguntas(self) -> list[Pergunta]:
        """Perguntas do quiz, expostas como uma cópia da lista interna."""
        return self._perguntas.copy()

    @property
    def limite_tentativas(self) -> int:
        return self._limite_tentativas

    @property
    def tempo_limite_minutos(self) -> int | None:
        return self._tempo_limite_minutos

    def adicionar_pergunta(self, pergunta: Pergunta) -> None:
        if not isinstance(pergunta, Pergunta):
            raise TypeError("O quiz aceita apenas objetos Pergunta.")
        self._perguntas.append(pergunta)

    def remover_pergunta(self, pergunta: Pergunta) -> None:
        self._perguntas.remove(pergunta)

    def calcular_pontuacao_maxima(self) -> int:
        """Considera um ponto possível por pergunta."""
        return len(self._perguntas)

    def __len__(self) -> int:
        return len(self._perguntas)

    def __iter__(self) -> Iterator[Pergunta]:
        return iter(self._perguntas)
