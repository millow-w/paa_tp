"""
Branch and Bound com Relaxação Fracionária para Mochila 0-1 com duas restrições
"""

class BranchAndBound:
    def __init__(self):
        self.melhor_valor = 0
        self.melhor_solucao = []
    
    def resolver(self, capacidade_peso, capacidade_volume, pesos, volumes, valores):
        n = len(pesos)
        self.melhor_valor = 0
        self.melhor_solucao = [False] * n
        
        # Criar lista de índices ordenados por densidade de valor
        # Densidade = valor / min(peso, volume) para considerar ambas restrições
        indices = list(range(n))
        densidades = []
        for i in range(n):
            # Usar o mínimo entre peso e volume normalizado pela capacidade
            # para considerar qual restrição é mais limitante
            restricao_limitante = min(pesos[i] / capacidade_peso if capacidade_peso > 0 else float('inf'),
                                     volumes[i] / capacidade_volume if capacidade_volume > 0 else float('inf'))
            if restricao_limitante > 0:
                densidade = valores[i] / restricao_limitante
            else:
                densidade = valores[i]
            densidades.append(densidade)
        
        # Ordenar por densidade decrescente
        indices.sort(key=lambda i: densidades[i], reverse=True)
        
        # Reordenar arrays
        pesos_ord = [pesos[i] for i in indices]
        volumes_ord = [volumes[i] for i in indices]
        valores_ord = [valores[i] for i in indices]
        
        # Resolver com arrays ordenados
        vetor = [False] * n
        self._backtrack(vetor, 0, n, capacidade_peso, capacidade_volume,
                       pesos_ord, volumes_ord, valores_ord, 0, 0, 0)
        
        # Mapear solução de volta para ordem original
        solucao_original = [False] * n
        for i in range(n):
            if self.melhor_solucao[i]:
                solucao_original[indices[i]] = True
        self.melhor_solucao = solucao_original
        
        return self.melhor_valor, self.melhor_solucao
    
    def _bound(self, k, n, cap_p, cap_v, pesos, volumes, valores, p_usado, v_usado, valor_atual):
        """
        Limitante superior usando relaxação fracionária.
        Assume que os itens já estão ordenados por densidade de valor.
        """
        if k >= n:
            return valor_atual
        
        bound = valor_atual
        p_rest = cap_p - p_usado
        v_rest = cap_v - v_usado
        
        # Greedy: adicionar itens completos enquanto couber
        for i in range(k, n):
            if pesos[i] <= p_rest and volumes[i] <= v_rest:
                bound += valores[i]
                p_rest -= pesos[i]
                v_rest -= volumes[i]
            else:
                # Adicionar fração do próximo item (relaxação fracionária)
                # A fração é limitada pela restrição mais apertada
                if pesos[i] > 0 and volumes[i] > 0:
                    fracao_peso = p_rest / pesos[i] if pesos[i] > 0 else 1.0
                    fracao_volume = v_rest / volumes[i] if volumes[i] > 0 else 1.0
                    fracao = min(1.0, fracao_peso, fracao_volume)
                    bound += fracao * valores[i]
                break
        
        return bound
    
    def _backtrack(self, vetor, k, n, cap_p, cap_v, pesos, volumes, valores, p_usado, v_usado, valor_atual):
        # Base case
        if k == n:
            if valor_atual > self.melhor_valor:
                self.melhor_valor = valor_atual
                self.melhor_solucao = vetor[:]
            return
        
        # Bound
        limitante = self._bound(k, n, cap_p, cap_v, pesos, volumes, valores, p_usado, v_usado, valor_atual)
        
        # Poda
        if limitante <= self.melhor_valor:
            return
        
        # Tentar incluir item k
        if p_usado + pesos[k] <= cap_p and v_usado + volumes[k] <= cap_v:
            vetor[k] = True
            self._backtrack(vetor, k+1, n, cap_p, cap_v, pesos, volumes, valores,
                          p_usado + pesos[k], v_usado + volumes[k], valor_atual + valores[k])
        
        # Não incluir item k
        vetor[k] = False
        self._backtrack(vetor, k+1, n, cap_p, cap_v, pesos, volumes, valores,
                      p_usado, v_usado, valor_atual)
