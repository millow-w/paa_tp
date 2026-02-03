#!/usr/bin/env python3
"""
Calcula tempos médios de execução por algoritmo e tamanho n (média sobre todos os pares W,V)
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plotar_comparacao(df_resultado):
    """
    Plota gráfico comparativo dos tempos de execução por algoritmo
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
    
    # Determinar número total de configurações esperadas
    n_configs_total = df_resultado['N_Configuracoes'].max()
    
    # Plotar cada algoritmo
    for algoritmo in sorted(df_resultado['Algoritmo'].unique()):
        dados = df_resultado[df_resultado['Algoritmo'] == algoritmo].sort_values('N_Itens')
        
        n = dados['N_Itens'].values
        tempo = dados['Tempo_Medio'].values
        tempo_std = dados['Tempo_Std'].values
        n_configs = dados['N_Configuracoes'].values
        
        estilo = estilos[algoritmo]
        nome = nomes_display[algoritmo]
        
        # Separar dados completos e incompletos
        completos = n_configs == n_configs_total
        incompletos = n_configs < n_configs_total
        
        # Plotar dados completos (linha sólida)
        if np.any(completos):
            ax.plot(n[completos], tempo[completos], 
                   color=estilo['color'],
                   marker=estilo['marker'],
                   markersize=8,
                   linestyle=estilo['linestyle'],
                   linewidth=estilo['linewidth'],
                   label=nome,
                   alpha=0.9)
            
            # Região de desvio padrão para dados completos
            ax.fill_between(n[completos],
                           np.maximum(tempo[completos] - tempo_std[completos], 1e-8),
                           tempo[completos] + tempo_std[completos],
                           color=estilo['color'],
                           alpha=0.15)
        
        # Plotar dados incompletos (marcadores vazios, mais transparentes)
        if np.any(incompletos):
            ax.plot(n[incompletos], tempo[incompletos], 
                   color=estilo['color'],
                   marker=estilo['marker'],
                   markersize=8,
                   markerfacecolor='none',
                   markeredgewidth=2,
                   linestyle=':',
                   linewidth=1.5,
                   label=f'{nome} (parcial)' if not np.any(completos) else '',
                   alpha=0.5)
            
            # Adicionar anotações para pontos incompletos
            for i in np.where(incompletos)[0]:
                ax.annotate(f'{n_configs[i]}/{n_configs_total}',
                           xy=(n[i], tempo[i]),
                           xytext=(5, 5),
                           textcoords='offset points',
                           fontsize=8,
                           color=estilo['color'],
                           alpha=0.7)
    
    # Configuração dos eixos
    ax.set_xlabel('Número de itens (n)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Tempo de execução (segundos)', fontweight='bold', fontsize=13)

    
    # Escala linear (removida escala logarítmica para melhor visualização do crescimento)
    # ax.set_yscale('log')
    
    # Grid
    ax.grid(True, which='major', linestyle='-', alpha=0.3, linewidth=0.8)
    ax.grid(True, which='minor', linestyle=':', alpha=0.2, linewidth=0.5)
    
    # Legenda
    ax.legend(loc='upper left', frameon=True, shadow=True, fancybox=True, fontsize=11)
    
    # Adicionar nota explicativa sobre dados parciais
    nota = (f"Nota: Marcadores vazios indicam dados incompletos devido a timeouts.\n"
            f"Número mostra configurações completadas (ex.: 4/{n_configs_total} = 4 de {n_configs_total} configurações de capacidade).")
    ax.text(0.98, 0.02, nota,
           transform=ax.transAxes,
           fontsize=9,
           verticalalignment='bottom',
           horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    output_path = 'resultados/comparacao_tempos_por_n.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Gráfico salvo em: {output_path}")
    plt.close()

def calcular_medias():
    pasta_resultados = Path('resultados')
    arquivos = sorted(pasta_resultados.glob('resultados_*.csv'))
    
    # Carregar todos os dados
    todos_dados = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo)
        todos_dados.append(df)
    
    df_completo = pd.concat(todos_dados, ignore_index=True)
    
    print("=" * 80)
    print("TEMPOS MÉDIOS DE EXECUÇÃO POR TAMANHO N E ALGORITMO")
    print("(média entre todas as configurações de capacidade W e V)")
    print("=" * 80)
    print()
    
    # Agrupar por N_Itens e Algoritmo
    resultado = []
    
    for n in sorted(df_completo['N_Itens'].unique()):
        print(f"📊 Tamanho n = {n}")
        print(f"   {'─' * 72}")
        
        dados_n = df_completo[df_completo['N_Itens'] == n]
        
        for algoritmo in sorted(dados_n['Algoritmo'].unique()):
            dados_alg = dados_n[dados_n['Algoritmo'] == algoritmo]
            
            tempo_medio = dados_alg['Tempo_Medio'].mean()
            tempo_std = dados_alg['Tempo_Medio'].std()
            tempo_min = dados_alg['Tempo_Medio'].min()
            tempo_max = dados_alg['Tempo_Medio'].max()
            n_configs = len(dados_alg)
            
            print(f"   {algoritmo:20s}: {tempo_medio:10.6f}s ± {tempo_std:8.6f}s  "
                  f"(min: {tempo_min:.6f}s, max: {tempo_max:.6f}s, configs: {n_configs})")
            
            resultado.append({
                'N_Itens': n,
                'Algoritmo': algoritmo,
                'Tempo_Medio': tempo_medio,
                'Tempo_Std': tempo_std,
                'Tempo_Min': tempo_min,
                'Tempo_Max': tempo_max,
                'N_Configuracoes': n_configs
            })
        
        print()
    
    # Criar DataFrame resultado
    df_resultado = pd.DataFrame(resultado)
    
    # Tabela resumo final por algoritmo
    print("=" * 80)
    print("RESUMO GERAL POR ALGORITMO (média global sobre todos n e capacidades)")
    print("=" * 80)
    print()
    
    for algoritmo in sorted(df_resultado['Algoritmo'].unique()):
        dados_alg = df_resultado[df_resultado['Algoritmo'] == algoritmo]
        tempo_medio_geral = dados_alg['Tempo_Medio'].mean()
        print(f"   {algoritmo:20s}: {tempo_medio_geral:10.6f}s")
    
    print()
    print("=" * 80)
    
    # Salvar CSV resumo
    df_resultado.to_csv('resultados/resumo_tempos_por_n.csv', index=False)
    print("✅ Resumo salvo em: resultados/resumo_tempos_por_n.csv")
    print("=" * 80)
    
    # Plotar gráfico comparativo
    print("\n📊 Gerando gráfico comparativo...")
    plotar_comparacao(df_resultado)

if __name__ == '__main__':
    calcular_medias()
