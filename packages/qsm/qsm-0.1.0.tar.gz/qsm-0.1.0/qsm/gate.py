import numpy as np
from scipy import sparse
from qsm.method import *


class Gate:
    def __init__(self, qbits, apply_matrice, circuit_size):
        self.qbits = qbits
        self.gate = apply_matrice
        self.circuit_size = circuit_size

    def __operator_matrix__(self, gate_matrix: np.array, qubit: int):
        i_matrix = identity()
        gate_queue = [i_matrix for _ in range(self.circuit_size)]
        gate_queue[qubit] = gate_matrix

        operator_matrix = sparse.csr_matrix(gate_queue[0])

        for gate in gate_queue[1:]:
            operator_matrix = sparse.kron(operator_matrix, sparse.csr_matrix(gate))

        return operator_matrix

    def apply(self, qbit):
        new_array = self.__operator_matrix__(self.gate, qbit).dot(self.qbits[0])
        self.qbits[0] = new_array
        return new_array


class ControlledGate:
    def __init__(self, qbits, apply_matrice, circuit_size):
        self.qbits = qbits
        self.circuit_size = circuit_size
        self.gate = apply_matrice

    def __controlled_phase_handler__(self, matrix_to_calculate: np.array, control_qubit: int, target_qubit: int):
        if matrix_to_calculate.shape != (2, 2):
            matrix_to_calculate = matrix_to_calculate[-2:, -2:]

        bra_ket_zero = np.array([[1 + 0j, 0 + 0j], [0 + 0j, 0 + 0j]], "F")

        bra_ket_one = np.array([[0 + 0j, 0 + 0j], [0 + 0j, 1 + 0j]], "F")

        bra_ket_zero_kron = [identity()] * self.circuit_size

        bra_ket_one_kron = [identity()] * self.circuit_size

        bra_ket_zero_kron[control_qubit] = bra_ket_zero
        bra_ket_one_kron[control_qubit] = bra_ket_one
        bra_ket_one_kron[target_qubit] = matrix_to_calculate

        to_add_zero = sparse.csr_matrix(bra_ket_zero_kron[0])

        to_add_one = sparse.csr_matrix(bra_ket_one_kron[0])

        for i in range(1, len(bra_ket_zero_kron)):
            to_add_zero = sparse.kron(to_add_zero, sparse.csr_matrix(bra_ket_zero_kron[i]))

            to_add_one = sparse.kron(to_add_one, sparse.csr_matrix(bra_ket_one_kron[i]))

        to_add_zero += to_add_one
        matrix = to_add_zero.dot(self.qbits[0])
        return matrix

    def apply(self, qbit_target, qbit_control):
        new_array = sparse.csr_matrix(self.__controlled_phase_handler__(self.gate, qbit_control, qbit_target))
        return new_array


CX = lambda qbits, circuit_size: ControlledGate(qbits, paulix(), circuit_size)
I = lambda qbits, circuit_size: Gate(qbits, identity(), circuit_size)
X = lambda qbits, circuit_size: Gate(qbits, paulix(), circuit_size)
Y = lambda qbits, circuit_size: Gate(qbits, pauliy(), circuit_size)
Z = lambda qbits, circuit_size: Gate(qbits, pauliz(), circuit_size)
H = lambda qbits, circuit_size: Gate(qbits, hadamard(), circuit_size)
P = lambda qbits, theta, circuit_size: Gate(qbits, phase(theta), circuit_size)
S = lambda qbits, circuit_size: Gate(qbits, s(), circuit_size)
Sdg = lambda qbits, circuit_size: Gate(qbits, sdg(), circuit_size)
T = lambda qbits, circuit_size: Gate(qbits, t(), circuit_size)
Tdg = lambda qbits, circuit_size: Gate(qbits, tdg(), circuit_size)
RZ = lambda qbits, theta, circuit_size: Gate(qbits, rz(theta), circuit_size)
RX = lambda qbits, theta, circuit_size: Gate(qbits, rx(theta), circuit_size)
RY = lambda qbits, theta, circuit_size: Gate(qbits, ry(theta), circuit_size)
SX = lambda qbits, circuit_size: Gate(qbits, sx(), circuit_size)
SXdg = lambda qbits, circuit_size: Gate(qbits, sxdg(), circuit_size)
U = lambda qbits, theta, phi, lamba, circuit_size: Gate(qbits, u(theta, phi, lamba), circuit_size)
