def get_physical_errors(backend, coupling_map):
    """
    Extracts the CX gate error rates for all physical edges from the Qiskit backend.
    """
    physical_errors = {}
    for edge in coupling_map.get_edges():
        props = backend.target["cx"].get(edge)
        # Default to 0.01 if no data is available
        physical_errors[edge] = props.error if props else 0.01 
    return physical_errors

def noise_aware_layout(physical_errors, num_qubits):
    """
    Core algorithm: Calculates risk scores for physical qubits based on error rates 
    and maps logical qubits to the safest physical qubits.
    """
    # 1. Score the physical seats
    seat_scores = {q: 0 for q in range(num_qubits)}
    for edge, error_rate in physical_errors.items():
        q1, q2 = edge
        # Accumulate the error rate to both ends of the edge
        seat_scores[q1] += error_rate
        seat_scores[q2] += error_rate
        
    # 2. Sort seats by risk score (lowest risk first)
    sorted_seats = sorted(seat_scores, key=seat_scores.get)
    
    # 3. Create the logical-to-physical mapping
    layout_mapping = {}
    for logical_q in range(num_qubits):
        layout_mapping[logical_q] = sorted_seats[logical_q]
        
    return layout_mapping

def count_bad_edges(qc, physical_errors, threshold=0.05):
    """
    Counts how many times the compiled circuit executes a CX gate on a high-error-rate edge.
    """
    bad_count = 0
    for instruction in qc.data:
        if instruction.name == 'cx':
            q1 = qc.find_bit(instruction.qubits[0]).index
            q2 = qc.find_bit(instruction.qubits[1]).index
            # Handle both directions (q1,q2) and (q2,q1)
            error = physical_errors.get((q1, q2), physical_errors.get((q2, q1), 0))
            if error > threshold:
                bad_count += 1
    return bad_count