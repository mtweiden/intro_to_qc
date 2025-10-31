import numpy as np

from bqskit.ir import Circuit
from bqskit.compiler.compile import compile
from bqskit.ft.cliffordt.cliffordtmodel import CliffordTModel
from bqskit.ft.cliffordt.cliffordtgates import clifford_t_gates


# Example unitary to synthesize
def qft(num_qubits: int) -> np.ndarray:
    n = 2 ** num_qubits
    root = np.e ** (2j * np.pi / n)
    x = np.fromfunction(lambda x, y: root**(x * y), (n, n))
    return np.array(x) / np.sqrt(n)

u = qft(num_qubits=2)
circuit = Circuit.from_unitary(u)

# Let's choose a precision for synthesis
precision = 8
_precision = 10 ** (-precision)

# Regular syntheis
reg_circuit = compile(circuit, synthesis_epsilon=_precision)
# Let's save the regular qasm
reg_circuit.save(f'outputs/reg_qft_{precision}.qasm')

# Fault-tolerant synthesis
machine = CliffordTModel(circuit.num_qudits)
ft_circuit = compile(circuit, model=machine)
# Let's save the fault-tolerant qasm
ft_circuit.save(f'outputs/ft_qft_{precision}.qasm')

print('The Clifford+T gate set:')
print(clifford_t_gates)
print('The regular circuit contains these gates:')
print(reg_circuit.gate_set)
print('The fault-tolerant circuit contains these gates:')
print(ft_circuit.gate_set)

# Let's look at how far each circuit is from the target unitary
reg_unitary = reg_circuit.get_unitary()
ft_unitary = ft_circuit.get_unitary()

reg_d = reg_unitary.get_distance_from(u)
ft_d = ft_unitary.get_distance_from(u)

print(f'Regular circuit distance from target unitary: {reg_d}')
print(f'Fault-tolerant circuit distance from target unitary: {ft_d}')
