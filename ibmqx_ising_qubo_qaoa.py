from collections import OrderedDict
import numpy as np
from qiskit.quantum_info import Pauli

###### This is the function I couldn't find updated version ########## 
# from qiskit_aqua import Operator
### also change qiskit_aqua to qiskit.aqua #####
############################################
from qiskit.optimization.applications.ising import max_cut

from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import *
from qiskit.aqua import QuantumInstance
import networkx as nx
# from qiskit.aqua import get_aer_backend
from qiskit import Aer, execute


def sample_most_likely(state_vector):
    if isinstance(state_vector, dict) or isinstance(state_vector, OrderedDict):
        binary_string = sorted(state_vector.items(), key=lambda kv: kv[1])[-1][0]
        x = np.asarray([int(y) for y in reversed(list(binary_string))])
        return x
    else:
        n = int(np.log2(state_vector.shape[0]))
        k = np.argmax(np.abs(state_vector))
        x = np.zeros(n)
        for i in range(n):
            x[i] = k % 2
            k >>= 1
        return x
# def get_qubitops(input):
#     w = np.array(input.tolist())
#     num_nodes = len(w)
#     pauli_list = []
#     shift = 0
#     for i in range(num_nodes):
#         for j in range(i+1, num_nodes):
#             if w[i, j] != 0:
#                 xp = np.zeros(num_nodes, dtype=np.bool)
#                 zp = np.zeros(num_nodes, dtype=np.bool)
#                 zp[i] = True
#                 zp[j] = True
#                 pauli_list.append([w[i, j], Pauli(zp, xp)])
#                 shift += 1
#     for i in range(num_nodes):
#         degree = np.sum(w[i, :])
#         xp = np.zeros(num_nodes, dtype=np.bool)
#         zp = np.zeros(num_nodes, dtype=np.bool)
#         zp[i] = True
#         pauli_list.append([w[i, i], Pauli(zp, xp)])
#     return Operator(paulis=pauli_list)

#'ibmqx4'
#'ibmq_16_melbourne'
# from qiskit import IBMQ
# IBMQ.load_accounts()

def solve_ibmqx_ising_qubo(G, matrix_func, optimizer, p):
        backend = Aer.get_backend('qasm_simulator')
        w = matrix_func(G)
        # ops = get_qubitops(w)
        ops, offset = max_cut.get_operator(w)
        qaoa = QAOA(ops, optimizer, p, aux_operators='paulis')
        quantum_instance = QuantumInstance(backend)
        result = qaoa.run(quantum_instance)
        x = sample_most_likely(result['eigvecs'][0])
        return x
# def solve_ibmqx_ising_qubo_nisq_melbourne(G, matrix_func, optimizer, p):
#         backend = IBMQ.get_backend('ibmq_16_melbourne')
#         w = matrix_func(G)
#         ops = get_qubitops(w)
#         qaoa = QAOA(ops, optimizer, p, operator_mode='paulis')
#         quantum_instance = QuantumInstance(backend)
#         result = qaoa.run(quantum_instance)
#         x = sample_most_likely(result['eigvecs'][0])
#         return x
# def solve_ibmqx_ising_qubo_nisq_ibmqx4(G, matrix_func, optimizer, p):
#         backend = IBMQ.get_backend('ibmqx4')
#         w = matrix_func(G)
#         ops = get_qubitops(w)
#         qaoa = QAOA(ops, optimizer, p, operator_mode='paulis')
#         quantum_instance = QuantumInstance(backend)
#         result = qaoa.run(quantum_instance)
#         x = sample_most_likely(result['eigvecs'][0])
#         return x

