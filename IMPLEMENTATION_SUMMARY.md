# Implementation Summary - Knapsack Algorithm Improvements

## ✅ Completed Changes

### 1. **Branch and Bound Algorithm - Improved Bounding Function**

- **File**: [src/algoritmos/branch_and_bound.py](src/algoritmos/branch_and_bound.py)
- **Changes**:
  - Implemented fractional relaxation bound instead of naive optimistic sum
  - Added item sorting by value density: `valor / min(peso_normalizado, volume_normalizado)`
  - Greedy packing with fractional item addition for tighter upper bounds
  - Solution mapping back to original item order
- **Impact**: Much more effective pruning, reducing search space significantly

### 2. **Timeout Protection System**

- **File**: [src/utils.py](src/utils.py)
- **Changes**:
  - Added `TimeoutError` exception class
  - Implemented `executar_com_timeout()` using `signal.alarm()` (Linux/Unix)
  - Handles both timeout and `MemoryError` gracefully
  - Returns tuple `(result, success_flag)`

### 3. **Algorithm Resolver Functions**

- **File**: [src/experimentos.py](src/experimentos.py)
- **Changes**:
  - Updated all three resolvers: `resolver_backtracking`, `resolver_branch_and_bound`, `resolver_dinamico`
  - Added `timeout_seconds` parameter (optional, defaults to None)
  - Return signature changed from `(valor, solucao, tempo)` to `(valor, solucao, tempo, sucesso)`
  - Wrapped execution in timeout handler
  - Updated `testar_instancia()` to handle timeout results

### 4. **Benchmark System Overhaul**

- **File**: [src/benchmark.py](src/benchmark.py)
- **Changes**:
  - ✅ Added `argparse` with `--timeout` flag (default: 300s)
  - ✅ Added `--pastas` flag for custom folder selection
  - ✅ Changed iterations from 1 to **10** for statistical validity
  - ✅ **Removed hardcoded Backtracking skip** at n>30
  - ✅ Early exit on first timeout/memory error (skips remaining iterations)
  - ✅ Logs warnings: `⚠️ TIMEOUT/MEMORY ERROR: {algorithm} n={n} W={W} V={V}`
  - ✅ Only saves CSV rows if at least 1 successful execution
  - ✅ Logs skipped instances: `❌ SKIPPED: {algorithm} n={n} (nenhuma execução bem-sucedida)`

### 5. **Academic Comparison Graphs**

- **File**: [src/analise_resultados.py](src/analise_resultados.py)
- **New Function**: `plotar_comparacao_tres_algoritmos()`
- **Features**:
  - Generates **separate PNG per (W,V) configuration**
  - Log-scale y-axis for time comparison
  - Shows mean execution time with shaded standard deviation regions
  - Academic styling: serif font, clear labels, professional colors
  - Complexity annotations: "Dynamic Programming O(nWV)", "Backtracking O(2^n)", etc.
  - Integrated into `main()` analysis pipeline

---

## 🚀 Usage

### Running Benchmarks

```bash
# Basic usage (default: 300s timeout, default folders)
cd /home/tliuth/Documents/25.2/PAA/paa_tp/src
python3 benchmark.py

# Custom timeout (e.g., 600 seconds = 10 minutes)
python3 benchmark.py --timeout 600

# Custom folders
python3 benchmark.py --pastas W20_V30 W50_V100 W100_V100

# Both custom timeout and folders
python3 benchmark.py --timeout 120 --pastas W30_V40 W70_V100
```

### Generating Analysis and Graphs

```bash
cd /home/tliuth/Documents/25.2/PAA/paa_tp/src
python3 analise_resultados.py
```

This will generate:

- Standard analysis graphs in `src/graficos/`
- **Academic comparison graphs**: `comparacao_academica_W{X}_V{Y}.png` for each configuration

### Testing Individual Instances

```bash
cd /home/tliuth/Documents/25.2/PAA/paa_tp/src
python3 experimentos.py
```

---

## 📊 Expected Behavior

### Timeout Handling

1. **First iteration timeout**: Immediately stops and skips remaining 9 iterations
2. **Logs warning**: Console output shows which (algorithm, n, W, V) timed out
3. **Partial results saved**: If iterations 1-5 succeed but 6 times out, saves results from 1-5
4. **CSV filtering**: Only includes rows with at least 1 successful execution

### Statistical Output

- **10 iterations per instance** (unless timeout occurs)
- Mean and standard deviation calculated from successful runs
- Provides robust data for academic analysis

### Graph Characteristics

- **Log-scale y-axis**: Shows exponential vs polynomial growth clearly
- **Shaded regions**: Standard deviation for confidence visualization
- **Separate files**: One PNG per (W,V) for focused presentation
- **Publication-ready**: High DPI (300), professional styling

---

## 🧪 Testing

Run the timeout test:

```bash
cd /home/tliuth/Documents/25.2/PAA/paa_tp
python3 test_timeout.py
```

Expected output:

```
✓ Test 1 (10s timeout, n=10): Completes successfully
✓ Test 2 (1s timeout, n=40): Times out correctly
✓ Test 3 (no timeout, n=10): Completes successfully
```

---

## 📁 File Structure

```
src/
├── algoritmos/
│   ├── branch_and_bound.py    ← Improved bound function
│   ├── backtracking.py
│   └── dinamico.py
├── utils.py                    ← New: timeout wrapper
├── experimentos.py             ← Updated: timeout support
├── benchmark.py                ← Major updates: argparse, 10 iter, logging
├── analise_resultados.py       ← New: academic comparison function
├── graficos/                   ← Output directory for graphs
└── resultados/                 ← Output directory for CSV files
```

---

## 🎯 Key Improvements Summary

| Aspect             | Before              | After                                   |
| ------------------ | ------------------- | --------------------------------------- |
| **B&B Bound**      | Weak optimistic sum | Fractional relaxation with sorting      |
| **Timeout**        | Hardcoded n>30 skip | Configurable timeout (default 300s)     |
| **Iterations**     | 1 per instance      | 10 per instance (early-exit on timeout) |
| **Error Handling** | None                | Timeout + MemoryError caught            |
| **Logging**        | Minimal             | Detailed warnings for timeouts/skips    |
| **CSV Output**     | All rows            | Only successful executions              |
| **Graphs**         | Basic               | Academic-quality comparison plots       |
| **CLI**            | Hardcoded config    | argparse with --timeout and --pastas    |

---

## ⚠️ Notes

1. **Timeout uses `signal.alarm()`**: Linux/Unix only (won't work on Windows)
2. **Memory errors**: Caught and treated like timeouts (dynamic programming may hit memory limits on large W×V)
3. **Partial results**: If 5/10 iterations succeed, statistics calculated from those 5
4. **Graph gaps**: Points omitted where algorithms timed out (shows tendency with available data)

---

## 🎓 Academic Presentation Tips

1. **Show log-scale graphs**: Clearly demonstrates exponential vs polynomial complexity
2. **Highlight shaded regions**: Shows consistency/variability of measurements
3. **Compare growth rates**: Dynamic Programming remains flat while Backtracking/B&B curve up
4. **Discuss timeout points**: Where algorithms become impractical (e.g., Backtracking at n>40)
5. **B&B improvement**: Compare old vs new B&B performance if you have old data

---

All implementations tested and working correctly! ✅
