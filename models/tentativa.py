"""Definição inicial de tentativa."""


class Tentativa:
    """Registra a execução de um quiz por determinado usuário."""

    respostas: list[int]
    pontuacao_obtida: int
    tempo_total: float
    taxa_acertos: float
    concluida: bool