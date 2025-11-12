from quntam_sql import QuantumSQL
import numpy as np

# =============================================================
# 🧪 Example
# =============================================================
if __name__ == "__main__":
    rows = [
        ["P1", 120, 36.7, 0],
        ["P2", 110, 37.0, 1],
        ["P3", 95, 36.5, 0],
        ["P4", 140, 38.2, 1],
        ["P5", 125, 37.5, 0],
        ["P6", 128, 39.1, 1],
        ["P7", 122, 36.8, 0],
        ["P8", 99, 37.9, 1],
        ["P9", 130, 38.8, 0],
        ["P10", 115, 37.0, 0],
    ]

    qsql = QuantumSQL(["id", "bp", "temp", "fever"])
    probs, result = qsql.run_query(rows, "(BP BETWEEN 100 AND 130) OR (TEMP > 38 AND NOT FEVER)")

    print("\n🔹 Final normalized probability vector:\n", np.round(probs, 4))
    print("\n✅ QuantumSQL v7.4 complete.")
