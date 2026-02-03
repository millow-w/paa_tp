#!/usr/bin/env python3
"""
Gera tabela LaTeX com resumo estatístico dos algoritmos
"""
import pandas as pd
from pathlib import Path

def gerar_tabela_latex():
    pasta_resultados = Path('resultados')
    arquivos = sorted(pasta_resultados.glob('resultados_*.csv'))
    
    # Carregar todos os dados
    todos_dados = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo)
        todos_dados.append(df)
    
    df_completo = pd.concat(todos_dados, ignore_index=True)
    
    print("% Tabela de Resumo Estatístico dos Algoritmos")
    print("% Gerado automaticamente")
    print()
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{Resumo estatístico dos tempos de execução por algoritmo}")
    print("\\label{tab:resumo_estatistico}")
    print("\\begin{tabular}{lcccc}")
    print("\\hline")
    print("\\textbf{Algoritmo} & \\textbf{Instâncias} & \\textbf{Tempo Médio (s)} & \\textbf{Desvio Padrão (s)} & \\textbf{Tempo Máximo (s)} \\\\")
    print("\\hline")
    
    # Calcular estatísticas por algoritmo
    algoritmos_ordem = ['Dinamico', 'Branch_and_Bound', 'Backtracking']
    nomes_latex = {
        'Dinamico': 'Programação Dinâmica',
        'Branch_and_Bound': 'Branch \\& Bound',
        'Backtracking': 'Backtracking'
    }
    
    for algoritmo in algoritmos_ordem:
        dados = df_completo[df_completo['Algoritmo'] == algoritmo]
        
        n_instancias = len(dados)
        tempo_medio = dados['Tempo_Medio'].mean()
        tempo_std = dados['Tempo_Medio'].std()
        tempo_min = dados['Tempo_Medio'].min()
        tempo_max = dados['Tempo_Medio'].max()
        
        nome = nomes_latex[algoritmo]
        
        print(f"{nome} & {n_instancias} & {tempo_medio:.6f} & {tempo_std:.6f} & {tempo_max:.6f} \\\\")
    
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
    print()
    
    # Gerar também tabela por tamanho n
    print()
    print("% Tabela de Tempos Médios por Tamanho n")
    print()
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{Tempo médio de execução por tamanho da instância (n)}")
    print("\\label{tab:tempos_por_n}")
    print("\\begin{tabular}{cccc}")
    print("\\hline")
    print("\\textbf{n} & \\textbf{Prog. Dinâmica (s)} & \\textbf{Branch \\& Bound (s)} & \\textbf{Backtracking (s)} \\\\")
    print("\\hline")
    
    for n in sorted(df_completo['N_Itens'].unique()):
        dados_n = df_completo[df_completo['N_Itens'] == n]
        
        tempos = {}
        for algoritmo in algoritmos_ordem:
            dados_alg = dados_n[dados_n['Algoritmo'] == algoritmo]
            if len(dados_alg) > 0:
                tempos[algoritmo] = dados_alg['Tempo_Medio'].mean()
            else:
                tempos[algoritmo] = None
        
        din = f"{tempos['Dinamico']:.6f}" if tempos['Dinamico'] else "---"
        bnb = f"{tempos['Branch_and_Bound']:.6f}" if tempos['Branch_and_Bound'] else "---"
        bt = f"{tempos['Backtracking']:.6f}" if tempos['Backtracking'] else "---"
        
        # Adicionar nota de rodapé para dados parciais do backtracking
        n_bt = len(dados_n[dados_n['Algoritmo'] == 'Backtracking'])
        n_total = len(dados_n[dados_n['Algoritmo'] == 'Dinamico'])
        
        if n_bt < n_total and n_bt > 0:
            bt = f"{tempos['Backtracking']:.6f}$^*$"
        
        print(f"{n} & {din} & {bnb} & {bt} \\\\")
    
    print("\\hline")
    print("\\multicolumn{4}{l}{$^*$ Dados parciais devido a timeouts (média das instâncias que completaram)} \\\\")
    print("\\end{tabular}")
    print("\\end{table}")

if __name__ == '__main__':
    gerar_tabela_latex()
