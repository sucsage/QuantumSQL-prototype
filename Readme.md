# ⚛️ QuantumSQL v7.4 — Distributed Cluster Grover Engine

> **QuantumSQL** คือระบบฐานข้อมูลเชิงควอนตัม (Quantum-Relational Engine)
> ที่สามารถรันคำสั่ง SQL Logic Tree (AND / OR / NOT / BETWEEN / >= / <= / nested group)
> แล้วทำการ “สังเคราะห์เป็น Oracle” สำหรับ Quantum Search / Grover Amplification
> และจำลองการรันแบบกระจาย (Distributed Quantum Simulation) ได้โดยอัตโนมัติ

---

## 🚀 Highlights

| ฟีเจอร์ | รายละเอียด |
|----------|-------------|
| 🧠 **Full SQL Parser** | รองรับการเขียน query ในรูปแบบ `(A >= 10 AND B <= 20) OR (C > 5 AND NOT D)` |
| ⚙️ **Logic Tree Synthesizer** | แปลงเป็น Abstract Syntax Tree (AST) และสร้างวงจร Oracle อัตโนมัติ |
| 🧩 **Quantum Oracle Builder** | สร้าง comparator, variable register, และ logical phase flip สำหรับแต่ละเงื่อนไข |
| 🛰️ **Distributed Cluster Engine** | รันแบบ multi-processing หรือ GPU parallel หลาย node พร้อมกัน |
| 🧮 **Hybrid Sparse Simulation** | ถ้าจำนวน qubits เกินขีดจำกัด จะ fallback เป็นโหมด sparse hybrid โดยอัตโนมัติ |
| 📊 **Grover Diffusion Aggregation** | รวม amplitude จากหลาย batch กลับมาสร้าง probability vector สุดท้าย |
| 🔋 **Memory Safe (≤2 GB)** | สามารถจำลองได้หลายพันแถวโดยไม่ต้องใช้ memory มากเกินไป |

---

## 🧠 Architecture Overview

```
┌────────────────────────────────────────────┐
│             SQL CONDITION INPUT            │
│    e.g. (BP BETWEEN 100 AND 130)           │
│          OR (TEMP > 38 AND NOT FEVER)      │
└────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│        SQL PARSER & LOGIC TREE BUILDER     │
│      → Abstract Syntax Tree (AST)          │
└────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│           QUANTUM ORACLE SYNTHESIZER       │
│  - Comparator encoding (>, <, >=, <=, ==)  │
│  - Boolean ops (AND, OR, NOT)              │
└────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│       DISTRIBUTED CLUSTER EXECUTION        │
│   - Multiprocessing (N workers)            │
│   - GPU/CPU hybrid fallback                │
│   - Sparse simulation if qubits > 28       │
└────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│           AMPLITUDE AGGREGATION            │
│   Combine probabilities → normalized       │
│   Identify top quantum states (matches)    │
└────────────────────────────────────────────┘
```

---

## ⚙️ Installation

```bash
git clone https://github.com/yourname/QuantumSQL.git
cd QuantumSQL
pip install qiskit qiskit-aer pandas numpy
```

> 🧩 Optional: ถ้ามี GPU  
> ให้ติดตั้ง [Qiskit Aer GPU](https://qiskit.org/ecosystem/aer/stubs/qiskit_aer.AerSimulator.html#gpu-support)
> เพื่อรันแบบ statevector บน CUDA ได้โดยตรง

---

## 🧪 Example

```python
from main import QuantumSQL

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
```

---

## 🧩 Output Example

```
🧩 Normalized condition: ((BP >= 100 and BP <= 130)) or (TEMP > 38 and not FEVER)
🌳 AST: ('OR', ('AND', ('CMP', 'bp', '>=', '100'), ('CMP', 'bp', '<=', '130')),
              ('AND', ('CMP', 'temp', '>', '38'), ('NOT', ('VAR', 'fever'))))
🛰️ Launching 5 cluster workers (mode=sparse) ...
🔹 Aggregated 5 batches, total 10 rows.

🧠 Top Quantum Matches:
    id   bp  temp  fever
0  P1  120  36.7      0
1  P5  125  37.5      0
2  P7  122  36.8      0
3  P9  130  38.8      0

🔹 Final normalized probability vector:
 [0.1009 0.0991 0.1009 0.0991 0.1009 0.0991 0.1009 0.0991 0.1009 0.0991]

✅ QuantumSQL v7.4 complete.
```

---

## 💡 Developer Notes

- จำนวน qubits ทั้งหมดจะถูกจัดการอัตโนมัติตามขนาดของข้อมูล
- หาก qubits > 28 → จะสลับเข้าสู่โหมด **Sparse Hybrid Simulation**
- ถ้ามี GPU ที่รองรับ CUDA → จะใช้ `AerSimulator(device="GPU")`
- รองรับ multiprocessing สูงสุด 8 workers ต่อเครื่อง

---

## 📚 Future Roadmap

| Version | Feature | Description |
|----------|----------|-------------|
| **v7.5** | QuantumSQL Studio | Web dashboard สำหรับรัน query + ดู amplitude heatmap |
| **v8.0** | Adaptive Quantum Optimizer | Hybrid Grover + VQE engine สำหรับ noise calibration |
| **v8.5** | Quantum Neural Database | Self-learning condition inference (auto query synthesis) |

---

## 🧠 Citation

ถ้าใช้โปรเจกต์นี้ในงานวิจัย / บทความ กรุณาอ้างอิงดังนี้:

```
Sage et al., "QuantumSQL: Distributed Cluster Grover Engine for Quantum Logic Queries", 
Phuket Quantum Systems, 2025.
```

## 🧾 License

MIT License © 2025 QuantumSQL Lab
Developed by **Sage (Chalongphat naksaingsat)**
