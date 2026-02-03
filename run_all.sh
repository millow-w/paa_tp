#!/bin/bash
# Script completo para rodar benchmark e gerar análises

echo "=========================================="
echo "KNAPSACK ALGORITHM BENCHMARK & ANALYSIS"
echo "=========================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -d "src" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto"
    exit 1
fi

# Configurações
TIMEOUT=${1:-300}  # Primeiro argumento ou padrão 300s
FOLDERS=${2:-"W30_V40 W50_V100 W70_V100 W80_V80"}  # Segundo argumento ou padrão

echo "⚙️  Configuração:"
echo "   Timeout: ${TIMEOUT}s"
echo "   Pastas: ${FOLDERS}"
echo ""

# Executar benchmark
echo "📊 Executando benchmark..."
echo "   (Isso pode levar algum tempo dependendo do timeout e número de instâncias)"
echo ""

cd src
python3 benchmark.py --timeout $TIMEOUT --pastas $FOLDERS

if [ $? -ne 0 ]; then
    echo "❌ Erro ao executar benchmark"
    exit 1
fi

echo ""
echo "✅ Benchmark concluído!"
echo ""

# Gerar análises
echo "📈 Gerando gráficos e análises..."
python3 analise_resultados.py

if [ $? -ne 0 ]; then
    echo "❌ Erro ao gerar análises"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ PROCESSO COMPLETO!"
echo "=========================================="
echo ""
echo "📁 Resultados salvos em:"
echo "   - CSV: src/resultados/"
echo "   - Gráficos: src/graficos/"
echo ""
echo "🎓 Gráficos de comparação acadêmica:"
cd graficos
ls -1 comparacao_academica_*.png 2>/dev/null | while read file; do
    echo "   - $file"
done
cd ..

echo ""
echo "Para visualizar os gráficos:"
echo "   cd src/graficos && ls *.png"
echo ""
