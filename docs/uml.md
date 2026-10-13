# Modelo das classes

## Herança e relacionamentos

- `Usuario` herda de `Pessoa` os dados e validações de nome e e-mail.
- `Quiz` agrega perguntas. Uma mesma pergunta pode estar em mais de um quiz.
- `Usuario` mantém o histórico de tentativas; cada `Tentativa` referencia o usuário e o quiz correspondente.
- `Pergunta` usa `NivelDificuldade` para restringir os níveis disponíveis.

## Fluxo de uma tentativa

1. O usuário inicia um quiz com `iniciar_quiz(quiz)`.
2. `registrar_resposta(indice)` guarda a opção escolhida para a próxima pergunta.
3. `finalizar(tempo_total)` calcula a pontuação e a taxa de acertos.

## Diagrama

```mermaid
classDiagram
    class Pessoa {
        +str nome
        +str email
    }
    class Usuario {
        +str matricula_ou_id
        +list~Tentativa~ tentativas
        +iniciar_quiz(quiz) Tentativa
        +consultar_historico() list~Tentativa~
    }
    class Quiz {
        +str titulo
        +list~Pergunta~ perguntas
        +int limite_tentativas
        +int? tempo_limite_minutos
        +adicionar_pergunta(pergunta)
        +remover_pergunta(pergunta)
        +calcular_pontuacao_maxima() int
    }
    class Pergunta {
        +str enunciado
        +list~str~ alternativas
        +int indice_resposta_correta
        +str tema
        +NivelDificuldade dificuldade
    }
    class Tentativa {
        +list~int~ respostas
        +int pontuacao_obtida
        +float tempo_total
        +float taxa_acertos
        +bool concluida
        +registrar_resposta(indice) void
        +finalizar(tempo_total) void
    }
    class NivelDificuldade {
        <<enumeration>>
        FACIL
        MEDIO
        DIFICIL
    }

    Pessoa <|-- Usuario
    Quiz "0..*" o-- "0..*" Pergunta : agrega
    Usuario "1" *-- "0..*" Tentativa : mantém histórico
    Tentativa "0..*" --> "1" Quiz : referencia
    Pergunta --> NivelDificuldade : usa
```
