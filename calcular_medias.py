#!/usr/bin/env python3
"""
Calcula tempos médios de execução por algoritmo e tamanho n (média sobre todos os pares W,V)
Com extrapolação assintótica para valores de n ausentes
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def extrapolar_assintotico(n_observados, tempo_observados, n_faltantes, algoritmo):
    """
    Extrapola comportamento assintótico para valores de n ausentes
    
    - Backtracking/B&B: ajuste exponencial O(2^n) -> t = a * 2^(b*n) + c
    - Dinâmico: ajuste polinomial O(n^k) -> t = a * n^k + b
    """
    if len(n_observados) < 2:
        return None  # Não há dados suficientes para extrapolação
    
    try:
        if algoritmo in ['Backtracking', 'Branch_and_Bound']:
            # Modelo exponencial: t = a * 2^(b*n) + c
            def modelo_exp(n, a, b, c):
                return a * np.power(2.0, b * n) + c
            
            # Usar apenas últimos pontos para melhor ajuste da tendência
            n_fit = n_observados[-min(4, len(n_observados)):]
            t_fit = tempo_observados[-min(4, len(tempo_observados)):]
            
            # Chute inicial mais inteligente
            p0 = [t_fit[0] / (2 ** n_fit[0]), 1.0, 0.0]
            popt, _ = curve_fit(modelo_exp, n_fit, t_fit, p0=p0, maxfev=10000)
            
            tempos_extrapolados = modelo_exp(np.array(n_faltantes), *popt)
            return tempos_extrapolados
            
        else:  # Dinâmico
            # Modelo polinomial: t = a * n^k + b
            def modelo_poly(n, a, k, b):
                return a * np.power(n, k) + b
            
            # Chute inicial
            p0 = [tempo_observados[-1] / (n_observados[-1] ** 2), 2.0, 0.0]
            popt, _ = curve_fit(modelo_poly, n_observados, tempo_observados, p0=p0, maxfev=10000)
            
            tempos_extrapolados = modelo_poly(np.array(n_faltantes), *popt)
            return tempos_extrapolados
            
    except Exception as e:
        print(f"   ⚠️  Falha na extrapolação para {algoritmo}: {e}")
        return None

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
    
    # Determinar todos os valores de n presentes no dataset
    todos_n = sorted(df_resultado['N_Itens'].unique())
    
    # Plotar cada algoritmo
    for algoritmo in sorted(df_resultado['Algoritmo'].unique()):
        dados = df_resultado[df_resultado['Algoritmo'] == algoritmo].sort_values('N_Itens')
        
        n_presentes = dados['N_Itens'].values
        tempo = dados['Tempo_Medio'].values
        tempo_std = dados['Tempo_Std'].values
        
        estilo = estilos[algoritmo]
        nome = nomes_display[algoritmo]
        
        # Plotar dados observados (linha sólida com marcadores)
        ax.plot(n_presentes, tempo, 
               color=estilo['color'],
               marker=estilo['marker'],
               markersize=8,
               linestyle=estilo['linestyle'],
               linewidth=estilo['linewidth'],
               label=nome,
               alpha=0.9,
               zorder=3)
        
        # Região de desvio padrão
        ax.fill_between(n_presentes,
                       np.maximum(tempo - tempo_std, 1e-8),
                       tempo + tempo_std,
                       color=estilo['color'],
                       alpha=0.15,
                       zorder=1)
        
        # Identificar valores de n faltantes
        n_faltantes = [n for n in todos_n if n not in n_presentes]
        
        if len(n_faltantes) > 0 and len(n_presentes) >= 2:
            # Fazer extrapolação
            tempos_extrapolados = extrapolar_assintotico(n_presentes, tempo, n_faltantes, algoritmo)
            
            if tempos_extrapolados is not None:
                # Plotar linha pontilhada extrapolada
                ax.plot(n_faltantes, tempos_extrapolados,
                       color=estilo['color'],
                       linestyle=':',
                       linewidth=2.0,
                       alpha=0.6,
                       zorder=2,
                       label=f'{nome} (extrapolado)')
                
                # Adicionar marcadores vazios para os pontos extrapolados
                ax.scatter(n_faltantes, tempos_extrapolados,
                          marker=estilo['marker'],
                          s=80,
                          facecolors='none',
                          edgecolors=estilo['color'],
                          linewidths=2,
                          alpha=0.6,
                          zorder=2)
    
    # Configuração dos eixos
    ax.set_xlabel('Número de itens (n)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Tempo de execução (segundos)', fontweight='bold', fontsize=13)

    
    # Escala logarítmica para melhor visualização do comportamento exponencial
    ax.set_yscale('log')
    
    # Grid
    ax.grid(True, which='major', linestyle='-', alpha=0.3, linewidth=0.8)
    ax.grid(True, which='minor', linestyle=':', alpha=0.2, linewidth=0.5)
    
    # Legenda
    ax.legend(loc='upper left', frameon=True, shadow=True, fancybox=True, fontsize=10)
    
    # Adicionar nota explicativa sobre extrapolação
    nota = (f"Nota: Linhas pontilhadas com marcadores vazios representam extrapolação\n"
            f"assintótica baseada nos dados observados (dados reais com marcadores preenchidos).")
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
            
            # Calcular média APENAS dos testes que funcionaram (ignorando ausentes)
            # Isso evita viés, já que testes faltantes não devem impactar a tendência geral
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
                'Tempo_Std': tempo_std if not pd.isna(tempo_std) else 0.0,
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
