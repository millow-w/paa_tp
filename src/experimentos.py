import time
import sys
from utils import ler_instancia, executar_com_timeout
import algoritmos.backtracking as bt
import algoritmos.branch_and_bound as bnb
import algoritmos.dinamico as din

def resolver_backtracking(W, V, itens, timeout_seconds=None):
    """
    Resolve o problema da mochila usando backtracking.
    Retorna: (melhor_valor, melhor_solucao, tempo_execucao, sucesso)
    """
    def _executar():
        bt.melhor_valor = 0
        bt.melhor_solucao = []
            
        n = len(itens)
        vetor = [False] * n
        
        pesos = [item[0] for item in itens]
        volumes = [item[1] for item in itens]
        valores = [item[2] for item in itens]
        
        inicio = time.time()
        bt.backtrack(vetor, 0, n, W, V, pesos, volumes, valores, 0, 0)
        tempo = time.time() - inicio
        
        return bt.melhor_valor, bt.melhor_solucao, tempo
    
    if timeout_seconds:
        resultado, sucesso = executar_com_timeout(_executar, timeout_seconds)
        if sucesso:
            valor, solucao, tempo = resultado
            return valor, solucao, tempo, True
        else:
            return None, None, timeout_seconds, False
    else:
        valor, solucao, tempo = _executar()
        return valor, solucao, tempo, True

def resolver_branch_and_bound(W, V, itens, timeout_seconds=None):
    """
    Resolve o problema da mochila usando branch and bound.
    Retorna: (melhor_valor, melhor_solucao, tempo_execucao, sucesso)
    """
    def _executar():
        solver = bnb.BranchAndBound()
        
        pesos = [item[0] for item in itens]
        volumes = [item[1] for item in itens]
        valores = [item[2] for item in itens]
        
        inicio = time.time()
        melhor_valor, melhor_solucao = solver.resolver(W, V, pesos, volumes, valores)
        tempo = time.time() - inicio
        
        return melhor_valor, melhor_solucao, tempo
    
    if timeout_seconds:
        resultado, sucesso = executar_com_timeout(_executar, timeout_seconds)
        if sucesso:
            valor, solucao, tempo = resultado
            return valor, solucao, tempo, True
        else:
            return None, None, timeout_seconds, False
    else:
        valor, solucao, tempo = _executar()
        return valor, solucao, tempo, True

def resolver_dinamico(W, V, itens, timeout_seconds=None):
    """
    Resolve o problema com programação dinâmica
    Retorna: (melhor_valor, melhor_solucao, tempo_execucao, sucesso)
    """
    def _executar():
        n = len(itens)
        
        pesos = [0] + [item[0] for item in itens]
        volumes = [0] + [item[1] for item in itens]
        valores = [0] + [item[2] for item in itens]
        
        inicio = time.time()
        melhor_valor, melhor_solucao = din.dinamico(W, V, n, pesos, volumes, valores)
        tempo = time.time() - inicio
        
        return melhor_valor, melhor_solucao, tempo
    
    if timeout_seconds:
        resultado, sucesso = executar_com_timeout(_executar, timeout_seconds)
        if sucesso:
            valor, solucao, tempo = resultado
            return valor, solucao, tempo, True
        else:
            return None, None, timeout_seconds, False
    else:
        valor, solucao, tempo = _executar()
        return valor, solucao, tempo, True

def testar_instancia(caminho_arquivo, resolver_func, nome_algoritmo):
    """Testa uma única instância com o algoritmo especificado."""
    print(f"\nTestando: {caminho_arquivo}")
    
    W, V, itens = ler_instancia(caminho_arquivo)
    
    print(f"Capacidade da mochila: W={W}, V={V}")
    print(f"Número de itens: {len(itens)}")
    
    valor, solucao, tempo, sucesso = resolver_func(W, V, itens)
    
    if not sucesso:
        print(f"TIMEOUT ou ERRO DE MEMÓRIA após {tempo}s")
        return None, None, tempo
    
    # Calcular peso e volume totais da solução
    peso_total = sum(itens[i][0] for i in range(len(solucao)) if solucao[i])
    volume_total = sum(itens[i][1] for i in range(len(solucao)) if solucao[i])
    itens_selecionados = [i for i in range(len(solucao)) if solucao[i]]
    
    print(f"Melhor valor encontrado: {valor}")
    print(f"Peso total: {peso_total}/{W}")
    print(f"Volume total: {volume_total}/{V}")
    print(f"Itens selecionados: {itens_selecionados}")
    print(f"Quantidade de itens: {len(itens_selecionados)}")
    print(f"Tempo de execução: {tempo:.7f}s")
    
    return valor, solucao, tempo

def main():
    # Dicionário de algoritmos disponíveis
    algoritmos = {
        '1': (resolver_backtracking, 'Backtracking'),
        '2': (resolver_branch_and_bound, 'Branch and Bound'),
        '3': (resolver_dinamico, 'Programação Dinâmica')
    }
    
    # Verifica se foi passado argumento na linha de comando
    if len(sys.argv) > 1:
        escolha = sys.argv[1]
    else:
        # Menu interativo
        print("=== ESCOLHA O ALGORITMO ===")
        print("1 - Backtracking")
        print("2 - Branch and Bound")
        print("3 - Programação Dinâmica")
        escolha = input("Digite o número do algoritmo: ")
    
    if escolha not in algoritmos:
        print("Opção inválida!")
        return
    
    resolver_func, nome_algoritmo = algoritmos[escolha]
    
    print(f"\n=== TESTE DO {nome_algoritmo.upper()} ===")
    
    # Instâncias de teste
    instancias = [
        "../instancias/W200_V200/instancia_n30.txt",
        # "../instancias/W100_V50/instancia_n100.txt",
        # "../instancias/W50_V100/instancia_n30.txt",  # Descomente com cuidado
    ]
    
    resultados = []
    
    for instancia in instancias:
        try:
            valor, solucao, tempo = testar_instancia(instancia, resolver_func, nome_algoritmo)
            resultados.append((instancia, valor, tempo))
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {instancia}")
            print("Execute primeiro: python3 gerador_instancias.py 50 100")
        except KeyboardInterrupt:
            print("\n\nExecução interrompida pelo usuário!")
            break
    
    print(f"\n=== RESUMO - {nome_algoritmo.upper()} ===")
    for inst, val, t in resultados:
        print(f"{inst}: Valor={val}, Tempo={t:.6f}s")

if __name__ == "__main__":
    main()