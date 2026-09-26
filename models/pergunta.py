"""Definição inicial de pergunta."""

from __future__ import annotations

from .nivel_dificuldade import NivelDificuldade


class Pergunta:
    """Representa uma pergunta de múltipla escolha de determinado tema."""

    enunciado: str
    alternativas: list[str]
    indice_resposta_correta: int
    tema: str
    dificuldade: NivelDificuldade

    def validar_alternativas(self) -> bool:
        """Validará a quantidade de alternativas em uma etapa futura."""
        raise NotImplementedError

    def validar_resposta_correta(self) -> bool:
        """Validará o índice da resposta correta em uma etapa futura."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Descreverá a pergunta em uma etapa futura."""
        raise NotImplementedError

    def __eq__(self, outra: object) -> bool:
        """Comparará enunciado e tema em uma etapa futura."""
        raise NotImplementedError