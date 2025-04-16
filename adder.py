from qiskit import QuantumRegister as QuantumRegister
from qiskit import ClassicalRegister as ClassicalRegister
from qiskit import QuantumCircuit as QuantumCircuit
from qiskit_aer import AerSimulator

def quantum_full_adder(qc, a, b, cin, sum_, carry, temp1, temp2, temp3):
    qc.cx(a, sum_)
    qc.cx(b, sum_)
    qc.cx(cin, sum_)

    qc.ccx(a, b, temp1)
    qc.ccx(a, cin, temp2)
    qc.ccx(b, cin, temp3)

    qc.cx(temp1, carry)
    qc.cx(temp2, carry)
    qc.cx(temp3, carry)

def quantum_sub(qc, a, b, cin,  sum_, carry, temp1, temp2, temp3):
    qc.x(b)
    quantum_full_adder(qc, a, b, cin, sum_, carry, temp1, temp2, temp3)
    qc.x(b)

def quantum_and(qc, a, b, result):
    qc.ccx(a, b, result)

n = 8

a = QuantumRegister(n, 'a')
b = QuantumRegister(n, 'b')
sum_ = QuantumRegister(n, 'sum')
carry = QuantumRegister(n + 1, 'carry')
temp1 = QuantumRegister(n, 't1')
temp2 = QuantumRegister(n, 't2')
temp3 = QuantumRegister(n, 't3')
cr = ClassicalRegister(n + 1, 'c')
opcode = QuantumRegister(5, 'opcode')

qc = QuantumCircuit(a, b, sum_, carry, temp1, temp2, temp3, cr)

bin_a = input('Enter the first number (A) in binary: ')
bin_b = input('Enter the second number (B) in binary: ')

bin_a = bin_a.strip().replace(" ", "")
bin_b = bin_b.strip().replace(" ", "")

if not all(bit in '01' for bit in bin_a) or not all(bit in '01' for bit in bin_b):
    raise ValueError("Inputs must contain only binary digits (0 and 1)")

bin_a = bin_a.zfill(n)[-n:]
bin_b = bin_b.zfill(n)[-n:]

for i in range(n):
    if bin_a[n-1-i] == '1':
        qc.x(a[i])
    if bin_b[n-1-i] == '1':
        qc.x(b[i])


for i in range(n):
    quantum_full_adder(
        qc,
        a=a[i],
        b=b[i],
        cin=carry[i],
        sum_=sum_[i],
        carry=carry[i+1],
        temp1=temp1[i],
        temp2=temp2[i],
        temp3=temp3[i]
    )

for i in range(n):
    qc.measure(sum_[i], cr[i])
qc.measure(carry[n], cr[n])

backend = AerSimulator(method='matrix_product_state')

for i in range(3):
    ans = input("Do you want to see the circuit diagram? (y/n): ")
    if ans.lower() == 'y':
        print("Circuit diagram:")
        print(qc.draw())
        break
    elif ans.lower() == 'n':
        print("Circuit diagram not displayed.")
        break
    else:
        print("Invalid input, please enter 'y' or 'n'.")

job = backend.run(qc, shots=1024)
result = job.result()

counts = result.get_counts()
print("\nMeasurement results:")
print(counts)

