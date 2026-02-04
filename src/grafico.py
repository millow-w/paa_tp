# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # ===== CONFIGURAÇÃO =====
# # No arquivo src/grafico.py, mude para:
# csv_path = "../resultados/resultados_N10_V400_variando_W.csv"
# saida_dir = "graficos"
# nome_figura = "tempo_vs_W_N10_V400.png"

# os.makedirs(saida_dir, exist_ok=True)

# # ===== LEITURA =====
# df = pd.read_csv(csv_path)

# # Converter colunas numéricas
# df["W"] = pd.to_numeric(df["W"])
# df["Tempo_Medio"] = pd.to_numeric(df["Tempo_Medio"])

# # Ordenar por W
# df = df.sort_values("W")

# # ===== GRÁFICO =====
# plt.figure(figsize=(8, 5))

# for algoritmo in df["Algoritmo"].unique():
#     dados = df[df["Algoritmo"] == algoritmo]
#     plt.plot(
#         dados["W"],
#         dados["Tempo_Medio"],
#         marker="o",
#         linewidth=2,
#         label=algoritmo
#     )
# # plt.yscale('log')
# plt.xlabel("Capacidade W")
# plt.ylabel("Tempo médio de execução (s)")
# plt.title("Tempo de execução × Capacidade W (N = 10, V = 400)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()

# # ===== SALVAR =====
# plt.savefig(os.path.join(saida_dir, nome_figura), dpi=300)
# plt.close()

# print(f"Gráfico salvo em: {saida_dir}/{nome_figura}")


import pandas as pd
import matplotlib.pyplot as plt
import os

# ===== CONFIGURAÇÃO =====
csv_path = "../resultados3/resultados_W120_V130.csv"
saida_dir = "graficos"
nome_figura = "segundoset_tempo_vs_N_W120_V130.png"

os.makedirs(saida_dir, exist_ok=True)

# ===== LEITURA =====
df = pd.read_csv(csv_path)
df["N_Itens"] = pd.to_numeric(df["N_Itens"])
df["Tempo_Medio"] = pd.to_numeric(df["Tempo_Medio"])
df = df.sort_values("N_Itens")

# ===== GRÁFICO =====
plt.figure(figsize=(10, 6))

for algoritmo in df["Algoritmo"].unique():
    dados = df[df["Algoritmo"] == algoritmo]
    plt.plot(
        dados["N_Itens"],
        dados["Tempo_Medio"],
        marker="o",
        linewidth=2,
        label=algoritmo.replace('_', ' ')
    )

plt.yscale('log') # Essencial para visualizar a diferença exponencial
plt.xlabel("Número de Itens (N)", fontsize=12)
plt.ylabel("Tempo médio de execução (s) [Escala Log]", fontsize=12)
plt.title("Impacto do Número de Itens no Tempo de Execução\n(W=120, V=130 fixos)", fontsize=14)
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout()

# ===== SALVAR =====
plt.savefig(os.path.join(saida_dir, nome_figura), dpi=300)
print(f"Gráfico salvo em: {saida_dir}/{nome_figura}")