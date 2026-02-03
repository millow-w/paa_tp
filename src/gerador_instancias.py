import random
import os
import sys
from pathlib import Path

diretorio_projeto = Path(__file__).resolve().parent.parent
base_path = os.path.join(diretorio_projeto, "instancias")

def gerar_instancia(n, W, V, nome_arquivo):
    """Gera uma única instância seguindo o formato do trabalho."""
    with open(nome_arquivo, 'w') as f:
        f.write(f"{W}\t{V}\n")
        
        for _ in range(n):
            # Itens com peso e volume proporcionais à mochila
            # peso = random.randint(1, max(2, W // 4))
            peso = random.randint(1, 10)
            # volume = random.randint(1, max(2, V // 4))
            volume = random.randint(1, 10)
            valor = random.randint(10, 100)
            f.write(f"{peso}\t{volume}\t{valor}\n")

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 gerador_instancias.py <peso_max> <volume_max>")
        sys.exit(1)

    W = int(sys.argv[1])
    V = int(sys.argv[2])
    
    # Queremos uma instância para cada um destes tamanhos
    lista_n = [10, 12, 14, 16, 18, 20, 22, 24, 26, 30]

    # Criamos uma pasta única para esse conjunto de testes
    nome_pasta = f"W{W}_V{V}"
    pasta_caminho = os.path.join(base_path, nome_pasta)

    print(nome_pasta)

    print(pasta_caminho)

    if not os.path.exists(pasta_caminho):
        os.makedirs(pasta_caminho)

    print(f"Gerando instâncias variando N de 10 a 100 em: {nome_pasta}")
    
    for n in lista_n:
        nome_arq = os.path.join(pasta_caminho, f"instancia_n{n}.txt")
        gerar_instancia(n, W, V, nome_arq)

    print("\nConcluído! Você tem 10 arquivos, cada um com um número diferente de itens.")

if __name__ == "__main__":
    main()