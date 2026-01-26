# Trabalho Prático: Problema da Mochila 0-1 (Duas Restrições)

Repositório destinado ao desenvolvimento e avaliação do trabalho prático da disciplina de **BCC 241 - Projeto e Análise de Algoritmos (UFOP)**.

## 📖 Sobre o Projeto

Este trabalho consiste na avaliação empírica de três algoritmos para resolver o problema da mochila 0-1 sem repetição, considerando duas restrições: **peso** e **volume**.

O objetivo é maximizar o lucro transportado \(v_i\) respeitando os limites:

- **Capacidade de Peso (\(W\))**: Limite em quilos.
- **Capacidade de Volume (\(V\))**: Limite em litros.

### Algoritmos Implementados

Devem ser desenvolvidas três versões para o problema:

1. **Programação Dinâmica**
2. **Backtracking**
3. **Branch-and-Bound**

## 📥 Entrada e Saída

- **Entrada**: Leitura de um arquivo texto onde:
  - A primeira linha contém \(W\) (peso máximo) e \(V\) (volume máximo).
  - As demais linhas contêm, para cada item \(i\): \(w_i\) (peso), \(l_i\) (volume) e \(v_i\) (valor), separados por tabulação.

- **Saída**:
  - Lucro máximo obtido.
  - Itens selecionados.
  - Tempo de execução.

**Exemplo de entrada**:

```
10 9
6 3 10
3 4 14
4 2 16
2 5 9
```

## 🧪 Metodologia de Avaliação

Para cada combinação de:

- Número de itens (\(n\))
- Capacidade de peso (\(W\))
- Capacidade de volume (\(V\))

Devem ser realizados os seguintes passos:

1. Gerar 10 instâncias aleatórias.
2. Executar os três algoritmos sobre cada instância.
3. Coletar tempos de execução.

### Análise dos Resultados

- Realizar **testes estatísticos** para verificar possíveis empates entre algoritmos.
- Gerar **gráficos** do tempo de execução em função do número de itens e das capacidades.
- Analisar o comportamento assintótico de cada algoritmo.

## 📄 Relatório

O relatório deve conter:

- Título e autores.
- Resumo.
- Introdução (problema, objetivo, resultados e organização).
- Descrição dos algoritmos com análise de complexidade (tempo e espaço).
- Avaliação experimental (configuração, métricas, resultados e discussão).
- Conclusão.
- Referências bibliográficas.

**Formatação**: Máximo de 10 páginas, fonte Arial 12.

## 🗓️ Entrega e Apresentação

- **Data de entrega**: 01/02/2026.
- **Grupos**: 4 alunos.
- **Valor**: 10 pontos (peso 1.5).
- **Apresentação**:
  - Um membro será escolhido aleatoriamente pelo professor.
  - Apresentação de 15 minutos.
  - A nota da apresentação será atribuída a todo o grupo.
