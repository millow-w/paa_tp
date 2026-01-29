import time
from utils import ler_instancia
import algoritmos.backtracking as bt

def resolver_backtracking(W, V, itens):
    """
    Resolve o problema da mochila usando backtracking.
    Retorna: (melhor_valor, tempo_execucao)
    """
    bt.melhor_valor = 0
        
    n = len(itens)
    vetor = [False] * n  # Vetor de decisões (incluir ou não cada item)
    
    # Extrai pesos, volumes e valores dos itens
    pesos = [item[0] for item in itens]
    volumes = [item[1] for item in itens]
    valores = [item[2] for item in itens]
    
    inicio = time.time()
    bt.backtrack(vetor, 0, n, W, V, pesos, volumes, valores, 0, 0)
    tempo = time.time() - inicio
    
    return bt.melhor_valor, tempo

def testar_instancia(caminho_arquivo):
    """Testa uma única instância."""
    print(f"\nTestando: {caminho_arquivo}")
    
    W, V, itens = ler_instancia(caminho_arquivo)
    
    print(f"Capacidade da mochila: W={W}, V={V}")
    print(f"Número de itens: {len(itens)}")
    
    valor, tempo = resolver_backtracking(W, V, itens)
    
    print(f"Melhor valor encontrado: {valor}")
    print(f"Tempo de execução: {tempo:.7f}s")
    
    return valor, tempo

def main():
    # Testa com instâncias pequenas primeiro
    print("=== TESTE DO BACKTRACKING ===")
    
    # Começa com instâncias pequenas (n=10, n=20)
    instancias = [
        "../instancias/W50_V100/instancia_n10.txt",
        "../instancias/W50_V100/instancia_n20.txt",
        # "../instancias/W50_V100/instancia_n30.txt",  # Descomente com cuidado
    ]
    
    resultados = []
    
    for instancia in instancias:
        try:
            valor, tempo = testar_instancia(instancia)
            resultados.append((instancia, valor, tempo))
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {instancia}")
            print("Execute primeiro: python3 gerador_instancias.py 50 100")
    
    print("\n=== RESUMO ===")
    for inst, val, t in resultados:
        print(f"{inst}: Valor={val}, Tempo={t:.6f}s")

if __name__ == "__main__":
    main()