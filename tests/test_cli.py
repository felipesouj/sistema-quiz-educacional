import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from main import executar_cli
from models import QuizTematico
from persistencia import carregar_dados


class CliTests(unittest.TestCase):
    def test_cadastra_lista_responde_e_persiste_um_quiz(self) -> None:
        entradas = [
            "2",  # cadastrar
            "Geografia",
            "1",  # quiz geral
            "2",  # limite de tentativas
            "",  # sem tempo limite
            "1",  # tipo: múltipla escolha
            "Capital do Brasil?",
            "Geografia",
            "1",  # fácil
            "3",
            "Brasília",
            "São Paulo",
            "Rio de Janeiro",
            "1",  # resposta correta
            "s",  # adicionar outra pergunta
            "2",  # tipo: verdadeiro/falso
            "O Sol é um planeta?",
            "Astronomia",
            "1",  # fácil
            "2",  # afirmação falsa
            "n",  # não adicionar outra pergunta
            "1",  # listar
            "4",  # responder
            "1",  # primeiro quiz
            "Ana Silva",
            "ana@example.com",
            "A001",
            "1",  # resposta 1
            "2",  # resposta 2 (Falso)
            "5",  # relatório
            "7",  # salvar e sair
        ]
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            saida = io.StringIO()
            with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
                executar_cli(caminho)

            usuarios, quizzes = carregar_dados(caminho)

        self.assertEqual(len(quizzes), 1)
        self.assertEqual(quizzes[0].titulo, "Geografia")
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].tentativas[0].pontuacao_obtida, 2)
        self.assertIn('Quiz "Geografia" cadastrado', saida.getvalue())
        self.assertIn("100% de acertos", saida.getvalue())
        self.assertIn("RELATÓRIO DE DESEMPENHO", saida.getvalue())

    def test_cadastra_quiz_tematico(self) -> None:
        entradas = [
            "2",
            "Geografia",
            "2",  # quiz temático
            "Geografia",
            "1",  # limite de tentativas
            "",  # sem tempo limite
            "1",  # múltipla escolha
            "Capital do Brasil?",
            "Geografia",
            "1",  # fácil
            "3",
            "Brasília",
            "São Paulo",
            "Rio de Janeiro",
            "1",
            "n",
            "1",  # listar quizzes
            "7",
        ]
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            saida = io.StringIO()
            with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
                executar_cli(caminho)

            _, quizzes = carregar_dados(caminho)

        self.assertIsInstance(quizzes[0], QuizTematico)
        self.assertEqual(quizzes[0].tema, "Geografia")
        self.assertIn("tema: Geografia", saida.getvalue())

    def test_cadastra_e_lista_usuario_sem_iniciar_quiz(self) -> None:
        entradas = ["3", "Bia", "bia@example.com", "B002", "6", "7"]
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            saida = io.StringIO()
            with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
                executar_cli(caminho)
            usuarios, _ = carregar_dados(caminho)

        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nome, "Bia")
        self.assertIn("Bia <bia@example.com>", saida.getvalue())

    def test_entrada_invalida_nao_impede_retorno_ao_menu(self) -> None:
        saida = io.StringIO()
        with tempfile.TemporaryDirectory() as pasta:
            with patch("builtins.input", side_effect=["", "inválida", "7"]):
                with redirect_stdout(saida):
                    executar_cli(Path(pasta) / "dados.json")

        self.assertIn("Este campo é obrigatório", saida.getvalue())
        self.assertIn("Opção inválida", saida.getvalue())

    def test_json_invalido_e_preservado_sem_solicitar_entrada(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            conteudo = b"{ arquivo incompleto"
            caminho.write_bytes(conteudo)
            saida = io.StringIO()
            with redirect_stdout(saida):
                executar_cli(caminho)

            self.assertEqual(caminho.read_bytes(), conteudo)
        self.assertIn("O arquivo foi preservado", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
