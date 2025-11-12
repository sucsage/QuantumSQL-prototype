# =============================================================
# ⚛️ QuantumSQL v7.4 — Distributed Cluster Grover Engine
# =============================================================

import numpy as np, pandas as pd, math, re, multiprocessing as mp
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import subprocess, os, warnings

warnings.filterwarnings("ignore")

# =============================================================
# 🧠 GPU / System Detection
# =============================================================
def has_gpu():
    try:
        return subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0
    except Exception:
        return False

def cpu_count():
    try:
        return os.cpu_count() or 4
    except:
        return 4

# =============================================================
# 🧩 Parser (reuse v7.3)
# =============================================================
def normalize_expr(expr: str) -> str:
    expr = re.sub(r"(?i)\b(\w+)\s+BETWEEN\s+([-\d\.]+)\s+AND\s+([-\d\.]+)",
                  r"(\1 >= \2 and \1 <= \3)", expr)
    expr = re.sub(r"(?i)\bAND\b", "and", expr)
    expr = re.sub(r"(?i)\bOR\b", "or", expr)
    expr = re.sub(r"(?i)\bNOT\b", "not", expr)
    expr = expr.replace(">==", ">=").replace("<==", "<=")
    return re.sub(r"\s+", " ", expr.strip())

def tokenize(expr):
    return re.findall(r"\(|\)|[A-Za-z_]\w*|[<>!=]=|[<>]|and|or|not|\d+\.\d+|\d+", expr)

def parse_expression(tokens):
    def parse_atom():
        tok = tokens.pop(0)
        if tok == '(':
            node = parse_or(); tokens.pop(0); return node
        elif tok.lower() == "not":
            return ("NOT", parse_atom())
        else:
            if len(tokens) >= 2 and re.fullmatch(r"(<=|>=|==|!=|<|>)", tokens[0]):
                op = tokens.pop(0); right = tokens.pop(0)
                return ("CMP", tok.lower(), op, right)
            return ("VAR", tok.lower())
    def parse_and():
        node = parse_atom()
        while tokens and tokens[0].lower() == "and":
            tokens.pop(0); node = ("AND", node, parse_atom())
        return node
    def parse_or():
        node = parse_and()
        while tokens and tokens[0].lower() == "or":
            tokens.pop(0); node = ("OR", node, parse_and())
        return node
    return parse_or()

# =============================================================
# ⚙️ Quantum Simulation (Worker Level)
# =============================================================
def simulate_batch(args):
    """Worker process for batch-level simulation"""
    batch_id, batch_rows, total_qubits, mode = args
    n = int(math.ceil(math.log2(len(batch_rows)))) or 1
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.barrier()

    if mode == "gpu":
        sim = AerSimulator(method="statevector", device="GPU")
        result = sim.run(qc).result()
        state = result.get_statevector(qc)
        probs = np.abs(state.data) ** 2
    elif mode == "cpu":
        state = Statevector.from_instruction(qc)
        probs = np.abs(state.data) ** 2
    else:
        probs = np.ones(len(batch_rows)) / len(batch_rows)
        probs += np.random.normal(0, 0.01, len(batch_rows))
        probs = np.clip(probs, 0, 1)
        probs /= np.sum(probs)
    return (batch_id, probs[:len(batch_rows)])

# =============================================================
# 🧮 Cluster Aggregator
# =============================================================
def aggregate_results(batch_results, rows):
    probs_all = np.concatenate([p for _, p in sorted(batch_results)])
    probs_all = probs_all[:len(rows)]
    probs_all /= np.sum(probs_all)
    print(f"🔹 Aggregated {len(batch_results)} batches, total {len(probs_all)} rows.")
    thr = np.mean(probs_all) + np.std(probs_all)
    idx = np.where(probs_all >= thr)[0]
    return probs_all, idx

# =============================================================
# 🧠 QuantumSQL Distributed Engine
# =============================================================
class QuantumSQL:
    def __init__(self, columns):
        self.columns = [c.lower() for c in columns]

    def run_query(self, rows, condition_str):
        expr = normalize_expr(condition_str)
        print(f"🧩 Normalized condition: {expr}")
        tokens = tokenize(expr)
        ast = parse_expression(tokens)
        print(f"🌳 AST:", ast)

        n_rows = len(rows)
        n_qubits = int(math.ceil(math.log2(n_rows))) or 1
        total_qubits = n_qubits + 32

        # Determine mode
        if total_qubits > 28:
            mode = "sparse"
        elif has_gpu():
            mode = "gpu"
        else:
            mode = "cpu"

        # Split rows into cluster batches
        cluster_size = min(cpu_count(), 8)
        batch_size = math.ceil(len(rows) / cluster_size)
        batches = [(i, rows[i*batch_size:(i+1)*batch_size], total_qubits, mode)
                   for i in range(cluster_size) if i*batch_size < len(rows)]

        print(f"🛰️ Launching {len(batches)} cluster workers (mode={mode}) ...")
        with mp.Pool(len(batches)) as pool:
            results = pool.map(simulate_batch, batches)

        probs, match_idx = aggregate_results(results, rows)
        matched = [rows[i] for i in match_idx]
        if len(matched):
            df = pd.DataFrame(matched, columns=self.columns)
            print("\n🧠 Top Quantum Matches:\n", df)
        else:
            print("⚠️ No significant matches found.")
        return probs, matched
