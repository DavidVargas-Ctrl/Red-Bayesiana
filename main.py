import itertools
import json
import os
import pandas as pd

json_filename = "estudiante.json"

def load_network(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_cpts(network):
    for node_name, node in network['nodes'].items():
        parents = node.get('parents', [])
        for entry in node['cpt']:
            s = sum(entry['then'].values())
            if abs(s - 1.0) > 1e-8:
                raise ValueError(f"CPT '{node_name}' suma {s}, debe ser 1.0")
            for p, v in entry['when'].items():
                if p not in parents:
                    raise ValueError(f"Parent inesperado '{p}' en '{node_name}'")
                if v not in network['nodes'][p]['values']:
                    raise ValueError(f"Valor inválido '{v}' para parent '{p}' en '{node_name}'")

def compute_joint_distribution(network):
    names = list(network['nodes'])
    combos = itertools.product(*(network['nodes'][n]['values'] for n in names))
    joint = []
    for combo in combos:
        assignment = dict(zip(names, combo))
        p = 1.0
        for n in names:
            for entry in network['nodes'][n]['cpt']:
                if all(assignment[parent] == val for parent, val in entry['when'].items()):
                    p *= entry['then'][assignment[n]]
                    break
        joint.append({**assignment, "prob": p})
    return pd.DataFrame(joint)

def print_query_steps(network, query_var, evidence):
    names = list(network['nodes'])
    combos = itertools.product(*(network['nodes'][n]['values'] for n in names))

    denom = 0.0
    numerators = {val: 0.0 for val in network['nodes'][query_var]['values']}

    print(f"\n=== Cálculo paso a paso de P({query_var} | {evidence}) ===")
    for combo in combos:
        assignment = dict(zip(names, combo))
        # solo procesamos las combinaciones que cumplen la evidencia
        if all(assignment[var] == val for var, val in evidence.items()):
            print(f"\nProcesando combinación relevante: {assignment}")
            p = 1.0
            for n in names:
                for entry in network['nodes'][n]['cpt']:
                    if all(assignment[parent] == v for parent, v in entry['when'].items()):
                        factor = entry['then'][assignment[n]]
                        if entry['when']:
                            print(f"  Nodo {n}: P({n}={assignment[n]} | {entry['when']}) = {factor}")
                        else:
                            print(f"  Nodo {n}: P({n}={assignment[n]}) = {factor}")
                        p *= factor
                        break
            print(f"  → Probabilidad conjunta = {p:.8f}")
            denom += p
            numerators[assignment[query_var]] += p

    print(f"\nDenominador P(evidencia) = {denom:.8f}")
    for val in network['nodes'][query_var]['values']:
        num = numerators[val]
        print(f"Numerador P({query_var}={val}, evidencia) = {num:.8f}")
        print(f"P({query_var}={val} | evidencia) = {num/denom:.4f}")

if __name__ == "__main__":
    if not os.path.exists(json_filename):
        print("Archivo no encontrado:", json_filename)
        exit(1)

    # 1) Carga y validación
    net = load_network(json_filename)
    validate_cpts(net)

    # 2) Computar la distribución conjunta (internamente, sin imprimir cada combo)
    df_joint = compute_joint_distribution(net)

    # 3) Definir consulta y evidencia
    query = "DesempeñoAcademico"
    evidence = {"ConsumoCafeina": "Sí", "CargaAcademica": "Baja"}

    # 4) Imprimir sólo los pasos relevantes para la consulta
    print_query_steps(net, query, evidence)
