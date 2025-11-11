import re
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


# ===========================================
# 🔹 Quantum Logic Core
# ===========================================

def quantum_classic_compare(value, threshold, op):
    """Simulate simple qubit-based logic (classical mode using qubits)."""
    qc = QuantumCircuit(1)
    if (
        (op == ">" and value > threshold)
        or (op == "<" and value < threshold)
        or (op == ">=" and value >= threshold)
        or (op == "<=" and value <= threshold)
        or (op == "==" and value == threshold)
        or (op == "!=" and value != threshold)
    ):
        qc.x(0)  # flip to |1⟩ if condition true

    state = Statevector.from_instruction(qc)
    probs = np.abs(state.data) ** 2
    return 1 if probs[1] > 0.5 else 0


def quantum_amplitude_logic(value: float, conditions: list) -> float:
    """Simulate quantum logic using amplitude superposition (QAmplitude)."""
    n = len(conditions)
    qc = QuantumCircuit(n)

    # Superposition all qubits
    qc.h(range(n))

    # Apply Z phase if condition is True
    for i, (op, thr) in enumerate(conditions):
        cond = (
            (op == ">" and value > thr)
            or (op == "<" and value < thr)
            or (op == ">=" and value >= thr)
            or (op == "<=" and value <= thr)
            or (op == "==" and value == thr)
            or (op == "!=" and value != thr)
        )
        if cond:
            qc.z(i)

    # Add quantum interference (simulate logical coupling)
    for i in range(n - 1):
        qc.cx(i, i + 1)

    qc.h(range(n))
    state = Statevector.from_instruction(qc)
    probs = np.abs(state.data) ** 2
    return float(np.mean(probs))


# ===========================================
# 🔹 Quantum Table
# ===========================================

class QuantumTable:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []

    def insert(self, values):
        self.rows.append(values)
        print(f"✅ Inserted {values} into {self.name}")

    # --- Classic Qubit Mode ---
    def quantum_select_classic(self, col, op, threshold):
        idx = self.columns.index(col)
        results = []
        for row in self.rows:
            v = float(row[idx])
            if quantum_classic_compare(v, threshold, op):
                results.append(row)
        return results

    # --- Quantum Amplitude Mode ---
    def quantum_select_amplitude(self, col, logic_ops):
        print("🧠 Quantum Amplitude Probabilities:")
        idx = self.columns.index(col)
        results = []
        for row in self.rows:
            v = float(row[idx])
            p = quantum_amplitude_logic(v, logic_ops)
            results.append((row, p))
            print(f"   {row} → P={p:.2f}")
        return results


# ===========================================
# 🔹 Quantum SQL Server
# ===========================================

class QuantumSQLServer:
    def __init__(self):
        self.databases = {}
        self.current_db = None
        print("⚛️ QuantumSQL v4.9r3 — Interference Logic Engine ready")

    def execute(self, sql: str):
        sql = sql.strip()
        cmd = sql.split()[0].upper()

        # --- CREATE DATABASE ---
        if cmd == "CREATE" and "DATABASE" in sql.upper():
            name = sql.split()[-1]
            self.databases[name] = {}
            self.current_db = name
            print(f"✅ Database '{name}' created.")

        # --- CREATE TABLE ---
        elif cmd == "CREATE" and "TABLE" in sql.upper():
            m = re.match(r"CREATE TABLE (\w+) \((.+)\)", sql, re.I)
            if not m:
                print("❌ Syntax error in CREATE TABLE.")
                return
            tname, cols = m.groups()
            cols = [c.strip() for c in cols.split(",")]
            self.databases[self.current_db][tname] = QuantumTable(tname, cols)
            print(f"✅ Table '{tname}' created with columns {cols}")

        # --- INSERT ---
        elif cmd == "INSERT":
            m = re.match(r"INSERT INTO (\w+) VALUES \((.+)\)", sql, re.I)
            if not m:
                print("❌ Syntax error in INSERT.")
                return
            tname, values = m.groups()
            vals = [v.strip().strip("'") for v in values.split(",")]
            self.databases[self.current_db][tname].insert(vals)

        # --- SELECT ---
        elif cmd == "SELECT":
            m = re.match(r"SELECT \* FROM (\w+) WHERE (.+)", sql, re.I)
            if not m:
                print("❌ Syntax error in SELECT.")
                return
            tname, cond = m.groups()
            tb = self.databases[self.current_db][tname]

            # Quantum Amplitude Mode
            if any(q in cond.upper() for q in ["QAND", "QOR", "QNOT"]):
                print("🧠 Quantum SELECT (Amplitude Mode):")
                pattern = r"(\w+)\s*(>=|<=|==|!=|>|<)\s*([\d\.]+)"
                found = re.findall(pattern, cond)
                if not found:
                    print("❌ No valid conditions found.")
                    return
                logic_ops = [(op, float(thr)) for (_, op, thr) in found]
                tb.quantum_select_amplitude(found[0][0], logic_ops)

            # Classic Qubit Mode (supports AND / OR)
            elif " and " in cond.lower() or " or " in cond.lower():
                print("🧠 Quantum SELECT (Classic Qubit Mode):")
                parts = re.split(r"\band\b|\bor\b", cond, flags=re.I)
                operators = re.findall(r"\b(and|or)\b", cond, flags=re.I)
                results = tb.rows
                mask = set()

                for i, part in enumerate(parts):
                    m2 = re.match(r"(\w+)\s*(>=|<=|==|!=|>|<)\s*(\d+)", part.strip())
                    if not m2:
                        continue
                    col, op, val = m2.groups()
                    val = float(val)
                    sub_result = tb.quantum_select_classic(col, op, val)
                    sub_set = set(tuple(r) for r in sub_result)

                    if i == 0:
                        mask = sub_set
                    else:
                        if operators[i - 1].lower() == "and":
                            mask &= sub_set
                        else:
                            mask |= sub_set

                final = [list(r) for r in mask]
                print(f"🧠 Classic Qubit Logic Results ({cond}): {len(final)} matches")
                for r in final:
                    print("  ", r)

            else:
                print("🧠 Quantum SELECT (Classic Qubit Mode):")
                m2 = re.match(r"(\w+)\s*(>=|<=|==|!=|>|<)\s*(\d+)", cond)
                if not m2:
                    print("❌ Unsupported condition.")
                    return
                col, op, val = m2.groups()
                res = tb.quantum_select_classic(col, op, float(val))
                print(f"🧠 Classic Qubit Logic Results ({cond}): {len(res)} matches")
                for r in res:
                    print("  ", r)
