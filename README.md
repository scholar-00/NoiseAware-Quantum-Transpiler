# NoiseAware-Quantum-Transpiler

## Background
Qiskit's default layout algorithms (e.g., `DenseLayout`) primarily focus on the topological connectivity of the physical hardware. However, they neglect the physical noise (e.g., CX gate error rates) of real quantum chips. Allocating highly interactive logical qubits to high-error-rate physical edges significantly degrades the fidelity of the final quantum state.

## Core Algorithm
This project implements a custom Qiskit compiler plugin (`NoiseAwareLayout`) that introduces a hardware noise cost model during the layout stage:
1. Extracts real error rate data from the backend via `backend.target["cx"].error`.
2. Uses a greedy strategy to accumulate the error rates of adjacent edges for each physical qubit, calculating a "seat risk score".
3. Maps logical qubits to the "safest" physical qubits (lowest risk scores), maximizing the avoidance of high-error-rate connections.

## Experimental Results
In a simulated environment with a 10% error rate on a specific edge, this algorithm reduced the number of executions on the "bad edge" from **4 times** (Qiskit default) to **0 times**.
