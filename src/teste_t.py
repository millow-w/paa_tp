import pandas as pd
import ast
from scipy.stats import ttest_rel

ALFA = 0.05

def teste_t_por_capacidade(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Descobrimos todos os valores de W únicos no arquivo
    capacidades_w = sorted(df['W'].unique())

    for w in capacidades_w:
        print(f"\n--- Analisando Capacidade W = {w} ---")
        
        # Filtramos o dataframe para o W atual
        df_w = df[df['W'] == w]
        
        # Função interna para pegar os tempos de um algoritmo específico para este W
        def obter_tempos(alg):
            linha = df_w[df_w['Algoritmo'] == alg]
            if linha.empty:
                return None
            return ast.literal_eval(linha.iloc[0]['Tempos'])

        # Comparações
        pares = [
            ("Dinamico", "Branch_and_Bound"),
            ("Dinamico", "Backtracking"),
            ("Backtracking", "Branch_and_Bound")
        ]

        for alg1, alg2 in pares:
            t1 = obter_tempos(alg1)
            t2 = obter_tempos(alg2)

            if t1 and t2:
                estatistica, p_valor = ttest_rel(t1, t2)
                
                print(f"Comparação: {alg1} vs {alg2}")
                print(f"  t = {estatistica:.6f}")
                print(f"  p-valor = {p_valor:.8f}")

                if p_valor <= ALFA:
                    print("  ➡ Diferença estatisticamente significativa")
                else:
                    print("  ➡ Empate estatístico")
            else:
                print(f"Aviso: Dados insuficientes para comparar {alg1} vs {alg2} em W={w}")

if __name__ == "__main__":
    csv = "../resultados/resultados_N10_V400_variando_W.csv"
    teste_t_por_capacidade(csv)