import os
import csv
import statistics
from utils import ler_instancia
from experimentos import (
    resolver_backtracking,
    resolver_branch_and_bound,
    resolver_dinamico
)

def rodar_benchmark(pastas_escolhidas):
    diretorio_base = "../instancias/"
    diretorio_resultados = "resultados"

    # Cria a pasta resultados se não existir
    os.makedirs(diretorio_resultados, exist_ok=True)

    algoritmos = {
        'Dinamico': resolver_dinamico,
        'Backtracking': resolver_backtracking,
        'Branch_and_Bound': resolver_branch_and_bound
    }

    for pasta in pastas_escolhidas:
        caminho_pasta = os.path.join(diretorio_base, pasta)
        if not os.path.isdir(caminho_pasta):
            print(f"Pasta {pasta} não encontrada, pulando...")
            continue

        w_cap = pasta.split('_')[0].replace('W', '')
        v_cap = pasta.split('_')[1].replace('V', '')

        # Nome do CSV específico dessa pasta W_V
        nome_csv = f"resultados_W{w_cap}_V{v_cap}.csv"
        caminho_csv = os.path.join(diretorio_resultados, nome_csv)

        with open(caminho_csv, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow([
                'Capacidade_W', 'Capacidade_V', 'N_Itens', 'Algoritmo',
                'Tempo_Medio', 'Tempo_Std',
                'Valor_Medio', 'Valor_Std',
                'Tempos_10_Execucoes',
                'Valores_10_Execucoes'
            ])

            # Apenas 10 instâncias por pasta
            arquivos = sorted([
                a for a in os.listdir(caminho_pasta)
                if a.endswith('.txt')
            ])[:10]

            for arquivo in arquivos:
                n_itens = arquivo.split('_n')[1].replace('.txt', '')
                caminho_instancia = os.path.join(caminho_pasta, arquivo)

                print(f"Processando {pasta}/{arquivo}...")

                W, V, itens = ler_instancia(caminho_instancia)

                for nome_alg, func_resolver in algoritmos.items():
                    if nome_alg == 'Backtracking' and int(n_itens) > 30:
                        continue

                    tempos = []
                    valores = []

                    for _ in range(10):
                        valor, solucao, tempo = func_resolver(W, V, itens)
                        tempos.append(tempo)
                        valores.append(valor)

                    writer.writerow([
                        w_cap,
                        v_cap,
                        n_itens,
                        nome_alg,
                        f"{statistics.mean(tempos):.7f}",
                        f"{statistics.stdev(tempos):.7f}" if len(tempos) > 1 else 0,
                        statistics.mean(valores),
                        statistics.stdev(valores) if len(valores) > 1 else 0,
                        tempos,
                        valores
                    ])

        print(f"✔ Resultados salvos em {caminho_csv}")

if __name__ == "__main__":
    pastas_escolhidas = [
        "W30_V40",
        "W50_V100",
        "W80_V80",
        "W70_V100"
    ]

    rodar_benchmark(pastas_escolhidas)
