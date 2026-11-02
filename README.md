# Sistema de Quiz Educacional

Aplicação de terminal para a disciplina de Programação Orientada a Objetos. O sistema cadastra usuários e quizzes, apresenta perguntas de múltipla escolha ou verdadeiro/falso, registra tentativas, corrige respostas e persiste o histórico em JSON.

## Objetivo

Demonstrar modelagem de domínio, encapsulamento, abstração, herança, polimorfismo, relacionamentos entre classes e separação entre interface, regras de negócio e persistência.

## Funcionalidades

- Cadastrar e listar quizzes gerais ou temáticos.
- Criar perguntas de múltipla escolha e verdadeiro/falso, com tema, dificuldade e gabarito.
- Cadastrar e listar usuários; o cadastro também pode ocorrer ao iniciar uma tentativa.
- Responder às perguntas na ordem apresentada e corrigir a tentativa automaticamente.
- Calcular pontuação, percentual de acertos e duração.
- Consultar tentativas concluídas e em andamento por relatório.
- Salvar e recuperar quizzes, perguntas, usuários e histórico em `dados.json`.
- Validar dados no domínio e informar entradas inválidas na CLI.

## Tecnologias

- Python 3.10 ou superior.
- Biblioteca padrão do Python (`json`, `pathlib`, `abc`, `enum`, `unittest`, entre outras).
- Persistência local em JSON; não há dependências externas nem etapa de build.

## Estrutura

```text
.
├── main.py                  # CLI e ponto de entrada
├── persistencia.py          # serialização, migração e recuperação JSON
├── relatorios.py            # resumo de desempenho
├── models/
│   ├── pessoa.py            # classe-base de identificação
│   ├── usuario.py           # usuário e histórico
│   ├── pergunta.py          # abstração e tipos concretos de pergunta
│   ├── quiz.py              # quiz geral e coleção de perguntas
│   ├── quiz_tematico.py     # quiz que valida o tema das perguntas
│   ├── tentativa.py         # respostas, correção e resultado
│   └── nivel_dificuldade.py # enum de dificuldade
├── tests/                   # testes automatizados com unittest
└── docs/
    ├── diagnostico.md       # auditoria e comparação das fontes
    ├── checklist-entregas.md
    ├── requisitos.md        # regras e premissas
    ├── matriz-rastreabilidade.md
    └── uml.md                # UML textual e Mermaid
```

## Classes e relacionamentos

| Classe | Responsabilidade |
| --- | --- |
| `Pessoa` | Validar e expor nome e e-mail. |
| `Usuario(Pessoa)` | Acrescentar matrícula/ID e manter tentativas. |
| `Pergunta` | Definir a interface abstrata de opções e correção. |
| `PerguntaMultiplaEscolha(Pergunta)` | Validar três a cinco alternativas e o índice correto. |
| `PerguntaVerdadeiroFalso(Pergunta)` | Apresentar duas opções e corrigir por gabarito booleano. |
| `Quiz` | Agregar perguntas e armazenar limites. |
| `QuizTematico(Quiz)` | Aceitar somente perguntas do tema escolhido. |
| `Tentativa` | Associar usuário e quiz, registrar respostas e calcular o resultado. |
| `NivelDificuldade` | Restringir a dificuldade a fácil, médio ou difícil. |

`Quiz` agrega perguntas, que podem ser reutilizadas em mais de um quiz. `Usuario` mantém zero ou mais tentativas; cada `Tentativa` referencia um usuário e um quiz. As coleções expostas pelas classes são cópias, para evitar alterações externas acidentais.

## POO aplicada

- **Abstração:** `Pergunta` é uma classe abstrata que declara `opcoes` e `corrigir()`.
- **Encapsulamento:** estado interno com atributos convencionados como privados, propriedades de leitura e cópias de listas.
- **Herança:** `Usuario` herda de `Pessoa`; os dois tipos concretos herdam de `Pergunta`; `QuizTematico` herda de `Quiz`.
- **Polimorfismo:** `Tentativa`, persistência e CLI trabalham com `Pergunta` e usam `opcoes`/`corrigir()` sem depender do tipo concreto.
- **Responsabilidade:** os modelos validam regras do domínio; `main.py` cuida da interação; `persistencia.py` serializa; `relatorios.py` apresenta resultados.

## Regras principais

- Campos de identificação, títulos, enunciados e temas não podem estar vazios.
- Perguntas de múltipla escolha aceitam de três a cinco alternativas textuais não vazias e exigem índice correto válido.
- Perguntas verdadeiro/falso exigem gabarito booleano.
- Limite de tentativas e tempo limite configurado devem ser inteiros positivos.
- Quiz vazio não pode ser iniciado; o limite conta cada início, inclusive tentativa não concluída.
- Uma tentativa aceita uma resposta válida por pergunta, em ordem, e só pode ser finalizada uma vez após todas as respostas.
- Depois que a primeira tentativa começa, o conjunto de perguntas do quiz fica bloqueado para preservar resultados e histórico.
- Cada resposta correta vale um ponto. O percentual é calculado sobre o número de perguntas.
- A duração é registrada em segundos e precisa ser finita e não negativa.

O campo `tempo_limite_minutos` é salvo e exibido, mas não há cronômetro nem encerramento automático. As fontes recebidas não definem a consequência de expiração, então essa política ficou fora da implementação. Também não foram presumidos idade mínima, formato rígido de e-mail ou unicidade de matrícula/ID. As premissas e origens estão em [docs/requisitos.md](docs/requisitos.md).

## Persistência

Os dados ficam em `dados.json` ao lado de `main.py`. A gravação usa um arquivo temporário no mesmo diretório e substituição ao concluir, e o formato mantém referências para que uma pergunta compartilhada continue sendo o mesmo objeto após a recuperação. O carregador aceita os formatos anteriores com perguntas dentro de cada quiz e o formato intermediário com perguntas referenciadas por índice.

Se o JSON estiver ilegível ou inconsistente, a CLI informa o erro e não sobrescreve o arquivo. O armazenamento é local e não implementa autenticação, concorrência entre processos, backup ou transações entre várias gravações.

## Instalação e execução

Instale Python 3.10 ou superior. Não é necessário instalar dependências adicionais. No terminal, a partir desta pasta:

```bash
python main.py
```

O menu permite listar e cadastrar quizzes, cadastrar e listar usuários, responder a um quiz, consultar relatórios e salvar e sair. Para um quiz temático, todas as perguntas precisam usar o tema informado no cadastro. O cadastro feito durante a resposta reutiliza um usuário quando nome, e-mail e matrícula/ID correspondem exatamente. Para cada tentativa, a CLI apresenta a duração medida em segundos.

### Demonstração rápida

1. Escolha `2` e cadastre um quiz geral ou temático.
2. Cadastre pelo menos uma pergunta e informe o gabarito.
3. Escolha `4` para responder; informe os dados do usuário ou reutilize o cadastro existente.
4. Escolha `5` para consultar o relatório e `7` para salvar e sair.
5. Execute `python main.py` novamente para recuperar os dados salvos.

Autor: José Felipe dos Santos Souza — Engenharia de Software.
