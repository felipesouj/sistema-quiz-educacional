import math
import unittest

from models import (
    NivelDificuldade,
    Pergunta,
    PerguntaMultiplaEscolha,
    PerguntaVerdadeiroFalso,
    Pessoa,
    Quiz,
    QuizTematico,
    Usuario,
)


def criar_pergunta(enunciado: str = "Capital do Brasil?") -> Pergunta:
    return PerguntaMultiplaEscolha(
        enunciado,
        ["Brasília", "São Paulo", "Rio de Janeiro"],
        0,
        "Geografia",
        NivelDificuldade.FACIL,
    )


class PerguntaTests(unittest.TestCase):
    def test_rejeita_campos_textuais_obrigatorios_vazios(self) -> None:
        with self.assertRaises(ValueError):
            Pessoa("", "ana@example.com")
        with self.assertRaises(ValueError):
            Usuario("Ana", "", "A001")
        with self.assertRaises(ValueError):
            Usuario("Ana", "ana@example.com", " ")
        with self.assertRaises(ValueError):
            Quiz(" ")
        with self.assertRaises(ValueError):
            PerguntaMultiplaEscolha("", ["a", "b", "c"], 0, "Tema", NivelDificuldade.FACIL)
        with self.assertRaises(ValueError):
            PerguntaMultiplaEscolha("Pergunta?", ["a", "b", "c"], 0, " ", NivelDificuldade.FACIL)

    def test_rejeita_quantidade_invalida_de_alternativas(self) -> None:
        with self.assertRaisesRegex(ValueError, "entre 3 e 5"):
            PerguntaMultiplaEscolha("Pergunta?", ["sim", "não"], 0, "Tema", NivelDificuldade.FACIL)
        with self.assertRaisesRegex(ValueError, "entre 3 e 5"):
            PerguntaMultiplaEscolha("Pergunta?", ["sim", " ", "não"], 0, "Tema", NivelDificuldade.FACIL)

    def test_dificuldade_deve_ser_um_valor_do_enum(self) -> None:
        with self.assertRaisesRegex(TypeError, "NivelDificuldade"):
            PerguntaMultiplaEscolha("Pergunta?", ["a", "b", "c"], 0, "Tema", "FACIL")

    def test_rejeita_indice_correto_fora_da_lista_e_booleano(self) -> None:
        for indice in (3, -1, True):
            with self.subTest(indice=indice):
                with self.assertRaisesRegex(ValueError, "índice"):
                    PerguntaMultiplaEscolha(
                        "Pergunta?",
                        ["a", "b", "c"],
                        indice,
                        "Tema",
                        NivelDificuldade.FACIL,
                    )

    def test_lista_de_alternativas_exposta_e_uma_copia(self) -> None:
        pergunta = criar_pergunta()
        alternativas = pergunta.alternativas
        alternativas.clear()
        self.assertEqual(len(pergunta.alternativas), 3)


class PolimorfismoTests(unittest.TestCase):
    def test_pergunta_base_e_abstrata(self) -> None:
        with self.assertRaises(TypeError):
            Pergunta("Pergunta?", "Tema", NivelDificuldade.FACIL)  # type: ignore[abstract]

    def test_tipos_diferentes_respondem_a_mesma_mensagem(self) -> None:
        multipla = criar_pergunta()
        verdadeiro_falso = PerguntaVerdadeiroFalso(
            "Brasília é a capital do Brasil?", True, "Geografia", NivelDificuldade.FACIL
        )
        for pergunta in (multipla, verdadeiro_falso):
            self.assertIsInstance(pergunta, Pergunta)
            self.assertTrue(pergunta.corrigir(0))
            self.assertFalse(pergunta.corrigir(1))
        self.assertEqual(multipla.numero_opcoes, 3)
        self.assertEqual(verdadeiro_falso.opcoes, ["Verdadeiro", "Falso"])

    def test_verdadeiro_falso_com_afirmacao_falsa_e_validacao(self) -> None:
        pergunta = PerguntaVerdadeiroFalso("O Sol é um planeta?", False, "Astronomia", NivelDificuldade.FACIL)
        self.assertTrue(pergunta.corrigir(1))
        with self.assertRaises(TypeError):
            PerguntaVerdadeiroFalso("?", "sim", "Tema", NivelDificuldade.FACIL)  # type: ignore[arg-type]

    def test_quiz_misto_e_pontuado_polimorficamente(self) -> None:
        quiz = Quiz(
            "Misto",
            [
                criar_pergunta(),
                PerguntaVerdadeiroFalso("O Sol é um planeta?", False, "Astronomia", NivelDificuldade.FACIL),
            ],
        )
        tentativa = Usuario("Ana", "ana@example.com", "A001").iniciar_quiz(quiz)
        tentativa.registrar_resposta(0)
        tentativa.registrar_resposta(1)
        tentativa.finalizar(1.0)
        self.assertEqual(tentativa.pontuacao_obtida, 2)
        with self.assertRaisesRegex(ValueError, "alternativa"):
            Usuario("Bia", "b@example.com", "B1").iniciar_quiz(quiz).registrar_resposta(3)

    def test_perguntas_iguais_tem_mesmo_hash(self) -> None:
        self.assertEqual(len({criar_pergunta(), criar_pergunta()}), 1)


class TentativaTests(unittest.TestCase):
    def test_inicia_responde_calcula_resultado_e_fecha(self) -> None:
        quiz = Quiz("Geografia", [criar_pergunta(), criar_pergunta("Maior oceano?")])
        usuario = Usuario("Ana", "ana@example.com", "A001")
        tentativa = usuario.iniciar_quiz(quiz)

        tentativa.registrar_resposta(0)
        tentativa.registrar_resposta(2)
        tentativa.finalizar(tempo_total=12.5)

        self.assertEqual(tentativa.pontuacao_obtida, 1)
        self.assertEqual(tentativa.taxa_acertos, 50.0)
        self.assertEqual(tentativa.tempo_total, 12.5)
        self.assertTrue(tentativa.concluida)
        self.assertEqual(usuario.consultar_historico(), [tentativa])

    def test_impede_resposta_invalida_extra_e_finalizacao_incompleta(self) -> None:
        quiz = Quiz("Geografia", [criar_pergunta()])
        tentativa = Usuario("Ana", "ana@example.com", "A001").iniciar_quiz(quiz)

        with self.assertRaisesRegex(ValueError, "alternativa"):
            tentativa.registrar_resposta(3)
        with self.assertRaisesRegex(ValueError, "todas as perguntas"):
            tentativa.finalizar()

        tentativa.registrar_resposta(0)
        with self.assertRaisesRegex(ValueError, "Todas as perguntas"):
            tentativa.registrar_resposta(0)
        tentativa.finalizar()
        with self.assertRaisesRegex(ValueError, "já foi concluída"):
            tentativa.finalizar()

    def test_rejeita_tempo_negativo_nao_finito_ou_booleano(self) -> None:
        for tempo in (-0.1, math.inf, -math.inf, math.nan, True, 10**400):
            with self.subTest(tempo=tempo):
                quiz = Quiz("Geografia", [criar_pergunta()])
                tentativa = Usuario("Ana", "ana@example.com", "A001").iniciar_quiz(quiz)
                tentativa.registrar_resposta(0)
                with self.assertRaisesRegex(ValueError, "número finito"):
                    tentativa.finalizar(tempo_total=tempo)


class HerancaTests(unittest.TestCase):
    def test_usuario_herda_de_pessoa_e_reutiliza_validacao(self) -> None:
        usuario = Usuario("Ana", "ana@example.com", "A001")
        self.assertIsInstance(usuario, Pessoa)
        self.assertEqual(usuario.nome, "Ana")
        self.assertEqual(str(usuario), "Ana (A001)")
        self.assertEqual(str(Pessoa("Bia", "b@example.com")), "Bia <b@example.com>")


class UsuarioEQuizTests(unittest.TestCase):
    def test_validacao_dos_limites_configurados_no_quiz(self) -> None:
        for limite in (0, -1, True, 1.5):
            with self.subTest(limite=limite):
                with self.assertRaises(ValueError):
                    Quiz("Geografia", limite_tentativas=limite)

        for tempo in (0, -1, True, 1.5):
            with self.subTest(tempo=tempo):
                with self.assertRaises(ValueError):
                    Quiz("Geografia", tempo_limite_minutos=tempo)

        quiz = Quiz("Geografia", tempo_limite_minutos=5)
        self.assertEqual(quiz.tempo_limite_minutos, 5)

    def test_nao_inicia_quiz_vazio_e_respeita_limite_de_tentativas(self) -> None:
        usuario = Usuario("Ana", "ana@example.com", "A001")
        with self.assertRaisesRegex(ValueError, "sem perguntas"):
            usuario.iniciar_quiz(Quiz("Vazio"))

        quiz = Quiz("Geografia", [criar_pergunta()], limite_tentativas=1)
        usuario.iniciar_quiz(quiz)
        with self.assertRaisesRegex(ValueError, "limite de tentativas"):
            usuario.iniciar_quiz(quiz)

    def test_quiz_tematico_so_aceita_perguntas_do_tema(self) -> None:
        pergunta = criar_pergunta()
        quiz = QuizTematico("Capitais", "Geografia", [pergunta])
        self.assertEqual(len(quiz), 1)
        with self.assertRaisesRegex(ValueError, "tema do quiz"):
            quiz.adicionar_pergunta(
                PerguntaVerdadeiroFalso(
                    "O Sol é um planeta?", False, "Astronomia", NivelDificuldade.FACIL
                )
            )

    def test_perguntas_do_quiz_ficam_estaveis_apos_inicio_de_tentativa(self) -> None:
        pergunta = criar_pergunta()
        quiz = Quiz("Geografia", [pergunta])
        Usuario("Ana", "ana@example.com", "A001").iniciar_quiz(quiz)

        with self.assertRaisesRegex(ValueError, "após iniciar"):
            quiz.adicionar_pergunta(criar_pergunta("Outra pergunta?"))
        with self.assertRaisesRegex(ValueError, "após iniciar"):
            quiz.remover_pergunta(pergunta)

    def test_colecoes_expostas_nao_alteram_estado_interno(self) -> None:
        pergunta = criar_pergunta()
        quiz = Quiz("Geografia", [pergunta])
        usuario = Usuario("Ana", "ana@example.com", "A001")
        tentativa = usuario.iniciar_quiz(quiz)

        quiz.perguntas.clear()
        usuario.tentativas.clear()
        tentativa.respostas.clear()

        self.assertEqual(len(quiz), 1)
        self.assertEqual(len(usuario.tentativas), 1)
        self.assertEqual(tentativa.respostas, [])


if __name__ == "__main__":
    unittest.main()
