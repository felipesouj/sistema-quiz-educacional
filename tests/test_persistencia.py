import json
import tempfile
import unittest
from pathlib import Path

from models import (
    NivelDificuldade,
    PerguntaMultiplaEscolha,
    PerguntaVerdadeiroFalso,
    Quiz,
    QuizTematico,
    Usuario,
)
from persistencia import carregar_dados, salvar_dados


class PersistenciaTests(unittest.TestCase):
    def test_round_trip_preserva_quizzes_usuarios_e_tentativas(self) -> None:
        pergunta = PerguntaMultiplaEscolha(
            "Capital do Brasil?",
            ["Brasília", "São Paulo", "Rio"],
            0,
            "Geografia",
            NivelDificuldade.FACIL,
        )
        vf = PerguntaVerdadeiroFalso("O Sol é um planeta?", False, "Astronomia", NivelDificuldade.FACIL)
        quiz = Quiz("Geografia", [pergunta, vf], limite_tentativas=3)
        quiz_tematico = QuizTematico("Capitais", "Geografia", [pergunta], limite_tentativas=2)
        usuario = Usuario("Ana", "ana@example.com", "A001")
        concluida = usuario.iniciar_quiz(quiz)
        concluida.registrar_resposta(0)
        concluida.registrar_resposta(1)
        concluida.finalizar(tempo_total=9.25)
        em_andamento = usuario.iniciar_quiz(quiz)
        em_andamento.registrar_resposta(1)

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            salvar_dados([usuario], [quiz, quiz_tematico], caminho)
            usuarios_carregados, quizzes_carregados = carregar_dados(caminho)

        self.assertEqual(len(quizzes_carregados), 2)
        self.assertEqual(quizzes_carregados[0].titulo, "Geografia")
        tentativas = usuarios_carregados[0].consultar_historico()
        self.assertEqual(len(tentativas), 2)
        self.assertTrue(tentativas[0].concluida)
        self.assertEqual(tentativas[0].pontuacao_obtida, 2)
        self.assertIs(tentativas[0].usuario, usuarios_carregados[0])
        self.assertIs(tentativas[0].quiz, quizzes_carregados[0])
        self.assertIsInstance(quizzes_carregados[0].perguntas[1], PerguntaVerdadeiroFalso)
        self.assertIsInstance(quizzes_carregados[1], QuizTematico)
        self.assertIs(quizzes_carregados[0].perguntas[0], quizzes_carregados[1].perguntas[0])
        self.assertEqual(quizzes_carregados[1].tema, "Geografia")
        self.assertEqual(tentativas[0].tempo_total, 9.25)
        self.assertFalse(tentativas[1].concluida)
        self.assertEqual(tentativas[1].respostas, [1])

    def test_carrega_formato_inline_da_entrega_anterior(self) -> None:
        dados_antigos = {
            "quizzes": [
                {
                    "titulo": "Geografia",
                    "limite_tentativas": 2,
                    "tempo_limite_minutos": None,
                    "perguntas": [
                        {
                            "enunciado": "Capital do Brasil?",
                            "alternativas": ["Brasília", "São Paulo", "Rio"],
                            "indice_resposta_correta": 0,
                            "tema": "Geografia",
                            "dificuldade": "FACIL",
                        }
                    ],
                }
            ],
            "usuarios": [],
        }
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            caminho.write_text(json.dumps(dados_antigos), encoding="utf-8")
            usuarios, quizzes = carregar_dados(caminho)

        self.assertEqual(usuarios, [])
        self.assertEqual(quizzes[0].perguntas[0].enunciado, "Capital do Brasil?")

    def test_carrega_formato_com_perguntas_referenciadas(self) -> None:
        dados_referenciados = {
            "perguntas": [
                {
                    "enunciado": "Capital do Brasil?",
                    "alternativas": ["Brasília", "São Paulo", "Rio"],
                    "indice_resposta_correta": 0,
                    "tema": "Geografia",
                    "dificuldade": "FACIL",
                }
            ],
            "quizzes": [
                {
                    "tipo": "simples",
                    "titulo": "Geografia",
                    "limite_tentativas": 2,
                    "tempo_limite_minutos": None,
                    "perguntas": [0],
                }
            ],
            "usuarios": [
                {
                    "nome": "Ana",
                    "email": "ana@example.com",
                    "matricula_ou_id": "A001",
                    "tentativas": [
                        {
                            "quiz": 0,
                            "respostas": [0],
                            "tempo_total": 2.0,
                            "concluida": True,
                        }
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.json"
            caminho.write_text(json.dumps(dados_referenciados), encoding="utf-8")
            usuarios, quizzes = carregar_dados(caminho)

        self.assertTrue(usuarios[0].tentativas[0].concluida)
        self.assertEqual(usuarios[0].tentativas[0].pontuacao_obtida, 1)
        self.assertIs(usuarios[0].tentativas[0].quiz, quizzes[0])


if __name__ == "__main__":
    unittest.main()
