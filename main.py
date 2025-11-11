from quantum_sql import QuantumSQLServer

srv = QuantumSQLServer()
srv.execute("CREATE DATABASE hospital")
srv.execute("CREATE TABLE patients (id, name, bp)")
srv.execute("INSERT INTO patients VALUES ('P1','sage',120)")
srv.execute("INSERT INTO patients VALUES ('P2','gift',110)")
srv.execute("INSERT INTO patients VALUES ('P3','kai',95)")
srv.execute("INSERT INTO patients VALUES ('P4','mimi',140)")

# ✅ Classic Logic Mode
srv.execute("SELECT * FROM patients WHERE bp > 100 and bp < 130")

# ⚛️ Quantum Amplitude Logic Mode
srv.execute("SELECT * FROM patients WHERE (bp > 100 QAND bp < 130) QOR (bp == 95)")