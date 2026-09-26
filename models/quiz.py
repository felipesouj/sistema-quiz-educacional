"""Definição inicial de quiz."""

from __future__ import annotations

from typing import Iterator

from .pergunta import Pergunta


class Quiz:
    """Agrupa perguntas e define limites de execução."""

    titulo: str
    perguntas: list[Pergunta]
    limite_tentativas: int
    tempo_limite_minutos: int | None

    def calcular_pontuacao_maxima(self) -> int:
        """Calculará a pontuação máxima em uma etapa futura."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Retornará a quantidade de perguntas em uma etapa futura."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[Pergunta]:
        """Percorrerá as perguntas em uma etapa futura."""
        raise NotImplementedError