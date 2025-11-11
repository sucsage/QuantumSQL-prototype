# ⚛️ QuantumSQL v4.8 — Superposition Logic Engine

**QuantumSQL v4.8** คือระบบจำลองฐานข้อมูลเชิงควอนตัม (Quantum Database Emulator)
ที่ใช้หลักการของ **quantum superposition**, **amplitude probability** และ **quantum logic gates**
เพื่อจำลองพฤติกรรมของ SQL Query (`SELECT`, `WHERE`, `AND`, `OR`, `NOT`) ในเชิงควอนตัม

---

## 🧠 Concept Overview

### 🔹 Classical SQL

การประมวลผลแบบปกติจะใช้บิต (0/1) เพื่อระบุว่าแถวใด “เข้าเงื่อนไข” หรือ “ไม่เข้าเงื่อนไข”

```sql
SELECT * FROM patients WHERE bp > 100 AND bp < 130;
```

### ⚛️ Quantum SQL

QuantumSQL ใช้ **qubit superposition** แทนบิต  ทุกแถวของข้อมูลจะถูกแปลงเป็น “สถานะควอนตัม” (|ψ⟩) ที่มีทั้ง True/False พร้อมกัน  โดยผลลัพธ์จะได้ **probability (P)** ซึ่งบ่งบอก “ความน่าจะเป็นเชิงควอนตัม”  ที่แถวนั้นจะเป็นจริงตามเงื่อนไขที่ให้ไว้

> `P = |β|²`  คือ amplitude probability ของเงื่อนไขเป็นจริงหลังผ่านการสังเกต (measurement)

---

## 🚀 Features

| Feature                    | Description                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| 🧩 Quantum Logic Engine    | ใช้ Qiskit จำลองการทำงานของ logic (AND / OR / NOT) ด้วย quantum gates |
| 🌈 Superposition Logic     | รองรับ `QAND`, `QOR`, `QNOT` สำหรับการคำนวณแบบ superposition          |
| 💡 Amplitude Probability   | แสดงค่า P ของแต่ละแถวแทน True/False                                   |
| 🧮 Logic Tree Parser       | แปลงเงื่อนไขซ้อนกันเป็นต้นไม้เชิงตรรกะ (logic tree)                   |
| 🔄 Classical Compatibility | ทำงานร่วมกับ query SQL ปกติ (`>`, `<`, `>=`, `<=`, `==`, `!=`)        |
| ⚙️ Quantum Batch Engine    | รองรับ batch ข้อมูลจำนวนมาก (8 qubits ต่อ batch)                      |

---

## 🧪 Example

### ✅ Setup

```python
from quantum_sql import QuantumSQLServer

srv = QuantumSQLServer()
srv.create_database("hospital")

srv.execute("CREATE TABLE patients (id, name, bp)")
srv.execute("INSERT INTO patients VALUES ('P1','sage',120)")
srv.execute("INSERT INTO patients VALUES ('P2','gift',110)")
srv.execute("INSERT INTO patients VALUES ('P3','kai',95)")
srv.execute("INSERT INTO patients VALUES ('P4','mimi',140)")
```

### 🔍 Query Example

```sql
SELECT * FROM patients
WHERE (bp > 100 QAND bp < 130) QOR (bp == 95);
```

#### 🧠 Output

```
🧩 Parsed Quantum Conditions:
   ('bp', 100.0, 'QAND', '>')
   ('bp', 130.0, 'QOR', '<')
   ('bp', 95.0, None, '==')

🧠 Amplitude probabilities:
   ['P1', 'sage', '120'] → P=0.50
   ['P2', 'gift', '110'] → P=0.50
   ['P3', 'kai', '95']   → P=0.50
   ['P4', 'mimi', '140'] → P=0.50
```

---

## 🧬 Probability Meaning

| P value           | Meaning                                                   |
| ----------------- | --------------------------------------------------------- |
| **P = 1.00**      | แถวนี้เข้าเงื่อนไขแน่นอน (fully true)                     |
| **P = 0.00**      | แถวนี้ไม่เข้าเงื่อนไขแน่นอน (fully false)                 |
| **0.0 < P < 1.0** | แถวนี้อยู่ใน superposition — เข้า/ไม่เข้าเงื่อนไขพร้อมกัน |

---

## 🧠 Architecture

```
┌──────────────────────────┐
│ QuantumSQLServer         │
│ ├── Databases            │
│ ├── Tables               │
│ └── Parser + Executor    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ QuantumTable             │
│ ├── Quantum Encoding     │
│ ├── Batch Qubit Engine   │
│ ├── Logic Tree Processor │
│ └── Amplitude Calculator │
└──────────────────────────┘
```

---

## 🥮 Logic Operators

| Operator               | Classical         | Quantum Equivalent         |
| ---------------------- | ----------------- | -------------------------- |
| `AND`                  | Bitwise AND       | `QAND` → Superposition AND |
| `OR`                   | Bitwise OR        | `QOR` → Superposition OR   |
| `NOT`                  | Logical NOT       | `QNOT` → Quantum Negation  |
| `==, !=, >, <, >=, <=` | Normal Comparison | Encoded as amplitude gates |

---

## ⚙️ Quantum Backend

ใช้ Qiskit **AerSimulator (statevector method)**  หรือ `Statevector.from_instruction()` เพื่อคำนวณ amplitude โดยตรง

---

## 📊 Example Output Summary

```
🧠 Combined matches (P ≥ 0.5):
    ['P1', 'sage', 120]
    ['P2', 'gift', 110]
    ['P3', 'kai', 95]
    ['P6', 'kim', 111]
```

---

## 🧩 Future Work (v5.0 Plan)

* ใช้ **multi-register encoding** (value → binary qubits)
* เพิ่ม **Quantum Arithmetic Logic (QALU)** สำหรับเงื่อนไขซับซ้อน
* รองรับ **amplitude interference visualization**
* เพิ่มโหมด **quantum join** ระหว่างตาราง

---

## 🧾 License

MIT License © 2025 QuantumSQL Lab
Developed by **Sage (Phuket Quantum Research Initiative)**
