#!/usr/bin/env python3
"""
Script de teste rápido para verificar o funcionamento do timeout
"""
import sys
sys.path.insert(0, 'src')

from utils import ler_instancia
from experimentos import resolver_backtracking, resolver_branch_and_bound, resolver_dinamico

def test_timeout():
    print("="*80)
    print("TESTE DE TIMEOUT")
    print("="*80)
    
    # Testar com uma instância pequena com timeout curto
    instancia = "instancias/W30_V40/instancia_n10.txt"
    
    print(f"\nCarregando: {instancia}")
    W, V, itens = ler_instancia(instancia)
    print(f"W={W}, V={V}, n={len(itens)}")
    
    # Teste 1: Com timeout generoso (deve completar)
    print("\n1️⃣  Teste com timeout de 10s (deve completar):")
    valor, sol, tempo, sucesso = resolver_backtracking(W, V, itens, timeout_seconds=10)
    if sucesso:
        print(f"   ✓ Sucesso! Valor={valor}, Tempo={tempo:.4f}s")
    else:
        print(f"   ✗ Falhou (timeout/erro)")
    
    # Teste 2: Com timeout muito curto (deve dar timeout)
    print("\n2️⃣  Teste com timeout de 1s em instância maior:")
    instancia_grande = "instancias/W50_V100/instancia_n40.txt"
    W2, V2, itens2 = ler_instancia(instancia_grande)
    print(f"   Carregando: W={W2}, V={V2}, n={len(itens2)}")
    
    valor2, sol2, tempo2, sucesso2 = resolver_backtracking(W2, V2, itens2, timeout_seconds=1)
    if not sucesso2:
        print(f"   ✓ Timeout funcionou corretamente! Tempo={tempo2}s")
    else:
        print(f"   ✗ Completou (inesperado): Valor={valor2}, Tempo={tempo2:.4f}s")
    
    # Teste 3: Sem timeout (deve completar)
    print("\n3️⃣  Teste sem timeout:")
    valor3, sol3, tempo3, sucesso3 = resolver_branch_and_bound(W, V, itens, timeout_seconds=None)
    if sucesso3:
        print(f"   ✓ Sucesso! Valor={valor3}, Tempo={tempo3:.4f}s")
    
    print("\n" + "="*80)
    print("✅ TESTE CONCLUÍDO")
    print("="*80)

if __name__ == "__main__":
    test_timeout()
