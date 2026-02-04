import pandas as pd
import ast
from scipy.stats import ttest_rel

def teste_t_por_instancia(csv_path, alg1, alg2, alpha=0.05):
    df = pd.read_csv(csv_path)

    # Agrupa por instância (W, V, N)
    grupos = df.groupby(['Capacidade_W', 'Capacidade_V', 'N_Itens'])

    print(f"\nComparação: {alg1} vs {alg2}\n")

    for (W, V, N), grupo in grupos:
        linha1 = grupo[grupo['Algoritmo'] == alg1]
        linha2 = grupo[grupo['Algoritmo'] == alg2]

        # Só testa se os dois algoritmos existem nessa instância
        if linha1.empty or linha2.empty:
            continue

        tempos1 = ast.literal_eval(linha1.iloc[0]['Tempos_10_Execucoes'])
        tempos2 = ast.literal_eval(linha2.iloc[0]['Tempos_10_Execucoes'])

        t, p = ttest_rel(tempos1, tempos2)

        print(f"W={W}, V={V}, N={N}")
        print(f"  t = {t:.4f}")
        print(f"  p-valor = {p:.6e}")

        if p <= alpha:
            print("  ➡ Diferença estatisticamente significativa\n")
        else:
            print("  ➡ Empate estatístico\n")

teste_t_por_instancia(
    "../resultados/resultados_N10_V400_variando_W.csv",
    "Branch_and_Bound",
    "Backtracking"
)
