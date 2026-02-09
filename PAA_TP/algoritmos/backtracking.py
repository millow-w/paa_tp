melhor_valor = 0
melhor_solucao = []

def backtrack(vetor, k, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, peso_atual, volume_atual):
    global melhor_valor, melhor_solucao
    
    if k == n:
        valor = process_solution(vetor, n, valores)
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_solucao = vetor.copy()
    else:
        c = construct_candidates(k, peso_atual, volume_atual, pesos, volumes, capacidade_peso, capacidade_volume)
        for possibilidade in c:
            vetor[k] = possibilidade
            novo_peso = peso_atual + (pesos[k] if possibilidade else 0)
            novo_volume = volume_atual + (volumes[k] if possibilidade else 0)
            backtrack(vetor, k + 1, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, novo_peso, novo_volume)

def construct_candidates(k, peso_atual, volume_atual, pesos, volumes, capacidade_peso, capacidade_volume):
    
    c = []
    
    if peso_atual + pesos[k] <= capacidade_peso and volume_atual + volumes[k] <= capacidade_volume:
        c.append(True)
        
    c.append(False)
    return c

def process_solution(vetor, n, valores):
    valor_total = 0
    
    for i in range(n):
        valor_total += valores[i] if vetor[i] else 0
    return valor_total