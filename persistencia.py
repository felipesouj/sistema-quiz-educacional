"""Salvamento e carregamento simples dos dados em JSON."""

import json
from pathlib import Path
from typing import Iterable

from models import NivelDificuldade, Pergunta, Quiz, Usuario


def salvar_dados(
    usuarios: Iterable[Usuario],
    quizzes: Iterable[Quiz],
    caminho: str | Path = "dados.json",
) -> None:
    """Salva quizzes, usuários e histórico em um arquivo JSON."""
    lista_usuarios = list(usuarios)
    lista_quizzes = list(quizzes)
    indices_quizzes = {id(quiz): indice for indice, quiz in enumerate(lista_quizzes)}

    dados = {
        "quizzes": [
            {
                "titulo": quiz.titulo,
                "limite_tentativas": quiz.limite_tentativas,
                "tempo_limite_minutos": quiz.tempo_limite_minutos,
                "perguntas": [
                    {
                        "enunciado": pergunta.enunciado,
                        "alternativas": pergunta.alternativas,
                        "indice_resposta_correta": pergunta.indice_resposta_correta,
                        "tema": pergunta.tema,
                        "dificuldade": pergunta.dificuldade.name,
                    }
                    for pergunta in quiz
                ],
            }
            for quiz in lista_quizzes
        ],
        "usuarios": [],
    }

    for usuario in lista_usuarios:
        tentativas = []
        for tentativa in usuario.consultar_historico():
            if id(tentativa.quiz) not in indices_quizzes:
                raise ValueError("Inclua na lista de quizzes todos os quizzes tentados.")
            tentativas.append(
                {
                    "quiz": indices_quizzes[id(tentativa.quiz)],
                    "respostas": tentativa.respostas,
                    "tempo_total": tentativa.tempo_total,
                    "concluida": tentativa.concluida,
                }
            )
        dados["usuarios"].append(
            {
                "nome": usuario.nome,
                "email": usuario.email,
                "matricula_ou_id": usuario.matricula_ou_id,
                "tentativas": tentativas,
            }
        )

    with Path(caminho).open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def carregar_dados(caminho: str | Path = "dados.json") -> tuple[list[Usuario], list[Quiz]]:
    """Carrega o JSON e reconstrói os objetos e suas relações."""
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    quizzes = []
    for dados_quiz in dados["quizzes"]:
        perguntas = [
            Pergunta(
                enunciado=dados_pergunta["enunciado"],
                alternativas=dados_pergunta["alternativas"],
                indice_resposta_correta=dados_pergunta["indice_resposta_correta"],
                tema=dados_pergunta["tema"],
                dificuldade=NivelDificuldade[dados_pergunta["dificuldade"]],
            )
            for dados_pergunta in dados_quiz["perguntas"]
        ]
        quizzes.append(
            Quiz(
                titulo=dados_quiz["titulo"],
                perguntas=perguntas,
                limite_tentativas=dados_quiz["limite_tentativas"],
                tempo_limite_minutos=dados_quiz["tempo_limite_minutos"],
            )
        )

    usuarios = []
    for dados_usuario in dados["usuarios"]:
        usuario = Usuario(
            nome=dados_usuario["nome"],
            email=dados_usuario["email"],
            matricula_ou_id=dados_usuario["matricula_ou_id"],
        )
        for dados_tentativa in dados_usuario["tentativas"]:
            tentativa = usuario.iniciar_quiz(quizzes[dados_tentativa["quiz"]])
            for resposta in dados_tentativa["respostas"]:
                tentativa.registrar_resposta(resposta)
            if dados_tentativa["concluida"]:
                tentativa.finalizar(dados_tentativa["tempo_total"])
        usuarios.append(usuario)

    return usuarios, quizzes
