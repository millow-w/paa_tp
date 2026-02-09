import pandas as pd
import matplotlib.pyplot as plt
import os

# ===== CONFIGURAÇÃO =====
csv_path = "../resultados/resultados_W20_V20_variando_N.csv"
saida_dir = "graficos"
nome_figura = "tempo_vs_N_W20_V20.png"

os.makedirs(saida_dir, exist_ok=True)

# ===== LEITURA E VALIDAÇÃO =====
if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
    print(f"Erro: O arquivo {csv_path} está vazio ou não existe.")
    exit()

# O Pandas lerá automaticamente o cabeçalho: Pasta, Arquivo, Algoritmo, N_Itens, etc.
df = pd.read_csv(csv_path)

# Remover espaços em branco extras dos nomes das colunas, se houver
df.columns = df.columns.str.strip()

# ===== CONVERSÃO DE DADOS =====
# Usando 'N_Itens' conforme consta no seu CSV
df["N_Itens"] = pd.to_numeric(df["N_Itens"], errors='coerce')
df["Tempo_Medio"] = pd.to_numeric(df["Tempo_Medio"], errors='coerce')

# Remove linhas que possam ter falhado na conversão
df = df.dropna(subset=["N_Itens", "Tempo_Medio"])

# Ordenar por N para a linha do gráfico ficar contínua
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
        label=algoritmo
    )

# Escala logarítmica é essencial aqui! 
# O Backtracking chega a 66s enquanto o B&B está na casa de 10^-5.
plt.yscale('log') 

plt.xlabel("Número de Itens (N)")
plt.ylabel("Tempo Médio de Execução (s) - Escala Log")
plt.title("Desempenho dos Algoritmos: Tempo x N\n(Mochila 2D: W=20, V=20)")
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout()

# ===== SALVAR =====
caminho_final = os.path.join(saida_dir, nome_figura)
plt.savefig(caminho_final, dpi=300)
plt.close()

print(f"✅ Gráfico gerado com sucesso: {caminho_final}")

# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # ===== CONFIGURAÇÃO =====
# csv_path = "../resultados3/resultados_W120_V130.csv"
# saida_dir = "graficos"
# nome_figura = "segundoset_tempo_vs_N_W120_V130.png"

# os.makedirs(saida_dir, exist_ok=True)

# # ===== LEITURA =====
# df = pd.read_csv(csv_path)
# df["N_Itens"] = pd.to_numeric(df["N_Itens"])
# df["Tempo_Medio"] = pd.to_numeric(df["Tempo_Medio"])
# df = df.sort_values("N_Itens")

# # ===== GRÁFICO =====
# plt.figure(figsize=(10, 6))

# for algoritmo in df["Algoritmo"].unique():
#     dados = df[df["Algoritmo"] == algoritmo]
#     plt.plot(
#         dados["N_Itens"],
#         dados["Tempo_Medio"],
#         marker="o",
#         linewidth=2,
#         label=algoritmo.replace('_', ' ')
#     )

# plt.yscale('log') # Essencial para visualizar a diferença exponencial
# plt.xlabel("Número de Itens (N)", fontsize=12)
# plt.ylabel("Tempo médio de execução (s) [Escala Log]", fontsize=12)
# plt.title("Impacto do Número de Itens no Tempo de Execução\n(W=120, V=130 fixos)", fontsize=14)
# plt.legend()
# plt.grid(True, which="both", ls="-", alpha=0.5)
# plt.tight_layout()

# # ===== SALVAR =====
# plt.savefig(os.path.join(saida_dir, nome_figura), dpi=300)
# print(f"Gráfico salvo em: {saida_dir}/{nome_figura}")