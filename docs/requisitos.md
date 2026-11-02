# Requisitos e regras de negócio

## Fontes consultadas

- **F1 — Entrega 1.0.1:** README e UML versionados na tag `v1.0.1`; estabelecem usuários, quizzes, perguntas, tentativas e dificuldade.
- **F2 — Entrega 2:** README, UML e modelos do commit `f2d41a3`; acrescentam encapsulamento, validações, limites e operações de quiz.
- **F3 — Entrega 3:** README, UML e implementação no commit `27d1a37`; acrescentam `Pessoa`, histórico, resposta, pontuação, JSON e relatório.
- **F4 — Materiais recebidos nesta consolidação:** instruções das quatro etapas, requisitos funcionais e a cópia com CLI/testes incluída na pasta de trabalho.

Não foi encontrado enunciado oficial separado. As fontes não especificam idade mínima, autenticação, unicidade de matrícula/ID, validação sintática de e-mail ou política de encerramento ao expirar o tempo configurado.

## Regras verificáveis

| ID | Regra válida | Validação e efeito | Origem |
| --- | --- | --- | --- |
| RB-01 | Nome, e-mail, matrícula/ID, título, enunciado e tema são textos não vazios. | Construtores rejeitam valores vazios e tipos incorretos. | F1–F4 |
| RB-02 | Pergunta de múltipla escolha tem de 3 a 5 alternativas textuais não vazias. | `PerguntaMultiplaEscolha` valida quantidade e conteúdo. | F1, F2 |
| RB-03 | Gabarito de múltipla escolha é um índice inteiro existente; booleanos não contam como índices. | O construtor rejeita índice fora do intervalo, booleano ou outro tipo. | F1, F2 |
| RB-04 | Pergunta verdadeiro/falso recebe gabarito booleano. | `PerguntaVerdadeiroFalso` rejeita outros tipos. | F4 (implementação recebida) |
| RB-05 | Dificuldade pertence a `NivelDificuldade` (`FACIL`, `MEDIO`, `DIFICIL`). | Os tipos concretos de pergunta validam o enum. | F1–F4 |
| RB-06 | Limite de tentativas é inteiro positivo; tempo limite informado é inteiro positivo em minutos. | `Quiz` valida os limites no domínio. | F2, F3 |
| RB-07 | Quiz tem perguntas antes de ser iniciado; o usuário ainda não pode ter atingido o limite daquele quiz. | `Usuario.iniciar_quiz` conta inícios anteriores do mesmo objeto e rejeita quiz vazio ou limite atingido. | F2, F3 |
| RB-08 | Quiz temático contém somente perguntas do tema definido. | `QuizTematico.adicionar_pergunta` rejeita tema diferente. | F4 (extensão existente) |
| RB-09 | As perguntas de um quiz não mudam depois do início da primeira tentativa. | `Quiz` rejeita adição/remoção posterior, preservando o conjunto usado nos resultados. | F4 (integridade das tentativas) |
| RB-10 | A tentativa recebe uma opção válida para a próxima pergunta sem resposta. | `Tentativa.registrar_resposta` rejeita índice inválido, resposta extra ou tentativa já concluída. | F3, F4 |
| RB-11 | Uma tentativa só é finalizada uma vez e com todas as perguntas respondidas. | `Tentativa.finalizar` rejeita incompletude e repetição. | F3, F4 |
| RB-12 | Cada resposta correta vale um ponto; percentual é acertos dividido pelo total de perguntas. | `Tentativa.finalizar` corrige polimorficamente e calcula pontos e percentual. | F2, F3 |
| RB-13 | Duração é finita, numérica e não negativa, em segundos. | `Tentativa.finalizar` rejeita negativos, `NaN`, infinitos e booleanos. | F3, F4 |
| RB-14 | Perguntas, quizzes, usuários, tentativas e vínculos sobrevivem à reinicialização. | `persistencia.py` serializa JSON e reconstrói objetos; formatos inline antigos também são aceitos. | F3, F4 |
| RB-15 | CLI permite cadastro/consulta de quizzes e usuários, responder, consultar resultados e salvar. | `main.py` oferece o menu; erros de entrada são informados e dados corrompidos não são sobrescritos. | F4 |

## Decisões e limites

- `tempo_limite_minutos` é validado, salvo e exibido, mas não aciona cronômetro ou encerramento automático, pois não há política de timeout definida.
- O limite de tentativas conta quando `Usuario.iniciar_quiz` é chamado. Tentativas abandonadas ou interrompidas contam no limite e não podem ser retomadas pela CLI.
- Resposta e pontuação são armazenadas em memória enquanto a aplicação está aberta e gravadas no JSON após cada ação do menu ou ao sair.
- O JSON atual guarda perguntas uma vez e referencia seus índices nos quizzes, preservando reutilização. O carregador também lê os formatos anteriores com perguntas inline e o formato intermediário com referências por índice.
- O armazenamento não oferece autenticação, concorrência entre processos, histórico de alterações ou backup automático.
- Não há operações de edição/remoção de usuário na CLI; classes de domínio permitem adicionar/remover perguntas antes ou fora de tentativas. O sistema não impõe unicidade para e-mail ou matrícula/ID porque a regra não aparece nas fontes.

A relação entre regras, código e testes está em [matriz-rastreabilidade.md](matriz-rastreabilidade.md).
