"""Hierarquia de perguntas do quiz (abstração, herança e polimorfismo)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .nivel_dificuldade import NivelDificuldade


class Pergunta(ABC):
    """Abstração de uma pergunta: o que toda pergunta precisa oferecer.

    Subclasses definem *como* as opções são apresentadas e *como* uma resposta
    é corrigida. Quem usa uma ``Pergunta`` (``Quiz``, ``Tentativa``, CLI) não
    precisa saber qual é o tipo concreto: é o polimorfismo em ação.
    """

    tipo: str = ""

    def __init__(self, enunciado: str, tema: str, dificuldade: NivelDificuldade) -> None:
        if not isinstance(enunciado, str) or not enunciado.strip():
            raise ValueError("O enunciado não pode ficar vazio.")
        if not isinstance(tema, str) or not tema.strip():
            raise ValueError("O tema não pode ficar vazio.")
        if not isinstance(dificuldade, NivelDificuldade):
            raise TypeError("A dificuldade deve ser um NivelDificuldade.")
        self._enunciado = enunciado
        self._tema = tema
        self._dificuldade = dificuldade

    @property
    def enunciado(self) -> str:
        """Texto apresentado ao usuário."""
        return self._enunciado

    @property
    def tema(self) -> str:
        """Tema ao qual a pergunta pertence."""
        return self._tema

    @property
    def dificuldade(self) -> NivelDificuldade:
        """Nível de dificuldade da pergunta."""
        return self._dificuldade

    @property
    @abstractmethod
    def opcoes(self) -> list[str]:
        """Opções exibidas ao usuário, em ordem (cópia da lista interna)."""

    @abstractmethod
    def corrigir(self, indice_opcao: int) -> bool:
        """Informa se a opção de índice ``indice_opcao`` é a correta."""

    @property
    def numero_opcoes(self) -> int:
        """Quantidade de opções disponíveis."""
        return len(self.opcoes)

    def __str__(self) -> str:
        return self._enunciado

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._enunciado!r}, tema={self._tema!r})"

    def __eq__(self, outra: object) -> bool:
        if not isinstance(outra, Pergunta):
            return False
        return self._enunciado == outra._enunciado and self._tema == outra._tema

    def __hash__(self) -> int:
        return hash((self._enunciado, self._tema))


class PerguntaMultiplaEscolha(Pergunta):
    """Pergunta com três a cinco alternativas e uma delas correta."""

    tipo = "multipla_escolha"

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
        super().__init__(enunciado, tema, dificuldade)
        self._alternativas = list(alternativas)
        self._indice_resposta_correta = indice_resposta_correta

        if not self.validar_alternativas():
            raise ValueError("A pergunta deve ter entre 3 e 5 alternativas válidas.")
        if not self.validar_resposta_correta():
            raise ValueError("O índice da resposta correta deve apontar para uma alternativa.")

    @property
    def alternativas(self) -> list[str]:
        """Alternativas em ordem, expostas como uma cópia da lista interna."""
        return self._alternativas.copy()

    @property
    def indice_resposta_correta(self) -> int:
        """Índice da alternativa correta, começando em zero."""
        return self._indice_resposta_correta

    @property
    def opcoes(self) -> list[str]:
        return self.alternativas

    def corrigir(self, indice_opcao: int) -> bool:
        return (
            isinstance(indice_opcao, int)
            and not isinstance(indice_opcao, bool)
            and 0 <= indice_opcao < len(self._alternativas)
            and indice_opcao == self._indice_resposta_correta
        )

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


class PerguntaVerdadeiroFalso(Pergunta):
    """Pergunta com duas opções fixas: Verdadeiro (índice 0) e Falso (índice 1)."""

    tipo = "verdadeiro_falso"
    _OPCOES = ("Verdadeiro", "Falso")

    def __init__(
        self,
        enunciado: str,
        afirmacao_verdadeira: bool,
        tema: str,
        dificuldade: NivelDificuldade,
    ) -> None:
        if not isinstance(afirmacao_verdadeira, bool):
            raise TypeError("A afirmação deve ser marcada como verdadeira (True) ou falsa (False).")
        super().__init__(enunciado, tema, dificuldade)
        self._afirmacao_verdadeira = afirmacao_verdadeira

    @property
    def afirmacao_verdadeira(self) -> bool:
        """Indica se a afirmação do enunciado é verdadeira."""
        return self._afirmacao_verdadeira

    @property
    def opcoes(self) -> list[str]:
        return list(self._OPCOES)

    def corrigir(self, indice_opcao: int) -> bool:
        return (
            isinstance(indice_opcao, int)
            and not isinstance(indice_opcao, bool)
            and indice_opcao in (0, 1)
            and indice_opcao == (0 if self._afirmacao_verdadeira else 1)
        )
