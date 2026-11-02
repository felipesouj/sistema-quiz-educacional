# Checklist das quatro etapas

Este checklist resume os requisitos acadêmicos presentes no pedido da consolidação e nos documentos recebidos. O checklist de origem menciona ES0008/UFCA; não havia enunciado oficial independente para conferir detalhes adicionais.

| Etapa | Itens verificados | Evidência no projeto | Situação |
| --- | --- | --- | --- |
| 1 — Modelagem OO | UML textual; classes, atributos, métodos e relações; README com objetivo e estrutura; classes com docstrings. | [uml.md](uml.md), [README.md](../README.md), docstrings em `models/`. | Atendida |
| 2 — Implementação e encapsulamento | Classes-base, atributos internos, propriedades de leitura, validações e responsabilidades definidas. | `Pessoa`, `Usuario`, `Pergunta`, `Quiz`, `Tentativa` e `NivelDificuldade`. | Atendida |
| 3 — Herança, relações e persistência | Herança funcional; associações/agregação/composição; JSON recuperável; relatório. | `Usuario(Pessoa)`, tipos concretos de `Pergunta`, `QuizTematico`, `persistencia.py`, `relatorios.py`. | Atendida |
| 4 — Regras e integração | Regras na camada de domínio; quiz não vazio; perguntas estáveis após início; CLI; persistência integrada; testes automatizados. | `models/`, `main.py`, `persistencia.py`, `tests/`. | Atendida |

## Conceitos de POO

| Conceito | Evidência |
| --- | --- |
| Abstração | `Pergunta` abstrata e o enum `NivelDificuldade`. |
| Encapsulamento | Estado interno, propriedades de leitura e cópias de coleções. |
| Herança | `Usuario(Pessoa)`, `PerguntaMultiplaEscolha(Pergunta)`, `PerguntaVerdadeiroFalso(Pergunta)` e `QuizTematico(Quiz)`. |
| Polimorfismo | `Tentativa` chama `Pergunta.corrigir()` sem distinguir o tipo concreto. |

## Pendências de especificação

- O tempo limite configurado não possui cronômetro nem ação automática ao expirar, porque as fontes recebidas não dizem se a tentativa deve ser encerrada, enviada ou penalizada.
- A CLI não retoma nem cancela tentativas interrompidas. O início conta no limite; tentativas em andamento aparecem no relatório.
- Não foram implementados idade mínima, autenticação, formato estrito de e-mail ou unicidade de matrícula/ID, pois não constam dos requisitos disponíveis.

Os testes são executados com `python -m unittest discover -s tests -v`. A [matriz de rastreabilidade](matriz-rastreabilidade.md) aponta os casos automatizados por regra.
