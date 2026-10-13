# Sistema de Quiz Educacional

Projeto simples de programação orientada a objetos para criar quizzes, registrar tentativas e consultar resultados.

## Funcionalidades

- `Usuario` herda de `Pessoa` e reaproveita a validação e as propriedades de nome e e-mail.
- `Quiz` reúne objetos `Pergunta`; `Usuario` mantém suas `Tentativa`; cada tentativa referencia o usuário e o quiz.
- A tentativa registra uma alternativa por pergunta, calcula pontuação e percentual ao finalizar.
- `persistencia.py` salva e carrega quizzes, usuários e tentativas em JSON.
- `relatorios.py` gera um resumo textual das tentativas por usuário.

## Como executar

Com Python 3.10 ou superior, execute na pasta do projeto:

```bash
python main.py
```

O exemplo cria um quiz, registra respostas, salva os dados em `dados.json`, carrega o arquivo e imprime o relatório.

## Uso básico

```python
from models import NivelDificuldade, Pergunta, Quiz, Usuario
from persistencia import carregar_dados, salvar_dados
from relatorios import gerar_relatorio

pergunta = Pergunta(
    "Quanto é 2 + 2?", ["3", "4", "5"], 1, "Matemática", NivelDificuldade.FACIL
)
quiz = Quiz("Matemática", [pergunta])
usuario = Usuario("Ana", "ana@example.com", "A001")

tentativa = usuario.iniciar_quiz(quiz)
tentativa.registrar_resposta(1)  # Índices das alternativas começam em zero.
tentativa.finalizar(tempo_total=12)

salvar_dados([usuario], [quiz])
usuarios, quizzes = carregar_dados()
print(gerar_relatorio(usuarios))
```

Consulte [docs/uml.md](docs/uml.md) para as classes e seus relacionamentos.

Autor: José Felipe dos Santos Souza — Engenharia de Software.
