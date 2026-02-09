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
            peso = random.randint(1, max(2, W // 4))
            volume = random.randint(1, max(2, V // 4))
            valor = random.randint(10, 100)
            f.write(f"{peso}\t{volume}\t{valor}\n")

def main():
    print("=== GERADOR DE INSTÂNCIAS CUSTOMIZADO ===")
    print("1 - Variar N (W e V fixos)")
    print("2 - Variar W (N e V fixos)")
    print("3 - Variar V (N e W fixos)")
    
    opcao = input("Escolha o modo de geração: ")

    if opcao == '1':
        W = int(input("Peso total (W): "))
        V = int(input("Volume total (V): "))
        lista_valores = [10, 12, 14, 16, 18, 20, 22, 24, 26, 30]
        prefixo = f"W{W}_V{V}_variando_N"
        
    elif opcao == '2':
        n = int(input("Número de itens (N): "))
        V = int(input("Volume total (V): "))
        lista_valores = [100, 200, 400, 800, 1600, 3200]
        prefixo = f"N{n}_V{V}_variando_W"

    elif opcao == '3':
        n = int(input("Número de itens (N): "))
        W = int(input("Peso total (W): "))
        lista_valores = [100, 200, 400, 800, 1600, 3200]
        prefixo = f"N{n}_W{W}_variando_V"
    
    else:
        print("Opção inválida.")
        return

    pasta_caminho = os.path.join(base_path, prefixo)
    if not os.path.exists(pasta_caminho):
        os.makedirs(pasta_caminho)

    for val in lista_valores:
        if opcao == '1':
            nome_arq = os.path.join(pasta_caminho, f"instancia_n{val}.txt")
            gerar_instancia(val, W, V, nome_arq)
        elif opcao == '2':
            nome_arq = os.path.join(pasta_caminho, f"instancia_W{val}.txt")
            gerar_instancia(n, val, V, nome_arq)
        elif opcao == '3':
            nome_arq = os.path.join(pasta_caminho, f"instancia_V{val}.txt")
            gerar_instancia(n, W, val, nome_arq)

    print(f"\nConcluído! Instâncias geradas em: {pasta_caminho}")

if __name__ == "__main__":
    main()