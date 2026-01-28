import os

def ler_instancia(caminho_arquivo):
    """
    Lê o arquivo de instância e retorna as capacidades e a lista de itens.
    Formato esperado:
    W \t V
    peso \t volume \t valor
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            # Lê a primeira linha e remove espaços/quebras de linha extras
            linha_capacidades = f.readline().strip()
            if not linha_capacidades:
                return None
            
            # Separa W e V por tabulação 
            W, V = map(int, linha_capacidades.split('\t'))
            
            itens = []
            for linha in f:
                linha = linha.strip()
                if linha:
                    # Cada item tem peso, volume e valor [cite: 7, 9]
                    dados = list(map(int, linha.split('\t')))
                    itens.append(tuple(dados))
            
            return W, V, itens
            
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None

def salvar_resultado(caminho_arquivo, lucro, itens_selecionados, tempo_execucao):
    """
    Opcional: Salva a saída conforme exigido pelo trabalho.
    """
    with open(caminho_arquivo, 'w') as f:
        f.write(f"Lucro Máximo: {lucro}\n")
        f.write(f"Tempo de Execução: {tempo_execucao:.6f}s\n")
        f.write("Itens (Peso, Volume, Valor):\n")
        for item in itens_selecionados:
            f.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")