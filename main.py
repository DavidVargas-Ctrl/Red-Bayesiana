import itertools
import json
import os
import pandas as pd

json_filename = "tren.json"
def load_network(json_path):
    #Carga la red bayesiana desde un archivo JSON
    with open(json_path, 'r', encoding='utf-8') as dicc:
        return json.load(dicc)



def validate_cpts(network):
    # Por cada nodo
    for node_name, node in network['nodes'].items():
        parents = node.get('parents', [])
        # Regla condicional en el cpt
        for entry in node['cpt']:
            total_prob = sum(entry['then'].values())
            # Probabilidades que sumen 1
            if abs(total_prob - 1.0) > 1e-8:
                raise ValueError(f"CPT de nodo '{node_name}' suma {total_prob}, debe ser 1.0")
            for p_name, p_val in entry['when'].items():
                # Parents definidos
                if p_name not in parents:
                    raise ValueError(f"Nodo '{node_name}': parent '{p_name}' no está en parents")
                # Valores validos de los padres definidos
                if p_val not in network['nodes'][p_name]['values']:
                    raise ValueError(f"Nodo '{node_name}': valor '{p_val}' no válido para el parent '{p_name}'")

def compute_joint_distribution(network):
    node_names = list(network['nodes'].keys())
    joint = []
    # Combinaciones segun producto cartesiano
    combinations = itertools.product(*(network['nodes'][n]['values'] for n in node_names))

    # Combinaciones
    for combo in combinations:
        assignment = dict(zip(node_names, combo))
        prob = 1.0

        # Multiplicaciones de probabilidades

        for n in node_names:
            node = network['nodes'][n]
            for entry in node['cpt']:
                if all(assignment[parent] == val for parent, val in entry['when'].items()):
                    prob *= entry['then'][assignment[n]]
                    break
            else:
                raise ValueError(f"No se encontró CPT válido para nodo '{n}' con 'when' = {entry['when']}")

        joint.append({
            "assignment": assignment,
            "probability": round(prob, 8)
        })

    return joint



#main
if os.path.exists(json_filename):
    red = load_network(json_filename)
    validate_cpts(red)
    red["joint"] = compute_joint_distribution(red)

    # Mostrar la tabla de forma legible
    df = pd.DataFrame(red["joint"])
    print(df.to_string(index=False))


else:
    print("No se encontró el archivo:", json_filename)
