"""Modelo de uma pergunta de múltipla escolha."""

from __future__ import annotations

from .nivel_dificuldade import NivelDificuldade


class Pergunta:
    """Representa uma pergunta com alternativas e resposta correta."""

    _enunciado: str
    _alternativas: list[str]
    _indice_resposta_correta: int
    _tema: str
    _dificuldade: NivelDificuldade

    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        indice_resposta_correta: int,
        tema: str,
        dificuldade: NivelDificuldade,
    ) -> None:
        if not isinstance(alternativas, list):
            raise TypeError("As alternativas devem ser informadas em uma lista de textos.")
        if not isinstance(enunciado, str) or not enunciado.strip():
            raise ValueError("O enunciado não pode ficar vazio.")
        if not isinstance(tema, str) or not tema.strip():
            raise ValueError("O tema não pode ficar vazio.")
        if not isinstance(dificuldade, NivelDificuldade):
            raise TypeError("A dificuldade deve ser um NivelDificuldade.")

        self._enunciado = enunciado
        self._alternativas = list(alternativas)
        self._indice_resposta_correta = indice_resposta_correta
        self._tema = tema
        self._dificuldade = dificuldade

        if not self.validar_alternativas():
            raise ValueError("A pergunta deve ter entre 3 e 5 alternativas válidas.")
        if not self.validar_resposta_correta():
            raise ValueError("O índice da resposta correta deve apontar para uma alternativa.")

    @property
    def enunciado(self) -> str:
        """Texto apresentado ao usuário."""
        return self._enunciado

    @property
    def alternativas(self) -> list[str]:
        """Alternativas em ordem, expostas como uma cópia da lista interna."""
        return self._alternativas.copy()

    @property
    def indice_resposta_correta(self) -> int:
        """Índice da alternativa correta, começando em zero."""
        return self._indice_resposta_correta

    @property
    def tema(self) -> str:
        """Tema ao qual a pergunta pertence."""
        return self._tema

    @property
    def dificuldade(self) -> NivelDificuldade:
        """Nível de dificuldade da pergunta."""
        return self._dificuldade

    def validar_alternativas(self) -> bool:
        """Informa se há de três a cinco alternativas textuais não vazias."""
        return 3 <= len(self._alternativas) <= 5 and all(
            isinstance(alternativa, str) and alternativa.strip()
            for alternativa in self._alternativas
        )

    def validar_resposta_correta(self) -> bool:
        """Informa se o índice correto aponta para uma alternativa existente."""
        return (
            isinstance(self._indice_resposta_correta, int)
            and not isinstance(self._indice_resposta_correta, bool)
            and 0 <= self._indice_resposta_correta < len(self._alternativas)
        )

    def __str__(self) -> str:
        return self._enunciado

    def __eq__(self, outra: object) -> bool:
        if not isinstance(outra, Pergunta):
            return False
        return self._enunciado == outra._enunciado and self._tema == outra._tema
