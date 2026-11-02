"""Interface de terminal do Sistema de Quiz Educacional."""

from __future__ import annotations

import json
from pathlib import Path
from time import monotonic

from models import (
    NivelDificuldade,
    Pergunta,
    PerguntaMultiplaEscolha,
    PerguntaVerdadeiroFalso,
    Quiz,
    QuizTematico,
    Usuario,
)
from persistencia import carregar_dados, salvar_dados
from relatorios import gerar_relatorio

ARQUIVO_DADOS = Path(__file__).with_name("dados.json")


class EntradaEncerrada(Exception):
    """Sinaliza o fim da entrada interativa."""


def ler_texto(mensagem: str, *, permitir_vazio: bool = False) -> str:
    """Lê texto obrigatório, tratando entradas vazias sem encerrar o programa."""
    while True:
        try:
            valor = input(mensagem).strip()
        except EOFError as erro:
            raise EntradaEncerrada from erro
        if valor or permitir_vazio:
            return valor
        print("Este campo é obrigatório.")


def ler_inteiro(
    mensagem: str,
    minimo: int,
    maximo: int | None = None,
) -> int:
    """Lê um inteiro dentro do intervalo informado."""
    while True:
        valor = ler_texto(mensagem)
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            limite = f" e no máximo {maximo}" if maximo is not None else ""
            print(f"Digite um valor entre {minimo}{limite}.")
            continue
        return numero


def criar_pergunta() -> Pergunta:
    """Coleta uma pergunta e valida seus dados antes de criá-la."""
    print("Tipo: 1. Múltipla escolha  2. Verdadeiro/Falso")
    tipo = ler_inteiro("Escolha: ", 1, 2)
    enunciado = ler_texto("Enunciado: ")
    tema = ler_texto("Tema: ")
    print("Dificuldade: 1. Fácil  2. Médio  3. Difícil")
    opcao_dificuldade = ler_inteiro("Escolha: ", 1, 3)
    dificuldade = {
        1: NivelDificuldade.FACIL,
        2: NivelDificuldade.MEDIO,
        3: NivelDificuldade.DIFICIL,
    }[opcao_dificuldade]

    if tipo == 2:
        print("A afirmação é: 1. Verdadeira  2. Falsa")
        verdadeira = ler_inteiro("Escolha: ", 1, 2) == 1
        return PerguntaVerdadeiroFalso(enunciado, verdadeira, tema, dificuldade)

    quantidade = ler_inteiro("Quantidade de alternativas (3 a 5): ", 3, 5)
    alternativas = [
        ler_texto(f"Alternativa {indice}: ")
        for indice in range(1, quantidade + 1)
    ]
    indice_correto = ler_inteiro("Número da alternativa correta: ", 1, quantidade) - 1

    return PerguntaMultiplaEscolha(
        enunciado, alternativas, indice_correto, tema, dificuldade
    )


def criar_quiz(quizzes: list[Quiz]) -> None:
    """Cadastra um quiz com uma ou mais perguntas."""
    titulo = ler_texto("Título do quiz: ")
    print("Tipo de quiz: 1. Geral  2. Temático")
    tipo_quiz = ler_inteiro("Escolha: ", 1, 2)
    tema_quiz = ler_texto("Tema do quiz: ") if tipo_quiz == 2 else None
    limite_tentativas = ler_inteiro("Limite de tentativas por usuário: ", 1)
    texto_tempo = ler_texto(
        "Tempo limite em minutos (vazio para sem limite): ", permitir_vazio=True
    )
    tempo_limite = None
    if texto_tempo:
        try:
            tempo_limite = int(texto_tempo)
        except ValueError:
            print("O tempo limite deve ser um número inteiro de minutos.")
            return
        if tempo_limite < 1:
            print("O tempo limite deve ser positivo.")
            return

    if tema_quiz is None:
        quiz = Quiz(
            titulo,
            limite_tentativas=limite_tentativas,
            tempo_limite_minutos=tempo_limite,
        )
    else:
        quiz = QuizTematico(
            titulo,
            tema_quiz,
            limite_tentativas=limite_tentativas,
            tempo_limite_minutos=tempo_limite,
        )
    while True:
        try:
            quiz.adicionar_pergunta(criar_pergunta())
        except (TypeError, ValueError) as erro:
            print(f"Não foi possível cadastrar a pergunta: {erro}")
            continue
        if ler_texto("Adicionar outra pergunta? (s/N): ").lower() != "s":
            break

    quizzes.append(quiz)
    print(f'Quiz "{quiz.titulo}" cadastrado com {len(quiz)} pergunta(s).')
    if quiz.tempo_limite_minutos is not None:
        print(
            "O tempo limite fica registrado no quiz; esta versão não possui "
            "cronômetro nem encerramento automático por tempo."
        )


def listar_quizzes(quizzes: list[Quiz]) -> None:
    """Mostra os quizzes cadastrados e suas configurações."""
    if not quizzes:
        print("Nenhum quiz cadastrado.")
        return
    print("\nQUIZZES DISPONÍVEIS")
    for indice, quiz in enumerate(quizzes, start=1):
        tempo = (
            f"{quiz.tempo_limite_minutos} min (informativo)"
            if quiz.tempo_limite_minutos is not None
            else "sem limite configurado"
        )
        print(
            f"{indice}. {quiz.titulo} — {len(quiz)} pergunta(s), "
            f"até {quiz.limite_tentativas} tentativa(s), tempo: {tempo}"
            + (f", tema: {quiz.tema}" if isinstance(quiz, QuizTematico) else "")
        )


def obter_usuario(usuarios: list[Usuario]) -> tuple[Usuario, bool]:
    """Localiza um usuário pelo conjunto de identificação ou coleta seu cadastro."""
    nome = ler_texto("Nome: ")
    email = ler_texto("E-mail: ")
    matricula_ou_id = ler_texto("Matrícula ou ID: ")
    for usuario in usuarios:
        if (
            usuario.nome == nome
            and usuario.email == email
            and usuario.matricula_ou_id == matricula_ou_id
        ):
            return usuario, False
    return Usuario(nome, email, matricula_ou_id), True


def cadastrar_usuario(usuarios: list[Usuario]) -> None:
    """Cadastra um usuário sem exigir que ele inicie um quiz."""
    usuario, novo_usuario = obter_usuario(usuarios)
    if not novo_usuario:
        print(f"O usuário {usuario.nome} já está cadastrado.")
        return
    usuarios.append(usuario)
    print(f"Usuário {usuario.nome} cadastrado.")


def listar_usuarios(usuarios: list[Usuario]) -> None:
    """Mostra os usuários e a quantidade de tentativas de cada um."""
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("\nUSUÁRIOS CADASTRADOS")
    for indice, usuario in enumerate(usuarios, start=1):
        print(
            f"{indice}. {usuario.nome} <{usuario.email}> "
            f"({usuario.matricula_ou_id}) — {len(usuario.tentativas)} tentativa(s)"
        )


def iniciar_quiz(usuarios: list[Usuario], quizzes: list[Quiz]) -> None:
    """Executa uma tentativa interativa de um quiz."""
    if not quizzes:
        print("Cadastre um quiz antes de iniciar uma tentativa.")
        return
    listar_quizzes(quizzes)
    indice = ler_inteiro("Número do quiz (0 para voltar): ", 0, len(quizzes))
    if indice == 0:
        return
    quiz = quizzes[indice - 1]

    usuario, novo_usuario = obter_usuario(usuarios)
    try:
        tentativa = usuario.iniciar_quiz(quiz)
    except (TypeError, ValueError) as erro:
        print(f"Não foi possível iniciar a tentativa: {erro}")
        return
    if novo_usuario:
        usuarios.append(usuario)

    inicio = monotonic()
    print(f"\nQuiz: {quiz.titulo}")
    for numero, pergunta in enumerate(quiz, start=1):
        print(f"\n{numero}/{len(quiz)}. {pergunta.enunciado}")
        for indice_opcao, opcao in enumerate(pergunta.opcoes, start=1):
            print(f"  {indice_opcao}. {opcao}")
        resposta = ler_inteiro("Sua resposta: ", 1, pergunta.numero_opcoes)
        tentativa.registrar_resposta(resposta - 1)

    tentativa.finalizar(tempo_total=monotonic() - inicio)
    print(
        f"Tentativa concluída: {tentativa.pontuacao_obtida}/{len(quiz)} ponto(s), "
        f"{tentativa.taxa_acertos:.0f}% de acertos."
    )


def _salvar_estado(usuarios: list[Usuario], quizzes: list[Quiz], caminho: Path) -> bool:
    try:
        salvar_dados(usuarios, quizzes, caminho)
    except (OSError, TypeError, ValueError) as erro:
        print(f"Não foi possível salvar os dados: {erro}")
        return False
    return True


def executar_cli(caminho_dados: str | Path = ARQUIVO_DADOS) -> None:
    """Carrega os dados e inicia o menu principal."""
    caminho = Path(caminho_dados)
    try:
        if caminho.exists():
            usuarios, quizzes = carregar_dados(caminho)
        else:
            usuarios, quizzes = [], []
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ) as erro:
        print(f"Não foi possível carregar {caminho}: {erro}")
        print("O arquivo foi preservado. Corrija-o ou escolha outro caminho de dados.")
        return

    print("Sistema de Quiz Educacional")
    try:
        while True:
            print(
                "\n1. Listar quizzes\n"
                "2. Cadastrar quiz\n"
                "3. Cadastrar usuário\n"
                "4. Responder a um quiz\n"
                "5. Consultar relatórios\n"
                "6. Listar usuários\n"
                "7. Salvar e sair"
            )
            opcao = ler_texto("Opção: ")
            if opcao == "1":
                listar_quizzes(quizzes)
            elif opcao == "2":
                criar_quiz(quizzes)
            elif opcao == "3":
                cadastrar_usuario(usuarios)
            elif opcao == "4":
                iniciar_quiz(usuarios, quizzes)
            elif opcao == "5":
                print(gerar_relatorio(usuarios))
            elif opcao == "6":
                listar_usuarios(usuarios)
            elif opcao == "7":
                if _salvar_estado(usuarios, quizzes, caminho):
                    print("Dados salvos. Até logo!")
                else:
                    print("Saindo sem confirmar que os dados foram salvos.")
                return
            else:
                print("Opção inválida. Escolha um número de 1 a 7.")
            _salvar_estado(usuarios, quizzes, caminho)
    except (EntradaEncerrada, KeyboardInterrupt):
        print("\nEntrada encerrada. Salvando o estado atual.")
        _salvar_estado(usuarios, quizzes, caminho)


if __name__ == "__main__":
    executar_cli()
