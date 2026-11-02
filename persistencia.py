"""Salvamento e carregamento dos dados do quiz em JSON."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Iterable

from models import (
    NivelDificuldade,
    Pergunta,
    PerguntaMultiplaEscolha,
    PerguntaVerdadeiroFalso,
    Quiz,
    QuizTematico,
    Usuario,
)


def _pergunta_para_dict(pergunta: Pergunta) -> dict[str, object]:
    """Serializa uma pergunta conforme seu tipo concreto."""
    dados: dict[str, object] = {
        "tipo": pergunta.tipo,
        "enunciado": pergunta.enunciado,
        "tema": pergunta.tema,
        "dificuldade": pergunta.dificuldade.name,
    }
    if isinstance(pergunta, PerguntaMultiplaEscolha):
        dados["alternativas"] = pergunta.alternativas
        dados["indice_resposta_correta"] = pergunta.indice_resposta_correta
    elif isinstance(pergunta, PerguntaVerdadeiroFalso):
        dados["afirmacao_verdadeira"] = pergunta.afirmacao_verdadeira
    else:
        raise TypeError(f"Tipo de pergunta sem serialização: {type(pergunta).__name__}")
    return dados


def _pergunta_de_dict(dados: dict[str, object]) -> Pergunta:
    """Reconstrói perguntas atuais e perguntas de múltipla escolha antigas."""
    try:
        dificuldade = NivelDificuldade[str(dados["dificuldade"])]
        tipo = dados.get("tipo", PerguntaMultiplaEscolha.tipo)
        enunciado = dados["enunciado"]
        tema = dados["tema"]
    except (KeyError, TypeError) as erro:
        raise ValueError("Dados de pergunta incompletos ou inválidos.") from erro

    if tipo == PerguntaVerdadeiroFalso.tipo:
        if "afirmacao_verdadeira" not in dados:
            raise ValueError("Pergunta verdadeiro/falso sem gabarito.")
        return PerguntaVerdadeiroFalso(
            enunciado,  # type: ignore[arg-type]
            dados["afirmacao_verdadeira"],  # type: ignore[arg-type]
            tema,  # type: ignore[arg-type]
            dificuldade,
        )
    if tipo == PerguntaMultiplaEscolha.tipo:
        try:
            alternativas = dados["alternativas"]
            indice_correto = dados["indice_resposta_correta"]
        except KeyError as erro:
            raise ValueError("Pergunta de múltipla escolha sem alternativas ou gabarito.") from erro
        return PerguntaMultiplaEscolha(
            enunciado,  # type: ignore[arg-type]
            alternativas,  # type: ignore[arg-type]
            indice_correto,  # type: ignore[arg-type]
            tema,  # type: ignore[arg-type]
            dificuldade,
        )
    raise ValueError(f"Tipo de pergunta desconhecido: {tipo}")


def _quiz_para_dict(quiz: Quiz, indices_perguntas: list[int]) -> dict[str, object]:
    dados: dict[str, object] = {
        "tipo": "tematico" if isinstance(quiz, QuizTematico) else "simples",
        "titulo": quiz.titulo,
        "limite_tentativas": quiz.limite_tentativas,
        "tempo_limite_minutos": quiz.tempo_limite_minutos,
        "perguntas": indices_perguntas,
    }
    if isinstance(quiz, QuizTematico):
        dados["tema"] = quiz.tema
    return dados


def salvar_dados(
    usuarios: Iterable[Usuario],
    quizzes: Iterable[Quiz],
    caminho: str | Path = "dados.json",
) -> None:
    """Salva quizzes, perguntas e tentativas com referências preservadas.

    A escrita usa um arquivo temporário no mesmo diretório e substituição
    atômica, para não deixar o JSON pela metade se a gravação for interrompida.
    """
    lista_usuarios = list(usuarios)
    lista_quizzes = list(quizzes)
    if any(not isinstance(usuario, Usuario) for usuario in lista_usuarios):
        raise TypeError("A persistência aceita apenas objetos Usuario.")
    if any(not isinstance(quiz, Quiz) for quiz in lista_quizzes):
        raise TypeError("A persistência aceita apenas objetos Quiz.")

    indices_perguntas: dict[int, int] = {}
    perguntas: list[dict[str, object]] = []
    quizzes_serializados = []
    indices_quizzes = {id(quiz): indice for indice, quiz in enumerate(lista_quizzes)}

    for quiz in lista_quizzes:
        indices_do_quiz = []
        for pergunta in quiz:
            chave = id(pergunta)
            if chave not in indices_perguntas:
                indices_perguntas[chave] = len(perguntas)
                perguntas.append(_pergunta_para_dict(pergunta))
            indices_do_quiz.append(indices_perguntas[chave])
        quizzes_serializados.append(_quiz_para_dict(quiz, indices_do_quiz))

    usuarios_serializados = []
    for usuario in lista_usuarios:
        tentativas = []
        for tentativa in usuario.consultar_historico():
            indice_quiz = indices_quizzes.get(id(tentativa.quiz))
            if indice_quiz is None:
                raise ValueError("Inclua na lista todos os quizzes tentados pelos usuários.")
            tentativas.append(
                {
                    "quiz": indice_quiz,
                    "respostas": tentativa.respostas,
                    "tempo_total": tentativa.tempo_total,
                    "concluida": tentativa.concluida,
                }
            )
        usuarios_serializados.append(
            {
                "nome": usuario.nome,
                "email": usuario.email,
                "matricula_ou_id": usuario.matricula_ou_id,
                "tentativas": tentativas,
            }
        )

    dados = {
        "versao": 2,
        "perguntas": perguntas,
        "quizzes": quizzes_serializados,
        "usuarios": usuarios_serializados,
    }

    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    nome_temporario: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destino.parent,
            prefix=f".{destino.name}.",
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            nome_temporario = arquivo.name
            json.dump(dados, arquivo, ensure_ascii=False, indent=2, allow_nan=False)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        Path(nome_temporario).replace(destino)
    finally:
        if nome_temporario is not None:
            Path(nome_temporario).unlink(missing_ok=True)


def _ler_lista(dados: dict[str, object], chave: str) -> list[object]:
    valor = dados.get(chave)
    if not isinstance(valor, list):
        raise ValueError(f"O campo '{chave}' deve ser uma lista.")
    return valor


def _construir_quiz(
    dados_quiz: dict[str, object],
    perguntas: list[Pergunta],
) -> Quiz:
    try:
        titulo = dados_quiz["titulo"]
        limite = dados_quiz.get("limite_tentativas", 1)
        tempo = dados_quiz.get("tempo_limite_minutos")
        tipo = dados_quiz.get("tipo", "simples")
    except (KeyError, TypeError) as erro:
        raise ValueError("Dados de quiz incompletos ou inválidos.") from erro

    if tipo == "tematico":
        try:
            tema = dados_quiz["tema"]
        except KeyError as erro:
            raise ValueError("Quiz temático sem tema.") from erro
        return QuizTematico(
            titulo,  # type: ignore[arg-type]
            tema,  # type: ignore[arg-type]
            perguntas,
            limite,  # type: ignore[arg-type]
            tempo,  # type: ignore[arg-type]
        )
    if tipo not in ("simples", None):
        raise ValueError(f"Tipo de quiz desconhecido: {tipo}")
    return Quiz(
        titulo,  # type: ignore[arg-type]
        perguntas,
        limite,  # type: ignore[arg-type]
        tempo,  # type: ignore[arg-type]
    )


def carregar_dados(caminho: str | Path = "dados.json") -> tuple[list[Usuario], list[Quiz]]:
    """Carrega o formato atual e os formatos inline das entregas anteriores."""
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, dict):
        raise ValueError("A raiz do arquivo de dados deve ser um objeto JSON.")

    quizzes_brutos = _ler_lista(dados, "quizzes")
    perguntas_globais = dados.get("perguntas")
    quizzes: list[Quiz] = []

    if "perguntas" in dados:
        if not isinstance(perguntas_globais, list):
            raise ValueError("O campo 'perguntas' deve ser uma lista.")
        perguntas = []
        for item in perguntas_globais:
            if not isinstance(item, dict):
                raise ValueError("Cada pergunta persistida deve ser um objeto JSON.")
            perguntas.append(_pergunta_de_dict(item))

        for item in quizzes_brutos:
            if not isinstance(item, dict):
                raise ValueError("Cada quiz persistido deve ser um objeto JSON.")
            indices = item.get("perguntas")
            if not isinstance(indices, list):
                raise ValueError("As referências de perguntas do quiz devem ser uma lista.")
            perguntas_do_quiz = []
            for indice in indices:
                if (
                    not isinstance(indice, int)
                    or isinstance(indice, bool)
                    or not 0 <= indice < len(perguntas)
                ):
                    raise ValueError("Referência de pergunta inválida no quiz.")
                perguntas_do_quiz.append(perguntas[indice])
            quizzes.append(
                _construir_quiz(item, perguntas_do_quiz)
            )
    else:
        for item in quizzes_brutos:
            if not isinstance(item, dict):
                raise ValueError("Cada quiz persistido deve ser um objeto JSON.")
            dados_perguntas = item.get("perguntas")
            if not isinstance(dados_perguntas, list):
                raise ValueError("As perguntas do quiz devem ser uma lista.")
            perguntas_do_quiz = []
            for dados_pergunta in dados_perguntas:
                if not isinstance(dados_pergunta, dict):
                    raise ValueError("Cada pergunta persistida deve ser um objeto JSON.")
                perguntas_do_quiz.append(_pergunta_de_dict(dados_pergunta))
            quizzes.append(
                _construir_quiz(item, perguntas_do_quiz)
            )

    usuarios_brutos = _ler_lista(dados, "usuarios")
    usuarios: list[Usuario] = []
    for dados_usuario in usuarios_brutos:
        if not isinstance(dados_usuario, dict):
            raise ValueError("Cada usuário persistido deve ser um objeto JSON.")
        try:
            usuario = Usuario(
                nome=dados_usuario["nome"],  # type: ignore[arg-type]
                email=dados_usuario["email"],  # type: ignore[arg-type]
                matricula_ou_id=dados_usuario["matricula_ou_id"],  # type: ignore[arg-type]
            )
        except KeyError as erro:
            raise ValueError("Dados de usuário incompletos.") from erro

        tentativas = dados_usuario.get("tentativas", [])
        if not isinstance(tentativas, list):
            raise ValueError("O histórico de tentativas deve ser uma lista.")
        for dados_tentativa in tentativas:
            if not isinstance(dados_tentativa, dict):
                raise ValueError("Cada tentativa persistida deve ser um objeto JSON.")
            indice_quiz = dados_tentativa.get("quiz")
            if (
                not isinstance(indice_quiz, int)
                or isinstance(indice_quiz, bool)
                or not 0 <= indice_quiz < len(quizzes)
            ):
                raise ValueError("Referência de quiz inválida na tentativa.")
            respostas = dados_tentativa.get("respostas", [])
            if not isinstance(respostas, list):
                raise ValueError("As respostas da tentativa devem ser uma lista.")

            tentativa = usuario.iniciar_quiz(quizzes[indice_quiz])
            for resposta in respostas:
                tentativa.registrar_resposta(resposta)  # type: ignore[arg-type]
            if dados_tentativa.get("concluida", False):
                tentativa.finalizar(dados_tentativa.get("tempo_total", 0.0))  # type: ignore[arg-type]
        usuarios.append(usuario)

    return usuarios, quizzes
