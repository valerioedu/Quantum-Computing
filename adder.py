import qiskit_aer
import qiskit

qr = qiskit.QuantumRegister(7, 'q1')
cr = qiskit.ClassicalRegister(2, 'c')
q2 = qiskit.QuantumRegister(1, 'q2')
qc = qiskit.QuantumCircuit(qr, cr, q2)

qc.x(qr[0])
qc.x(qr[1])
qc.x(qr[2])

qc.cx(qr[0], qr[3])
qc.cx(qr[1], qr[3])
qc.cx(qr[2], qr[3])

qc.ccx(qr[0], qr[1], qr[5])
qc.ccx(qr[0], qr[2], qr[6])

qc.ccx(qr[1], qr[2], q2[0])

qc.cx(qr[5], qr[4])
qc.cx(qr[6], qr[4])
qc.cx(q2[0], qr[4])

qc.measure(qr[3], cr[0])
qc.measure(qr[4], cr[1])

backend = qiskit_aer.Aer.get_backend('qasm_simulator')

print("Circuit diagram:")
print(qc.draw())

job = backend.run(qc, shots=1024)
result = job.result()

counts = result.get_counts()
print("\nMeasurement results:")
print(counts)

