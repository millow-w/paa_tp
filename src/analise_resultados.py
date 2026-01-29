#!/usr/bin/env python3
"""
Script para análise e visualização dos resultados dos experimentos.
Gera gráficos comparativos de desempenho dos algoritmos.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para evitar problemas com GUI
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def carregar_todos_resultados(pasta_resultados='resultados'):
    """Carrega todos os CSVs de resultados em um único DataFrame."""
    todos_dfs = []
    
    for arquivo in sorted(Path(pasta_resultados).glob('resultados_*.csv')):
        df = pd.read_csv(arquivo)
        todos_dfs.append(df)
    
    if not todos_dfs:
        print(f"❌ Nenhum arquivo de resultado encontrado em {pasta_resultados}/")
        return None
    
    df_completo = pd.concat(todos_dfs, ignore_index=True)
    print(f"✅ Carregados {len(df_completo)} resultados de {len(todos_dfs)} arquivos")
    return df_completo

def plotar_tempo_vs_n(df, salvar=True):
    """Gráfico: Tempo de execução vs Número de itens."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Escala linear
    for algoritmo in df['Algoritmo'].unique():
        dados = df[df['Algoritmo'] == algoritmo]
        axes[0].plot(dados['N_Itens'], dados['Tempo_Medio'], 
                    marker='o', label=algoritmo, linewidth=2)
    
    axes[0].set_xlabel('Número de Itens (n)')
    axes[0].set_ylabel('Tempo Médio (segundos)')
    axes[0].set_title('Tempo de Execução vs Número de Itens (Escala Linear)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Gráfico 2: Escala logarítmica
    for algoritmo in df['Algoritmo'].unique():
        dados = df[df['Algoritmo'] == algoritmo]
        axes[1].semilogy(dados['N_Itens'], dados['Tempo_Medio'], 
                        marker='o', label=algoritmo, linewidth=2)
    
    axes[1].set_xlabel('Número de Itens (n)')
    axes[1].set_ylabel('Tempo Médio (segundos) - Log Scale')
    axes[1].set_title('Tempo de Execução vs Número de Itens (Escala Log)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    if salvar:
        plt.savefig('analise_tempo_vs_n.png', dpi=300, bbox_inches='tight')
        print("📊 Gráfico salvo: analise_tempo_vs_n.png")
    plt.close()

def plotar_comparacao_por_capacidade(df, salvar=True):
    """Gráfico: Comparação de desempenho por capacidade (W, V)."""
    # Criar identificador de capacidade
    df['Capacidade'] = df['Capacidade_W'].astype(str) + 'x' + df['Capacidade_V'].astype(str)
    
    # Selecionar algumas capacidades representativas
    capacidades_unicas = df['Capacidade'].unique()
    n_caps = min(6, len(capacidades_unicas))
    capacidades_selecionadas = sorted(capacidades_unicas)[:n_caps]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    for idx, cap in enumerate(capacidades_selecionadas):
        if idx >= len(axes):
            break
        
        dados_cap = df[df['Capacidade'] == cap]
        
        for algoritmo in dados_cap['Algoritmo'].unique():
            dados_alg = dados_cap[dados_cap['Algoritmo'] == algoritmo]
            axes[idx].plot(dados_alg['N_Itens'], dados_alg['Tempo_Medio'],
                          marker='o', label=algoritmo, linewidth=2)
        
        axes[idx].set_xlabel('Número de Itens')
        axes[idx].set_ylabel('Tempo (s)')
        axes[idx].set_title(f'Capacidade W={cap.split("x")[0]}, V={cap.split("x")[1]}')
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True, alpha=0.3)
    
    # Ocultar eixos não utilizados
    for idx in range(len(capacidades_selecionadas), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    if salvar:
        plt.savefig('analise_por_capacidade.png', dpi=300, bbox_inches='tight')
        print("📊 Gráfico salvo: analise_por_capacidade.png")
    plt.close()

def plotar_heatmap_tempo(df, algoritmo, salvar=True):
    """Heatmap: Tempo de execução por N_Itens e Capacidade."""
    dados_alg = df[df['Algoritmo'] == algoritmo].copy()
    
    if dados_alg.empty:
        print(f"⚠️  Sem dados para algoritmo {algoritmo}")
        return
    
    # Criar pivot table
    pivot = dados_alg.pivot_table(
        values='Tempo_Medio',
        index='N_Itens',
        columns=['Capacidade_W', 'Capacidade_V'],
        aggfunc='mean'
    )
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot, annot=True, fmt='.4f', cmap='YlOrRd', 
                cbar_kws={'label': 'Tempo Médio (s)'})
    plt.title(f'Heatmap de Tempo de Execução - {algoritmo}')
    plt.xlabel('Capacidade (W, V)')
    plt.ylabel('Número de Itens')
    plt.tight_layout()
    
    if salvar:
        filename = f'heatmap_{algoritmo.lower()}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Gráfico salvo: {filename}")
    plt.close()

def plotar_speedup(df, salvar=True):
    """Gráfico: Speedup do B&B em relação ao Backtracking."""
    # Filtrar dados onde ambos algoritmos estão presentes
    df_pivot = df.pivot_table(
        values='Tempo_Medio',
        index=['Capacidade_W', 'Capacidade_V', 'N_Itens'],
        columns='Algoritmo',
        aggfunc='mean'
    ).reset_index()
    
    # Calcular speedup apenas onde Backtracking existe
    if 'Backtracking' in df_pivot.columns and 'Branch_and_Bound' in df_pivot.columns:
        df_pivot = df_pivot.dropna(subset=['Backtracking', 'Branch_and_Bound'])
        df_pivot['Speedup'] = df_pivot['Backtracking'] / df_pivot['Branch_and_Bound']
        
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(df_pivot)), df_pivot['Speedup'], color='steelblue', alpha=0.7)
        plt.axhline(y=1, color='r', linestyle='--', label='Sem ganho')
        plt.xlabel('Instância')
        plt.ylabel('Speedup (Backtracking / B&B)')
        plt.title('Speedup: Branch and Bound vs Backtracking')
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if salvar:
            plt.savefig('analise_speedup.png', dpi=300, bbox_inches='tight')
            print("📊 Gráfico salvo: analise_speedup.png")
        plt.close()
        
        print(f"\n📈 Speedup Médio: {df_pivot['Speedup'].mean():.2f}x")
        print(f"📈 Speedup Máximo: {df_pivot['Speedup'].max():.2f}x")
    else:
        print("⚠️  Dados insuficientes para calcular speedup")

def plotar_comparacao_valores(df, salvar=True):
    """Verifica se todos algoritmos encontram mesmos valores (validação)."""
    # Agrupar por instância e verificar se valores são iguais
    df_pivot = df.pivot_table(
        values='Valor_Medio',
        index=['Capacidade_W', 'Capacidade_V', 'N_Itens'],
        columns='Algoritmo',
        aggfunc='mean'
    ).reset_index()
    
    # Verificar diferenças
    algoritmos = [col for col in df_pivot.columns if col not in ['Capacidade_W', 'Capacidade_V', 'N_Itens']]
    
    if len(algoritmos) >= 2:
        df_pivot['Diff'] = df_pivot[algoritmos].max(axis=1) - df_pivot[algoritmos].min(axis=1)
        problemas = df_pivot[df_pivot['Diff'] > 0]
        
        if len(problemas) > 0:
            print(f"\n⚠️  ATENÇÃO: {len(problemas)} instâncias com valores diferentes entre algoritmos!")
            print("\nInstâncias problemáticas:")
            print(problemas[['Capacidade_W', 'Capacidade_V', 'N_Itens'] + algoritmos + ['Diff']])
        else:
            print("\n✅ Todos os algoritmos encontraram os mesmos valores ótimos!")
    
    # Gráfico de barras comparando valores
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Agrupar por instância e algoritmo para garantir alinhamento
    df_grouped = df.groupby(['Capacidade_W', 'Capacidade_V', 'N_Itens', 'Algoritmo'])['Valor_Medio'].mean().reset_index()
    
    # Selecionar algumas instâncias representativas
    instancias_unicas = df_grouped[['Capacidade_W', 'Capacidade_V', 'N_Itens']].drop_duplicates()
    amostra_instancias = instancias_unicas.sample(min(15, len(instancias_unicas)))
    
    # Filtrar apenas as instâncias da amostra
    df_plot = df_grouped.merge(amostra_instancias, on=['Capacidade_W', 'Capacidade_V', 'N_Itens'])
    df_plot = df_plot.sort_values(['N_Itens', 'Capacidade_W'])
    
    # Criar índice para as instâncias
    instancias = df_plot[['Capacidade_W', 'Capacidade_V', 'N_Itens']].drop_duplicates()
    instancias['idx'] = range(len(instancias))
    df_plot = df_plot.merge(instancias, on=['Capacidade_W', 'Capacidade_V', 'N_Itens'])
    
    x = np.arange(len(instancias))
    width = 0.25
    algoritmos = sorted(df_plot['Algoritmo'].unique())
    
    for i, algoritmo in enumerate(algoritmos):
        dados = df_plot[df_plot['Algoritmo'] == algoritmo]
        indices = dados['idx'].values
        valores = dados['Valor_Medio'].values
        ax.bar(indices + i * width, valores, width, label=algoritmo, alpha=0.8)
    
    ax.set_xlabel('Instância')
    ax.set_ylabel('Valor da Solução')
    ax.set_title('Comparação de Valores Obtidos (Amostra)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if salvar:
        plt.savefig('analise_valores.png', dpi=300, bbox_inches='tight')
        print("📊 Gráfico salvo: analise_valores.png")
    plt.close()

def gerar_tabela_resumo(df):
    """Gera tabela resumo com estatísticas por algoritmo."""
    print("\n" + "="*80)
    print("RESUMO ESTATÍSTICO POR ALGORITMO")
    print("="*80)
    
    for algoritmo in sorted(df['Algoritmo'].unique()):
        dados = df[df['Algoritmo'] == algoritmo]
        print(f"\n🔹 {algoritmo}")
        print(f"   Instâncias testadas: {len(dados)}")
        print(f"   Tempo médio: {dados['Tempo_Medio'].mean():.6f}s")
        print(f"   Tempo mínimo: {dados['Tempo_Medio'].min():.6f}s")
        print(f"   Tempo máximo: {dados['Tempo_Medio'].max():.6f}s")
        print(f"   Desvio padrão: {dados['Tempo_Medio'].std():.6f}s")
        print(f"   Valor médio obtido: {dados['Valor_Medio'].mean():.2f}")

def plotar_complexidade_empirica(df, salvar=True):
    """Analisa complexidade empírica dos algoritmos."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, algoritmo in enumerate(sorted(df['Algoritmo'].unique())):
        if idx >= 3:
            break
        
        dados = df[df['Algoritmo'] == algoritmo].sort_values('N_Itens')
        
        # Plot tempo vs n
        axes[idx].scatter(dados['N_Itens'], dados['Tempo_Medio'], 
                         alpha=0.6, s=50, label='Dados')
        
        # Ajustar curvas
        n = dados['N_Itens'].values
        t = dados['Tempo_Medio'].values
        
        if len(n) > 3:
            # Tentar ajuste exponencial para Backtracking/B&B
            if algoritmo in ['Backtracking', 'Branch_and_Bound']:
                try:
                    from scipy.optimize import curve_fit
                    def exp_func(x, a, b):
                        return a * np.exp(b * x)
                    params, _ = curve_fit(exp_func, n, t, maxfev=10000)
                    n_fit = np.linspace(n.min(), n.max(), 100)
                    axes[idx].plot(n_fit, exp_func(n_fit, *params), 
                                 'r--', label=f'Ajuste: ae^(bn)', linewidth=2)
                except:
                    pass
            
            # Ajuste polinomial para Dinâmico
            else:
                poly = np.polyfit(n, t, 2)
                p = np.poly1d(poly)
                n_fit = np.linspace(n.min(), n.max(), 100)
                axes[idx].plot(n_fit, p(n_fit), 
                             'g--', label=f'Ajuste: O(n²)', linewidth=2)
        
        axes[idx].set_xlabel('Número de Itens (n)')
        axes[idx].set_ylabel('Tempo (s)')
        axes[idx].set_title(f'Complexidade Empírica - {algoritmo}')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    if salvar:
        plt.savefig('analise_complexidade.png', dpi=300, bbox_inches='tight')
        print("📊 Gráfico salvo: analise_complexidade.png")
    plt.close()

def main():
    """Função principal."""
    print("="*80)
    print("ANÁLISE DE RESULTADOS - PROBLEMA DA MOCHILA BIDIMENSIONAL")
    print("="*80)
    
    # Carregar dados
    df = carregar_todos_resultados()
    if df is None:
        return
    
    print(f"\nAlgoritmos encontrados: {', '.join(df['Algoritmo'].unique())}")
    print(f"Faixa de n: {df['N_Itens'].min()} a {df['N_Itens'].max()}")
    print(f"Capacidades testadas: {len(df.groupby(['Capacidade_W', 'Capacidade_V']))}")
    
    # Criar pasta para gráficos
    os.makedirs('graficos', exist_ok=True)
    os.chdir('graficos')
    
    # Gerar análises
    print("\n" + "="*80)
    print("GERANDO GRÁFICOS E ANÁLISES...")
    print("="*80 + "\n")
    
    gerar_tabela_resumo(df)
    
    print("\n📊 Gerando gráfico: Tempo vs Número de Itens...")
    plotar_tempo_vs_n(df)
    
    print("\n📊 Gerando gráfico: Comparação por Capacidade...")
    plotar_comparacao_por_capacidade(df)
    
    print("\n📊 Gerando gráfico: Speedup...")
    plotar_speedup(df)
    
    print("\n📊 Gerando gráfico: Comparação de Valores...")
    plotar_comparacao_valores(df)
    
    print("\n📊 Gerando gráfico: Complexidade Empírica...")
    plotar_complexidade_empirica(df)
    
    # Heatmaps individuais
    for algoritmo in df['Algoritmo'].unique():
        print(f"\n📊 Gerando heatmap: {algoritmo}...")
        plotar_heatmap_tempo(df, algoritmo)
    
    print("\n" + "="*80)
    print("✅ ANÁLISE CONCLUÍDA!")
    print(f"📁 Gráficos salvos em: {os.getcwd()}/")
    print("="*80)

if __name__ == '__main__':
    main()
