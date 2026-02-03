#!/usr/bin/env python3
"""
Gera gráficos comparativos para configurações específicas de capacidade
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plotar_configuracao(df_config, w_cap, v_cap, output_path):
    """
    Plota gráfico comparativo para uma configuração específica de capacidade
    """
    # Configuração do estilo
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 11
    
    # Cores e estilos por algoritmo
    estilos = {
        'Backtracking': {'color': '#D32F2F', 'marker': 's', 'linestyle': '--', 'linewidth': 2.5},
        'Branch_and_Bound': {'color': '#1976D2', 'marker': '^', 'linestyle': '-.', 'linewidth': 2.5},
        'Dinamico': {'color': '#2E7D32', 'marker': 'o', 'linestyle': '-', 'linewidth': 2.5}
    }
    
    nomes_display = {
        'Backtracking': 'Backtracking O(2ⁿ)',
        'Branch_and_Bound': 'Branch & Bound O(2ⁿ)',
        'Dinamico': 'Dynamic Programming O(n·W·V)'
    }
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plotar cada algoritmo
    for algoritmo in sorted(df_config['Algoritmo'].unique()):
        dados = df_config[df_config['Algoritmo'] == algoritmo].sort_values('N_Itens')
        
        if len(dados) == 0:
            continue
            
        n = dados['N_Itens'].values
        tempo = dados['Tempo_Medio'].values
        tempo_std = dados['Tempo_Std'].values
        
        estilo = estilos.get(algoritmo, {'color': 'gray', 'marker': 'o', 'linestyle': '-', 'linewidth': 2.5})
        nome = nomes_display.get(algoritmo, algoritmo)
        
        # Linha principal com marcadores
        ax.plot(n, tempo, 
               color=estilo['color'],
               marker=estilo['marker'],
               markersize=8,
               linestyle=estilo['linestyle'],
               linewidth=estilo['linewidth'],
               label=nome,
               alpha=0.9)
        
        # Região de desvio padrão
        if tempo_std.max() > 0:
            ax.fill_between(n,
                           np.maximum(tempo - tempo_std, 1e-8),
                           tempo + tempo_std,
                           color=estilo['color'],
                           alpha=0.15)
    
    # Configuração dos eixos
    ax.set_xlabel('Número de itens (n)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Tempo de execução (segundos)', fontweight='bold', fontsize=13)
    ax.set_title(f'Comparação de Desempenho Algorítmico\nMochila 2D (W={w_cap}, V={v_cap})',
                fontweight='bold', fontsize=14, pad=20)
    
    # Escala linear
    # ax.set_yscale('log')  # Descomente para escala logarítmica
    
    # Grid
    ax.grid(True, which='major', linestyle='-', alpha=0.3, linewidth=0.8)
    ax.grid(True, which='minor', linestyle=':', alpha=0.2, linewidth=0.5)
    
    # Legenda
    ax.legend(loc='upper left', frameon=True, shadow=True, fancybox=True, fontsize=11)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Gráfico salvo em: {output_path}")
    plt.close()

def gerar_graficos_especificos():
    pasta_resultados = Path('resultados')
    
    # Configurações desejadas
    configs = [
        ('W20_V30', '20', '30'),
        ('W100_V150', '100', '150')
    ]
    
    print("=" * 80)
    print("GERANDO GRÁFICOS PARA CONFIGURAÇÕES ESPECÍFICAS")
    print("=" * 80)
    print()
    
    for nome_config, w_cap, v_cap in configs:
        arquivo = pasta_resultados / f'resultados_{nome_config}.csv'
        
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            print(f"   Pulando {nome_config}...\n")
            continue
        
        print(f"📊 Processando {nome_config} (W={w_cap}, V={v_cap})...")
        
        # Carregar dados
        df = pd.read_csv(arquivo)
        
        # Estatísticas por algoritmo
        print(f"   Algoritmos encontrados:")
        for algoritmo in sorted(df['Algoritmo'].unique()):
            dados_alg = df[df['Algoritmo'] == algoritmo]
            n_instancias = len(dados_alg)
            tempo_medio = dados_alg['Tempo_Medio'].mean()
            print(f"      - {algoritmo:20s}: {n_instancias} instâncias, tempo médio={tempo_medio:.6f}s")
        
        # Gerar gráfico
        output_path = pasta_resultados / f'comparacao_{nome_config}.png'
        plotar_configuracao(df, w_cap, v_cap, output_path)
        print()
    
    print("=" * 80)
    print("✅ GRÁFICOS GERADOS COM SUCESSO")
    print("=" * 80)

if __name__ == '__main__':
    gerar_graficos_especificos()
