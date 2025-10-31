from argparse import ArgumentParser
from timeit import default_timer as timer

from bqskit.ir import Circuit
from bqskit.compiler.compile import compile
from bqskit.ft.cliffordt.cliffordtmodel import CliffordTModel
from bqskit.ft.cliffordt.cliffordtgates import clifford_t_gates


def get_name(qasm_file: str) -> str:
    """Extract a name from the QASM file path."""
    import os
    base = os.path.basename(qasm_file)
    name, _ = os.path.splitext(base)
    return name


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('qasm_file', type=str, help='Path to the input QASM file.')
    parser.add_argument('precision', type=int, help='Precision for synthesis.')
    args = parser.parse_args()

    name = get_name(args.qasm_file)
    # Load input circuit
    circuit = Circuit.from_file(args.qasm_file)

    # Let's choose a precision for synthesis
    precision = args.precision
    _precision = 10 ** (-precision)

    print(f'Starting synthesis for {name} with precision 10^-{precision}...')

    # Regular syntheis
    start_time = timer()
    reg_circuit = compile(circuit, synthesis_epsilon=_precision)
    end_time = timer()
    reg_time = end_time - start_time
    # Let's save the regular qasm
    print(f'Regular synthesis time: {reg_time} seconds')
    reg_circuit.save(f'outputs/reg_{name}_{precision}.qasm')

    # Fault-tolerant synthesis
    machine = CliffordTModel(circuit.num_qudits)
    start_time = timer()
    ft_circuit = compile(circuit, model=machine)
    end_time = timer()
    ft_time = end_time - start_time
    # Let's save the fault-tolerant qasm
    print(f'Fault-tolerant synthesis time: {ft_time} seconds')
    ft_circuit.save(f'outputs/ft_{name}_{precision}.qasm')