from qsm.qubit import *

import scipy.sparse as ss

__all__ = [
    "gen_qubit",

]

class QuantumCircuit:
    def __init__(self, qbits, state: str="z"):

        self.circuit_size = qbits

        self.state = ss.csr_matrix(gen_qubit(state))

        for i in range(qbits-1):
            self.state = ss.kron(self.state, ss.csr_matrix(gen_qubit(state)))

    def apply_gate(self, gate, target_qubit: int):
        gate_class = gate([self.state], self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def apply_controlled_gate(self, gate, target_qubit, control_qubit):
        gate_class = gate([self.state], self.circuit_size)
        self.state = gate_class.apply(target_qubit, control_qubit)

    def custom_controlled_gate(self, gate_matrix, target_qubit, control_qubit):
        gate_class = ControlledGate([self.state], gate_matrix, self.circuit_size)
        self.state = gate_class.apply(target_qubit, control_qubit)

    def u(self, target_qubit, theta, phi, lamba):
        gate_class = U([self.state], theta, phi, lamba, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def p(self, target_qubit, theta):
        gate_class = P([self.state], theta, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def rz(self, target_qubit, theta):
        gate_class = RZ([self.state], theta, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def rx(self, target_qubit, theta):
        gate_class = RX([self.state], theta, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def ry(self, target_qubit, theta):
        gate_class = RY([self.state], theta, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def r(self, target_qubit, theta):
        gate_class = R([self.state], theta, self.circuit_size)
        self.state = gate_class.apply(target_qubit)

    def get_state(self):
        return self.state.toarray()

    def prob(self, show_percent: bool = False):
        return probabilities(self.state.toarray(), self.circuit_size, show_percent)

    def measure(self):
        prob = self.prob()
        return measure(self.state.toarray(), self.circuit_size, prob)

    def phase_angle(self):
        return phaseangle(self.state.toarray(), self.circuit_size)

    def amplitude(self):
        return amplitude(self.state.toarray(), self.circuit_size)
