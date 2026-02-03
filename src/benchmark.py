import os
import csv
from pathlib import Path
import statistics
import argparse
import time
from utils import ler_instancia
from experimentos import (
    resolver_backtracking,
    resolver_branch_and_bound,
    resolver_dinamico
)

diretorio_projeto = Path(__file__).resolve().parent.parent
diretorio_base = os.path.join(diretorio_projeto, "instancias")

def rodar_benchmark(pastas_escolhidas, timeout_seconds=120):

    print(diretorio_base)

    diretorio_resultados = "resultados"

    # Cria a pasta resultados se não existir
    os.makedirs(diretorio_resultados, exist_ok=True)

    algoritmos = {
        'Dinamico': resolver_dinamico,
        'Backtracking': resolver_backtracking,
        'Branch_and_Bound': resolver_branch_and_bound
    }
    
    # Contar total de testes para progresso
    total_instancias = 0
    for pasta in pastas_escolhidas:
        caminho_pasta = os.path.join(diretorio_base, pasta)
        if os.path.isdir(caminho_pasta):
            arquivos = [a for a in os.listdir(caminho_pasta) if a.endswith('.txt')][:10]
            total_instancias += len(arquivos)
    
    total_testes = total_instancias * len(algoritmos)
    teste_atual = 0
    inicio_benchmark = time.time()
    
    print(f"\n{'='*80}")
    print(f"BENCHMARK INICIADO")
    print(f"{'='*80}")
    print(f"Configuração:")
    print(f"  - Timeout por execução: {timeout_seconds}s")
    print(f"  - Iterações por teste: 10 (ou até timeout)")
    print(f"  - Pastas: {', '.join(pastas_escolhidas)}")
    print(f"  - Total de instâncias: {total_instancias}")
    print(f"  - Total de testes: {total_testes}")
    print(f"{'='*80}\n")

    for pasta in pastas_escolhidas:
        caminho_pasta = os.path.join(diretorio_base, pasta)
        if not os.path.isdir(caminho_pasta):
            print(f"Pasta {pasta} não encontrada, pulando...")
            continue

        w_cap = pasta.split('_')[0].replace('W', '')
        v_cap = pasta.split('_')[1].replace('V', '')

        # Nome do CSV específico dessa pasta W_V
        nome_csv = f"resultados_W{w_cap}_V{v_cap}.csv"
        caminho_csv = os.path.join(diretorio_resultados, nome_csv)

        with open(caminho_csv, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow([
                'Capacidade_W', 'Capacidade_V', 'N_Itens', 'Algoritmo',
                'Tempo_Medio', 'Tempo_Std',
                'Valor_Medio', 'Valor_Std',
                'Tempos_10_Execucoes',
                'Valores_10_Execucoes'
            ])

            # Apenas 10 instâncias por pasta
            arquivos = sorted([
                a for a in os.listdir(caminho_pasta)
                if a.endswith('.txt')
            ])[:10]

            for arquivo in arquivos:
                n_itens = arquivo.split('_n')[1].replace('.txt', '')
                caminho_instancia = os.path.join(caminho_pasta, arquivo)

                W, V, itens = ler_instancia(caminho_instancia)

                for nome_alg, func_resolver in algoritmos.items():
                    teste_atual += 1
                    tempo_decorrido = time.time() - inicio_benchmark
                    tempo_medio_por_teste = tempo_decorrido / teste_atual if teste_atual > 0 else 0
                    eta_segundos = tempo_medio_por_teste * (total_testes - teste_atual)
                    eta_minutos = eta_segundos / 60
                    
                    print(f"\n[{teste_atual}/{total_testes}] {pasta}/{arquivo} - {nome_alg}")
                    print(f"  └─ n={n_itens}, W={w_cap}, V={v_cap} | ETA: {eta_minutos:.1f}min | Decorrido: {tempo_decorrido/60:.1f}min")
                    
                    tempos = []
                    valores = []

                    for iteracao in range(1):
                        print(f"     Iteração {iteracao+1}/10...", end=" ", flush=True)
                        valor, solucao, tempo, sucesso = func_resolver(W, V, itens, timeout_seconds)
                        
                        if not sucesso:
                            # Log do timeout/erro de memória
                            print(f"\n     ⚠️  TIMEOUT/MEMORY ERROR (iteração {iteracao+1}/10)")
                            break  # Sai do loop de iterações
                        
                        print(f"✓ {tempo:.3f}s", flush=True)
                        tempos.append(tempo)
                        valores.append(valor)
                    
                    # Só salva se houver pelo menos 1 execução bem-sucedida
                    if len(tempos) > 0:
                        media_tempo = statistics.mean(tempos)
                        print(f"     ✅ Completo: {len(tempos)} iterações, tempo médio={media_tempo:.3f}s, valor={statistics.mean(valores):.0f}")
                        writer.writerow([
                            w_cap,
                            v_cap,
                            n_itens,
                            nome_alg,
                            f"{media_tempo:.7f}",
                            f"{statistics.stdev(tempos):.7f}" if len(tempos) > 1 else 0,
                            statistics.mean(valores),
                            statistics.stdev(valores) if len(valores) > 1 else 0,
                            tempos,
                            valores
                        ])
                    else:
                        print(f"     ❌ SKIPPED (nenhuma execução bem-sucedida)")

        print(f"\n{'='*80}")
        print(f"✔ Resultados salvos em {caminho_csv}")
        print(f"{'='*80}\n")
    
    tempo_total = time.time() - inicio_benchmark
    print(f"\n{'='*80}")
    print(f"BENCHMARK CONCLUÍDO")
    print(f"{'='*80}")
    print(f"Tempo total: {tempo_total/60:.2f} minutos ({tempo_total:.0f}s)")
    print(f"Testes completados: {total_testes}")
    print(f"Tempo médio por teste: {tempo_total/total_testes:.2f}s")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rodar benchmark dos algoritmos de mochila')
    parser.add_argument('--timeout', type=int, default=120, 
                        help='Timeout em segundos para cada execução (padrão: 120)')
    parser.add_argument('--pastas', nargs='+', 
                        help='Pastas específicas para testar (ex: W30_V40 W50_V100)')
    
    args = parser.parse_args()
    
    # Usar pastas especificadas ou padrão
    if args.pastas:
        pastas_escolhidas = args.pastas
    else:
        pastas_escolhidas = [
            "W20_V30",
            "W20_V40",
            "W30_V40",
            "W50_V70",
            "W80_V80",
            "W80_V100",
            "W80_V120",
            "W100_V150",
        ]
    
    print(f"Configuração: timeout={args.timeout}s, pastas={pastas_escolhidas}")
    rodar_benchmark(pastas_escolhidas, timeout_seconds=args.timeout)
