import os
import csv
import time
import statistics
from pathlib import Path

from utils import ler_instancia
from experimentos import (
    resolver_backtracking,
    resolver_branch_and_bound,
    resolver_dinamico
)

# ================= CONFIGURAÇÃO =================

N_EXECUCOES = 10
TIMEOUT = 120
MAX_N_BACKTRACKING = 40

ALGORITMOS = {
    "Dinamico": resolver_dinamico,
    "Backtracking": resolver_backtracking,
    "Branch_and_Bound": resolver_branch_and_bound,
}

# ===============================================

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCIAS_DIR = BASE_DIR / "instancias"
RESULTADOS_DIR = BASE_DIR / "resultados"
RESULTADOS_DIR.mkdir(exist_ok=True)

def rodar_benchmark(pastas):
    for pasta in pastas:
        caminho_pasta = INSTANCIAS_DIR / pasta
        if not caminho_pasta.is_dir():
            print(f"[SKIP] Pasta {pasta} não encontrada")
            continue

        print(f"\n📂 Pasta: {pasta}")

        csv_path = RESULTADOS_DIR / f"resultados_{pasta}.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Pasta",
                "Arquivo",
                "Algoritmo",
                "N_Itens",
                "W",
                "V",
                "Tempo_Medio",
                "Tempo_Std",
                "Valor_Medio",
                "Valor_Std",
                "Tempos",
                "Valores"
            ])

            arquivos = sorted(a for a in os.listdir(caminho_pasta) if a.endswith(".txt"))

            for arquivo in arquivos:
                caminho = caminho_pasta / arquivo
                W, V, itens = ler_instancia(caminho)
                n = len(itens)

                print(f"\n📄 {arquivo} | n={n}, W={W}, V={V}")

                for nome_alg, solver in ALGORITMOS.items():
                    if nome_alg == "Backtracking" and n > MAX_N_BACKTRACKING:
                        print(f"  ⏭️  {nome_alg} (n={n} > {MAX_N_BACKTRACKING})")
                        continue

                    tempos = []
                    valores = []

                    print(f"  ▶ {nome_alg}")

                    for i in range(N_EXECUCOES):
                        valor, solucao, tempo, sucesso = solver(
                            W, V, itens, timeout_seconds=TIMEOUT
                        )

                        if not sucesso:
                            print(f"    ⚠️ timeout na execução {i+1}")
                            break

                        tempos.append(tempo)
                        valores.append(valor)

                    if tempos:
                        writer.writerow([
                            pasta,
                            arquivo,
                            nome_alg,
                            n,
                            W,
                            V,
                            statistics.mean(tempos),
                            statistics.stdev(tempos) if len(tempos) > 1 else 0,
                            statistics.mean(valores),
                            statistics.stdev(valores) if len(valores) > 1 else 0,
                            tempos,
                            valores
                        ])

                        print(f"    ✅ ok | tempo médio={statistics.mean(tempos):.4f}s")

        print(f"💾 CSV salvo em {csv_path}")

# ===================== MAIN =====================

if __name__ == "__main__":
    pastas = [
        "N10_V400_variando_W",
        "W20_V20_variando_N",
    ]

    rodar_benchmark(pastas)
