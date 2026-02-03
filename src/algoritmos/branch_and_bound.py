"""
Branch and Bound para Mochila 0-1 com duas restrições (peso e volume)
"""

melhor_valor = 0
melhor_solucao = []

def calcular_limitante_superior(k, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, peso_atual, volume_atual, valor_atual):
    """
    Calcula o limitante superior (bound) para mochila bidimensional.
    Para garantir otimismo, soma TODOS os itens que cabem individualmente.
    """
    if k >= n:
        return valor_atual
    
    # Capacidades restantes
    peso_restante = capacidade_peso - peso_atual
    volume_restante = capacidade_volume - volume_atual
    
    limitante = valor_atual
    
    # Adicionar TODOS os itens que cabem nas restrições (otimista)
    for i in range(k, n):
        if pesos[i] <= peso_restante and volumes[i] <= volume_restante:
            limitante += valores[i]
    
    return limitante

def backtrack(vetor, k, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, peso_atual, volume_atual, valor_atual):
    global melhor_valor, melhor_solucao
    
    # Caso base: chegou ao fim
    if k == n:
        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_solucao = vetor.copy()
        return
    
    # Calcular limitante superior para o nó atual
    limitante = calcular_limitante_superior(k, n, capacidade_peso, capacidade_volume, 
                                            pesos, volumes, valores, peso_atual, volume_atual, valor_atual)
    
    # PODA: Se o limitante não supera o melhor valor, não explore este ramo
    if limitante <= melhor_valor:
        return
    
    # Explorar ramos
    c = construct_candidates(k, peso_atual, volume_atual, pesos, volumes, capacidade_peso, capacidade_volume)
    for possibilidade in c:
        vetor[k] = possibilidade
        novo_peso = peso_atual + (pesos[k] if possibilidade else 0)
        novo_volume = volume_atual + (volumes[k] if possibilidade else 0)
        novo_valor = valor_atual + (valores[k] if possibilidade else 0)
        backtrack(vetor, k + 1, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, novo_peso, novo_volume, novo_valor)

def construct_candidates(k, peso_atual, volume_atual, pesos, volumes, capacidade_peso, capacidade_volume):
    """
    Branch and Bound: explorar primeiro o ramo mais promissor (incluir item se possível)
    """
    c = []
    
    # Tentar incluir o item primeiro (ramo mais promissor)
    if peso_atual + pesos[k] <= capacidade_peso and volume_atual + volumes[k] <= capacidade_volume:
        c.append(True)
    
    # Depois tentar não incluir
    c.append(False)
        
    return c