import os
import signal

class TimeoutError(Exception):
    """Exceção customizada para timeout"""
    pass

def _timeout_handler(signum, frame):
    """Handler para o sinal de timeout"""
    raise TimeoutError("Execução excedeu o tempo limite")

def executar_com_timeout(func, timeout_seconds, *args, **kwargs):
    """
    Executa uma função com timeout usando signal.alarm (Linux/Unix).
    
    Args:
        func: Função a ser executada
        timeout_seconds: Tempo limite em segundos
        *args, **kwargs: Argumentos para a função
    
    Returns:
        (resultado, sucesso): tupla onde sucesso é True se completou, False se timeout/erro
    """
    # Configurar handler de timeout
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_seconds)
    
    try:
        resultado = func(*args, **kwargs)
        signal.alarm(0)  # Cancelar o alarme
        signal.signal(signal.SIGALRM, old_handler)  # Restaurar handler anterior
        return (resultado, True)
    except TimeoutError:
        signal.alarm(0)  # Cancelar o alarme
        signal.signal(signal.SIGALRM, old_handler)
        return (None, False)
    except MemoryError:
        signal.alarm(0)  # Cancelar o alarme
        signal.signal(signal.SIGALRM, old_handler)
        return (None, False)
    except Exception as e:
        signal.alarm(0)  # Cancelar o alarme
        signal.signal(signal.SIGALRM, old_handler)
        raise e  # Re-raise outras exceções

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