melhor_valor = 0
melhor_solucao = []

def calcular_limitante_superior(k, n, capacidade_peso, capacidade_volume, pesos, volumes, valores, peso_atual, volume_atual, valor_atual):
    """
    Calcula o limitante superior (bound) usando relaxação fracionária.
    Ordena os itens restantes por densidade de valor e adiciona itens fracionários.
    """
    if k >= n:
        return valor_atual
    
    # Capacidades restantes
    peso_restante = capacidade_peso - peso_atual
    volume_restante = capacidade_volume - volume_atual
    
    # Calcular densidades para itens restantes
    itens_restantes = []
    for i in range(k, n):
        # Densidade baseada no recurso mais restritivo
        densidade = valores[i] / max(pesos[i], volumes[i]) if max(pesos[i], volumes[i]) > 0 else 0
        itens_restantes.append((densidade, pesos[i], volumes[i], valores[i]))
    
    # Ordenar por densidade (decrescente)
    itens_restantes.sort(reverse=True, key=lambda x: x[0])
    
    limitante = valor_atual
    
    # Adicionar itens gulosos (fracionários se necessário)
    for densidade, peso, volume, valor in itens_restantes:
        if peso <= peso_restante and volume <= volume_restante:
            # Adicionar item completo
            limitante += valor
            peso_restante -= peso
            volume_restante -= volume
        else:
            # Adicionar fração do item baseada no recurso mais restritivo
            fracao_peso = peso_restante / peso if peso > 0 else float('inf')
            fracao_volume = volume_restante / volume if volume > 0 else float('inf')
            fracao = min(1.0, fracao_peso, fracao_volume)
            limitante += valor * fracao
            break
    
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
    # Branch and Bound: explorar primeiro o ramo mais promissor (incluir item se possível)
    c = []
    
    # Tentar incluir o item primeiro (ramo mais promissor)
    if peso_atual + pesos[k] <= capacidade_peso and volume_atual + volumes[k] <= capacidade_volume:
        c.append(True)
    
    # Depois tentar não incluir
    c.append(False)
        
    return c