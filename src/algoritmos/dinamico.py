# algoritmos/dinamico.py

def dinamico(W, V, n, pesos, volumes, valores):
    # 1. Criação do cubo (W+1 x V+1 x n+1)
    K = [[[None for _ in range(n + 1)] for _ in range(V + 1)] for _ in range(W + 1)]
    
    # Se a quantidade de itens (j) é 0, o lucro é 0 para qualquer W e V
    for w in range(W + 1):
        for v in range(V + 1):
            K[w][v][0] = 0

    # Se o Peso disponível (w) é 0, o lucro é 0 para qualquer j e v
    for j in range(n + 1):
        for v in range(V + 1):
            K[0][v][j] = 0

    # Se o Volume disponível (v) é 0, o lucro é 0 para qualquer j e w
    for j in range(n + 1):
        for w in range(W + 1):
            K[w][0][j] = 0

    # 2. Preenchimento do Miolo (DP Iterativa)
    for j in range(1, n + 1):
        for w in range(1, W + 1):
            for v in range(1, V + 1):
                if pesos[j] > w or volumes[j] > v:
                    K[w][v][j] = K[w][v][j - 1]
                else:
                    K[w][v][j] = max(
                        K[w][v][j - 1],
                        valores[j] + K[w - pesos[j]][v - volumes[j]][j - 1]
                    )

    melhor_valor = K[W][V][n]

    # 3. Recuperação da solução (caminho de volta no cubo)
    melhor_solucao = [False] * n
    w_at, v_at = W, V
    
    for j in range(n, 0, -1):
        # Se o valor mudou, o item j foi incluído
        if K[w_at][v_at][j] != K[w_at][v_at][j-1]:
            melhor_solucao[j-1] = True
            w_at -= pesos[j]
            v_at -= volumes[j]

    return melhor_valor, melhor_solucao