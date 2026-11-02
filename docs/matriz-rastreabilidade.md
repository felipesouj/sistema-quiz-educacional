# Matriz de rastreabilidade

As fontes F1–F4 estão descritas em [requisitos.md](requisitos.md). Os nomes dos testes são métodos executáveis da suíte `unittest`.

| Requisito | Implementação | Evidência automatizada | Situação |
| --- | --- | --- | --- |
| RB-01 — textos obrigatórios | `models/pessoa.py`, `models/usuario.py`, `models/quiz.py`, `models/pergunta.py` | `test_rejeita_campos_textuais_obrigatorios_vazios` | Atendido |
| RB-02 — alternativas de múltipla escolha | `PerguntaMultiplaEscolha.validar_alternativas` | `test_rejeita_quantidade_invalida_de_alternativas` | Atendido |
| RB-03 — índice correto válido | `PerguntaMultiplaEscolha.validar_resposta_correta` | `test_rejeita_indice_correto_fora_da_lista_e_booleano` | Atendido |
| RB-04 — gabarito verdadeiro/falso | `PerguntaVerdadeiroFalso` | `test_verdadeiro_falso_com_afirmacao_falsa_e_validacao` | Atendido |
| RB-05 — enum de dificuldade | `models/nivel_dificuldade.py`, hierarquia `Pergunta` | `test_dificuldade_deve_ser_um_valor_do_enum` | Atendido |
| RB-06 — limite e tempo de quiz | `Quiz.__init__` | `test_validacao_dos_limites_configurados_no_quiz` | Atendido |
| RB-07 — início válido e tentativas limitadas | `Usuario.iniciar_quiz` | `test_nao_inicia_quiz_vazio_e_respeita_limite_de_tentativas` | Atendido |
| RB-08 — tema de quiz temático | `QuizTematico.adicionar_pergunta` | `test_quiz_tematico_so_aceita_perguntas_do_tema`; `test_cadastra_quiz_tematico` | Atendido |
| RB-09 — quiz estável após iniciar tentativa | `Quiz._validar_editavel` | `test_perguntas_do_quiz_ficam_estaveis_apos_inicio_de_tentativa` | Atendido |
| RB-10 — resposta válida e sequencial | `Tentativa.registrar_resposta` | `test_impede_resposta_invalida_extra_e_finalizacao_incompleta` | Atendido |
| RB-11 — finalização completa e única | `Tentativa.finalizar` | `test_impede_resposta_invalida_extra_e_finalizacao_incompleta` | Atendido |
| RB-12 — pontuação e percentual | `Tentativa.finalizar` e `Pergunta.corrigir` | `test_inicia_responde_calcula_resultado_e_fecha`; `test_quiz_misto_e_pontuado_polimorficamente` | Atendido |
| RB-13 — duração finita e não negativa | `Tentativa.finalizar` | `test_rejeita_tempo_negativo_nao_finito_ou_booleano` | Atendido |
| RB-14 — persistência, relações e formatos anteriores | `persistencia.py` | `test_round_trip_preserva_quizzes_usuarios_e_tentativas`; `test_carrega_formato_inline_da_entrega_anterior`; `test_carrega_formato_com_perguntas_referenciadas` | Atendido |
| RB-15 — cadastro, consulta e CLI | `main.py`, `relatorios.py` | `test_cadastra_lista_responde_e_persiste_um_quiz`; `test_cadastra_e_lista_usuario_sem_iniciar_quiz`; `test_entrada_invalida_nao_impede_retorno_ao_menu` | Atendido |
| JSON inválido não é sobrescrito | `main.executar_cli` | `test_json_invalido_e_preservado_sem_solicitar_entrada` | Atendido |
| Abstração, herança e polimorfismo | `Pergunta(ABC)`, tipos concretos, `Usuario(Pessoa)`, `QuizTematico(Quiz)` | `test_pergunta_base_e_abstrata`; `test_usuario_herda_de_pessoa_e_reutiliza_validacao`; `test_tipos_diferentes_respondem_a_mesma_mensagem` | Atendido |
| Encapsulamento de coleções | Propriedades dos modelos retornam cópias | `test_lista_de_alternativas_exposta_e_uma_copia`; `test_colecoes_expostas_nao_alteram_estado_interno` | Atendido |
| Pergunta compartilhada entre quizzes | JSON serializa cada objeto uma vez e usa referências | `test_round_trip_preserva_quizzes_usuarios_e_tentativas` | Atendido |
| Timeout automático | Não definido nas fontes disponíveis | Não aplicável | Pendente de especificação |

As limitações de identidade, tempo e persistência estão detalhadas em [requisitos.md](requisitos.md).
