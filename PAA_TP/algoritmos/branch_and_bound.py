import time

# Variáveis globais para armazenar o estado da busca
melhor_valor = 0
melhor_solucao = []

def calcular_solucao_gulosa_inicial(n, capacidade_peso, capacidade_volume, itens_ordenados):
    """
    Calcula uma solução inicial (piso) usando estratégia gulosa para 
    permitir podas desde o início da árvore.
    """
    valor_acumulado = 0
    peso_acumulado = 0
    volume_acumulado = 0
    solucao = [False] * n

    for p, v, val, idx_original in itens_ordenados:
        if peso_acumulado + p <= capacidade_peso and volume_acumulado + v <= capacidade_volume:
            peso_acumulado += p
            volume_acumulado += v
            valor_acumulado += val
            solucao[idx_original] = True
            
    return valor_acumulado, solucao

def calcular_limitante_superior(k, n, capacidade_peso, capacidade_volume, itens_ordenados, peso_atual, volume_atual, valor_atual):
    """
    Calcula o Bound usando Relaxação Fracionária.
    Ordenação sugerida: Valor / (Peso + Volume).
    """
    if k >= n:
        return valor_atual

    peso_restante = capacidade_peso - peso_atual
    volume_restante = capacidade_volume - volume_atual
    limitante = float(valor_atual)

    for i in range(k, n):
        p, v, val, _ = itens_ordenados[i]

        if p <= peso_restante and v <= volume_restante:
            peso_restante -= p
            volume_restante -= v
            limitante += val
        else:
            fracao_peso = peso_restante / p if p > 0 else 1
            fracao_volume = volume_restante / v if v > 0 else 1
            
            fracao = min(fracao_peso, fracao_volume)
            limitante += val * fracao
            break 

    return limitante

def backtrack(vetor, k, n, capacidade_peso, capacidade_volume, itens_ordenados, peso_atual, volume_atual, valor_atual):
    global melhor_valor, melhor_solucao
    
    if k == n:
        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_solucao = vetor.copy()
        return
    
    p, v, val, idx_original = itens_ordenados[k]

    if peso_atual + p <= capacidade_peso and volume_atual + v <= capacidade_volume:
        vetor[idx_original] = True
        backtrack(vetor, k + 1, n, capacidade_peso, capacidade_volume, itens_ordenados, 
                  peso_atual + p, volume_atual + v, valor_atual + val)
        vetor[idx_original] = False

    limitante_exclusao = calcular_limitante_superior(k + 1, n, capacidade_peso, capacidade_volume, 
                                                     itens_ordenados, peso_atual, volume_atual, valor_atual)
    
    if limitante_exclusao > melhor_valor:
        vetor[idx_original] = False
        backtrack(vetor, k + 1, n, capacidade_peso, capacidade_volume, itens_ordenados, 
                  peso_atual, volume_atual, valor_atual)