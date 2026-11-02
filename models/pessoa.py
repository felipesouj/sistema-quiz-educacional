"""Dados comuns de uma pessoa no sistema."""


class Pessoa:
    """Classe base com os dados de identificação compartilhados."""

    _nome: str
    _email: str

    def __init__(self, nome: str, email: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome não pode ficar vazio.")
        if not isinstance(email, str) or not email.strip():
            raise ValueError("O e-mail não pode ficar vazio.")

        self._nome = nome
        self._email = email

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    def __str__(self) -> str:
        return f"{self._nome} <{self._email}>"
