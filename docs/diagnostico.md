# Auditoria e consolidação

## Escopo e fontes

Foram examinados o histórico Git disponível (`v1.0.0`, `v1.0.1` e commits até `27d1a37`), os arquivos versionados, as alterações locais existentes, as duas cópias do projeto encontradas na pasta, os README/UML/requisitos/checklists, os modelos, a persistência e os testes. O arquivo `sistema-quiz-educacional.rar`, adjacente ao repositório, contém a cópia aninhada que também foi inspecionada.

Não foi encontrado um enunciado oficial da disciplina separado dos arquivos do projeto. O checklist recebido menciona o Projeto 1 — ES0008/UFCA; essa identificação e as regras específicas do tema não puderam ser verificadas em material oficial adicional. As decisões funcionais foram limitadas aos artefatos disponíveis e ao pedido desta consolidação.

## Fontes comparadas

| Fonte | O que trouxe | Avaliação |
| --- | --- | --- |
| Tag `v1.0.1` | Modelo inicial do domínio, enum, README e UML. | Útil para preservar nomes, atributos e relações; código ainda era sobretudo estrutura e documentação. |
| Commit `f2d41a3` — Entrega 2 | Construtores, propriedades de leitura e validações em perguntas, quizzes, usuários e tentativas. | Base das regras de entrada e do encapsulamento. Ainda não concluía resposta, resultado ou persistência. |
| Commit `27d1a37` — Entrega 3 | `Pessoa`, herança de `Usuario`, limite de tentativas, respostas, pontuação, JSON e relatório. | Base funcional de domínio e persistência. `main.py` era uma demonstração fixa, sem CLI de cadastro. |
| Cópia incluída no RAR | CLI, abstração de pergunta, múltipla escolha/verdadeiro-falso, quiz temático e 21 testes. | Aproveitada para a integração e os fluxos interativos. A persistência antiga repetia perguntas em cada quiz e não preservava identidade compartilhada. |
| Alterações locais encontradas | Requisitos, rastreabilidade, testes adicionais, `QuizTematico` e proposta de persistência por referências. | Preservadas quando coerentes; a raiz continha testes incompatíveis com o `main.py` placeholder e modelos incompletos. A persistência por referências foi integrada e ampliada. |

## Decisões da consolidação

- Manter a implementação executável na raiz do repositório, em uma única árvore `models/`, `tests/` e `docs/`.
- Preservar `Usuario(Pessoa)` e acrescentar a abstração `Pergunta` com subclasses de múltipla escolha e verdadeiro/falso. A correção usa polimorfismo por `corrigir()`.
- Manter `QuizTematico`, existente nas alterações locais, e disponibilizá-lo tanto no modelo quanto na CLI.
- Integrar a CLI da cópia do RAR e acrescentar cadastro/listagem explícitos de usuários.
- Manter JSON, acrescentando salvamento temporário com substituição atômica, referências compartilhadas para perguntas reutilizadas e leitura dos formatos inline anteriores.
- Preservar a regra de um ponto por pergunta, o limite de tentativas, a validação do tempo gasto e o limite temporal configurável sem cronômetro. A documentação anterior não define o que deve acontecer ao expirar o limite.
- Bloquear adição/remoção de perguntas depois da primeira tentativa, para que respostas e resultados históricos continuem associados ao mesmo conjunto de perguntas.
- Não adicionar dependências, autenticação, unicidade de identificador ou outras regras sem fonte.

## Limpeza e organização

- A cópia aninhada `sistema-quiz-educacional/` foi removida após auditoria e integração das funcionalidades úteis à raiz. Ela duplicava código, testes e documentação, além de conter um `dados.json` de demonstração.
- `exemplo_etapa3.py` foi removido porque seu fluxo fixo foi substituído pela CLI interativa e pelos testes. `docs/funcionalidades_adicionais.md` foi removido após incorporar os pontos mantidos ao README, à UML e aos requisitos.
- Caches Python gerados foram removidos; `.gitignore` ignora `__pycache__`, `*.pyc`, ambientes virtuais e `dados.json` local.
- O arquivo RAR está fora do repositório Git e foi mantido na pasta de origem.
- O diretório `.git` e o histórico de commits/tags foram preservados. Nenhum commit ou referência histórica foi apagado.

## Resultado e limitações

A CLI final cadastra e lista quizzes e usuários, executa tentativas, apresenta relatórios e persiste os dados. Os testes cobrem regras centrais, os dois tipos de pergunta, perguntas reutilizadas, formatos de persistência anteriores e o fluxo da interface. A implementação consolidada e testada está na raiz do repositório. A pendência funcional conhecida é a política de tempo limite, não especificada nas fontes recebidas.

O tempo limite do quiz continua apenas informativo. Tentativas não concluídas permanecem no histórico e contam para o limite configurado; a CLI não oferece retomada nem cancelamento. Esses comportamentos são documentados porque as fontes não especificam outra política. A matriz de cobertura está em [matriz-rastreabilidade.md](matriz-rastreabilidade.md), e a lista de etapas está em [checklist-entregas.md](checklist-entregas.md).
