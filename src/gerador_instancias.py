import random
import os
import sys

def gerar_instancia(n, W, V, nome_arquivo):
    """Gera uma instância seguindo o formato do trabalho[cite: 9, 11]."""
    with open(nome_arquivo, 'w') as f:
        # [cite_start]Linha 1: W e V separados por tabulação [cite: 9]
        f.write(f"{W}\t{V}\n")
        
        for _ in range(n):
            # Pesos e volumes variando entre 1 e a capacidade (ou uma fração dela)
            peso = random.randint(1, max(2, W // 2))
            volume = random.randint(1, max(2, V // 2))
            valor = random.randint(10, 100)
            # [cite_start]Itens: peso, volume e valor [cite: 9]
            f.write(f"{peso}\t{volume}\t{valor}\n")

def main():
    # Verifica se os argumentos foram passados: script.py n W V
    if len(sys.argv) < 4:
        print("Uso: python3 gerador_instancias.py <n_itens> <peso_max> <volume_max>")
        sys.exit(1)

    n = int(sys.argv[1])
    W = int(sys.argv[2])
    V = int(sys.argv[3])
    num_repeticoes = 10

    base_path = os.path.join("..", "instancias")
    nome_pasta = f"n{n}_W{W}_V{V}"
    pasta_caminho = os.path.join(base_path, nome_pasta)

    if not os.path.exists(pasta_caminho):
        os.makedirs(pasta_caminho)

    print(f"Gerando {num_repeticoes} instâncias em: {nome_pasta}")
    for i in range(1, num_repeticoes + 1):
        nome_arq = os.path.join(pasta_caminho, f"instancia_{i}.txt")
        gerar_instancia(n, W, V, nome_arq)

if __name__ == "__main__":
    main()