# ============================================================
# ⚛️ QuantumSQL v4.8 — Superposition Logic Engine
# Dual Logic: Classic (Boolean) + Quantum Amplitude Logic
# ============================================================
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.library import SaveStatevector
import numpy as np
import re
from enum import Enum


# ------------------------------------------------------------
# 🧩 Logic Mode Enum
# ------------------------------------------------------------
class QuantumLogicMode(Enum):
    CLASSIC = 1
    AMPLITUDE = 2


# ------------------------------------------------------------
# ⚙️ Helper: Safe quantum-style compare
# ------------------------------------------------------------
def quantum_compare(val1, val2, op: str) -> int:
    if op == ">":
        return int(val1 > val2)
    elif op == "<":
        return int(val1 < val2)
    elif op == ">=":
        return int(val1 >= val2)
    elif op == "<=":
        return int(val1 <= val2)
    elif op == "==":
        return int(val1 == val2)
    elif op == "!=":
        return int(val1 != val2)
    else:
        raise ValueError(f"Unknown operator: {op}")


# ------------------------------------------------------------
# ⚛️ Quantum Operators (QAND / QOR)
# ------------------------------------------------------------
def QAND(qc: QuantumCircuit, qubits: list[int]):
    """Quantum AND via multi-controlled Toffoli"""
    if len(qubits) < 2:
        return
    qc.mcx(qubits[:-1], qubits[-1])


def QOR(qc: QuantumCircuit, qubits: list[int]):
    """Quantum OR via CX fusion"""
    if len(qubits) < 2:
        return
    for i in qubits[:-1]:
        qc.cx(i, qubits[-1])


def QNOT(qc: QuantumCircuit, qubit: int):
    qc.x(qubit)


# ------------------------------------------------------------
# ⚛️ Quantum Superposition Evaluation
# ------------------------------------------------------------
def simulate_amplitude_logic(n_qubits: int, conditions: list[tuple[str, float, str]], row_value: float):
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))  # superposition state

    # Condition qubits correspond to each condition
    for i, (op, threshold, _) in enumerate(conditions):
        result = quantum_compare(row_value, threshold, op)
        if result == 1:
            qc.x(i)  # mark true as |1⟩

    # Combine all condition qubits by their logical operators
    for i, (_, _, logic) in enumerate(conditions[:-1]):
        if logic == "QAND":
            QAND(qc, [i, i + 1])
        elif logic == "QOR":
            QOR(qc, [i, i + 1])

    # ✅ เพิ่มบรรทัดนี้เพื่อให้ simulator เก็บ statevector
    qc.append(SaveStatevector(len(qc.qubits)), qc.qubits)

    backend = AerSimulator(method="statevector")
    job = backend.run(transpile(qc, backend))
    result = job.result()

    # ✅ ดึง statevector อย่างถูกต้อง
    state = result.data(0)["statevector"]
    probs = np.abs(state) ** 2
    p_match = float(np.sum(probs[len(probs)//2:]))  # amplitude in |1> sector
    return p_match



# ------------------------------------------------------------
# 📦 Table class
# ------------------------------------------------------------
class QuantumTable:
    def __init__(self, name: str, columns: list[str]):
        self.name = name
        self.columns = columns
        self.rows = []

    def insert(self, row: list[str]):
        self.rows.append(row)
        print(f"✅ Inserted {row} into {self.name}")

    # -------------------------------
    # Classic Logic Mode
    # -------------------------------
    def quantum_select_classic(self, cond_func):
        matches = [r for r in self.rows if cond_func(r)]
        return matches

    # -------------------------------
    # Amplitude Logic Mode
    # -------------------------------
    def quantum_select_amplitude(self, colname: str, logic_conditions: list[tuple[str, float, str]]):
        idx = self.columns.index(colname)
        results = []
        for r in self.rows:
            val = float(r[idx])
            p = simulate_amplitude_logic(len(logic_conditions) + 1, logic_conditions, val)
            results.append((r, p))
        return results


# ------------------------------------------------------------
# 🧠 QuantumSQLServer
# ------------------------------------------------------------
class QuantumSQLServer:
    def __init__(self):
        self.databases = {}
        self.current_db = None
        self.logic_mode = QuantumLogicMode.CLASSIC
        print("⚛️ QuantumSQL v4.8 — Dual Logic Engine ready")

    def set_logic_mode(self, mode: QuantumLogicMode):
        self.logic_mode = mode

    def execute(self, sql: str):
        sql = sql.strip()

        # Detect database creation
        if sql.upper().startswith("CREATE DATABASE"):
            dbname = sql.split()[-1]
            self.databases[dbname] = {}
            self.current_db = dbname
            print(f"✅ Database '{dbname}' created.")
            return

        # Detect table creation
        if sql.upper().startswith("CREATE TABLE"):
            m = re.search(r"TABLE (\w+)", sql, re.I)
            if m is None:
                return
            name = m.group(1)
            cols = re.findall(r"\((.*?)\)", sql)[0].split(",")
            cols = [c.strip() for c in cols]
            self.databases[self.current_db][name] = QuantumTable(name, cols)
            print(f"✅ Table '{name}' created with columns {cols}")
            return

        # Detect insert
        if sql.upper().startswith("INSERT INTO"):
            m = re.search(r"INSERT INTO (\w+).*VALUES\s*\((.*?)\)", sql, re.I)
            if m is None:
                return
            name, values = m.group(1), m.group(2)
            values = [v.strip().strip("'") for v in values.split(",")]
            tb = self.databases[self.current_db][name]
            tb.insert(values)
            return

        # Detect SELECT
        if sql.upper().startswith("SELECT"):
            return self._handle_select(sql)

    # --------------------------------------------------------
    # Handle SELECT (detect logic mode)
    # --------------------------------------------------------
    def _handle_select(self, sql: str):
        m = re.search(r"FROM (\w+)", sql, re.I)
        if not m:
            print("❌ Syntax error: missing FROM <table> in SELECT.")
            return
        tb_name = m.group(1)
        tb = self.databases[self.current_db][tb_name]

        where = re.search(r"WHERE (.*)", sql, re.I)
        condition_str = where.group(1).strip() if where else ""

        # auto mode detection
        if "QAND" in condition_str or "QOR" in condition_str:
            self.logic_mode = QuantumLogicMode.AMPLITUDE
        else:
            self.logic_mode = QuantumLogicMode.CLASSIC

        if self.logic_mode == QuantumLogicMode.CLASSIC:
            print("\n🧠 Quantum SELECT (Classic Logic Mode):")
            def cond_func(row):
                env = {c: float(row[i]) if row[i].replace('.', '', 1).isdigit() else row[i]
                       for i, c in enumerate(tb.columns)}
                return eval(condition_str, {}, env)

            matches = tb.quantum_select_classic(cond_func)
            print(f"🧠 Combined matches: {len(matches)} rows")
            for m in matches:
                print("   ", m)
            return matches

        elif self.logic_mode == QuantumLogicMode.AMPLITUDE:
            print("\n🧠 Quantum SELECT (Superposition Logic Mode):")
            logic_conditions = self._parse_amplitude_conditions(condition_str)
            colname = logic_conditions[0][0]
            ops = [(op, val, logic) for (_, val, logic, op) in logic_conditions]
            results = tb.quantum_select_amplitude(colname, ops)

            print("🧠 Amplitude probabilities:")
            for r, p in results:
                print(f"   {r} → P={p:.2f}")
            return results
    # --------------------------------------------------------
    # Parse condition string for amplitude mode (safe version)
    # --------------------------------------------------------
    def _parse_amplitude_conditions(self, cond_str: str):
        # 🔹 จับกลุ่มเงื่อนไขเช่น "bp > 100", "bp <= 140", "bp == 95"
        cond_pattern = r"(\w+)\s*(==|!=|>=|<=|>|<)\s*([\d\.]+)"
        logic_pattern = r"\b(QAND|QOR|QNOT)\b"

        conditions = []
        logic_ops = re.findall(logic_pattern, cond_str)
        conds = re.findall(cond_pattern, cond_str)

        if not conds:
            print("❌ Parse error: no valid quantum condition found.")
            return []

        # 🔹 รวมแต่ละ condition กับ logic ต่อท้าย
        for i, (col, op, val) in enumerate(conds):
            next_logic = logic_ops[i] if i < len(logic_ops) else None
            conditions.append((col, float(val), next_logic, op))

        # Debug-print logic tree
        print("🧩 Parsed Quantum Conditions:")
        for c in conditions:
            print(f"   {c}")
        return conditions
