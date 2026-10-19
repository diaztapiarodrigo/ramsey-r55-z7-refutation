"""
Validacion cruzada avanzada del codificador RamseyZ7 en n=43 (VK-STD-003):
1. Estadisticas completas de 140 muestras aleatorias (seed=42):
   - Red-free, Blue-free, Saturated.
2. Analisis granular de casos frontera (con 1, 2, 3... K5/I5 monocromaticos):
   - Muestras en p=0.30 a p=0.70 con conteo exacto de cliques.
3. Verificacion de equivalencia logica bit a bit:
   (G contiene K5 rojo en grafo) <===> (CNF viola clausula roja)
   (G contiene K5 azul en grafo) <===> (CNF viola clausula azul)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
import random
import itertools
import numpy as np
from core.frontier_encoders import RamseyZ7Instance, _z7_shift

def main():
    print("=== TEST DE FRONTERA Y BAJA DENSIDAD DE K5/I5 EN n=43 ===", flush=True)
    random.seed(42)
    np.random.seed(42)
    
    t0 = time.time()
    inst = RamseyZ7Instance(6, 5, 5, red_blocks_of_0=None, symmetry_breaking=False, keep_clauses=True)
    clauses = inst.clauses
    assert len(clauses) == 275028
    
    red_clauses_vars = [[abs(x) for x in cl] for cl in clauses if cl[0] < 0]
    blue_clauses_vars = [[abs(x) for x in cl] for cl in clauses if cl[0] > 0]
    print(f"Cargadas {len(clauses)} clausulas ({len(red_clauses_vars)} rojas, {len(blue_clauses_vars)} azules) en {time.time()-t0:.2f}s", flush=True)

    # Precomputamos las 137,514 orbitas canonicas de 5-subconjuntos
    t_orb = time.time()
    canonical_5sets = []
    for tup in itertools.combinations(range(43), 5):
        is_canon = True
        for s in range(1, 7):
            shifted = tuple(sorted(_z7_shift(v, s) for v in tup))
            if shifted < tup:
                is_canon = False
                break
        if is_canon:
            canonical_5sets.append(tup)
    assert len(canonical_5sets) == 137514
    edges_of_subsets = [list(itertools.combinations(tup, 2)) for tup in canonical_5sets]
    print(f"Orbitas precomputadas en {time.time()-t_orb:.2f}s", flush=True)

    def evaluate_coloring(assignment):
        cnf_red_violations = sum(1 for c_vars in red_clauses_vars if all(assignment[v] == 1 for v in c_vars))
        cnf_blue_violations = sum(1 for c_vars in blue_clauses_vars if all(assignment[v] == 0 for v in c_vars))
        
        adj = np.zeros((43, 43), dtype=np.int8)
        for u in range(43):
            for v in range(u + 1, 43):
                var = inst.edge_var[u][v]
                if assignment[var] == 1:
                    adj[u, v] = adj[v, u] = 1

        graph_red_violations = sum(1 for edges in edges_of_subsets if all(adj[a, b] == 1 for a, b in edges))
        graph_blue_violations = sum(1 for edges in edges_of_subsets if all(adj[a, b] == 0 for a, b in edges))

        assert cnf_red_violations == graph_red_violations, f"Mismatch red: CNF={cnf_red_violations} vs Graph={graph_red_violations}"
        assert cnf_blue_violations == graph_blue_violations, f"Mismatch blue: CNF={cnf_blue_violations} vs Graph={graph_blue_violations}"
        
        return cnf_red_violations, cnf_blue_violations

    # FASE 1: 140 Muestras Aleatorias
    print("\n--- FASE 1: 140 Muestras Aleatorias (Estadisticas de Monocromaticidad) ---", flush=True)
    densities = [0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9]
    stats = {p: {"red_free": 0, "blue_free": 0, "both_free": 0, "total": 0} for p in densities}
    
    for p in densities:
        for _ in range(20):
            assignment = [0] + [1 if random.random() < p else 0 for _ in range(129)]
            r_viol, b_viol = evaluate_coloring(assignment)
            stats[p]["total"] += 1
            if r_viol == 0:
                stats[p]["red_free"] += 1
            if b_viol == 0:
                stats[p]["blue_free"] += 1
            if r_viol == 0 and b_viol == 0:
                stats[p]["both_free"] += 1
        
        print(f"p={p:.2f}: {stats[p]['total']} muestras | Red-free: {stats[p]['red_free']} | Blue-free: {stats[p]['blue_free']} | Ambos-free: {stats[p]['both_free']}", flush=True)

    # FASE 2: Casos de frontera fina con bajo conteo de cliques (1 a 10 cliques)
    print("\n--- FASE 2: Muestras de Frontera Fina con Conteo Bajo de Cliques ---", flush=True)
    boundary_found = 0
    # Exploramos densidades finas de transicion: 0.28 a 0.38 para K5 rojo, y 0.62 a 0.72 para I5 azul
    fine_densities = [0.28, 0.30, 0.32, 0.34, 0.36, 0.64, 0.66, 0.68, 0.70, 0.72]
    
    for p in fine_densities:
        for trial in range(5):
            assignment = [0] + [1 if random.random() < p else 0 for _ in range(129)]
            r_viol, b_viol = evaluate_coloring(assignment)
            # Casos frontera: donde alguno de los colores tiene entre 1 y 15 violaciones
            if (1 <= r_viol <= 15) or (1 <= b_viol <= 15):
                boundary_found += 1
                print(f"[Frontera p={p:.2f}] Red K5 violados: {r_viol} | Blue I5 violados: {b_viol} -> CNF y Grafo coinciden al 100.00%", flush=True)

    print(f"\nTotal casos de frontera con pocos cliques evaluados: {boundary_found}", flush=True)
    print("=== TODAS LAS PRUEBAS DE FRONTERA COMPLETADAS EXITOSAMENTE CON 0 DISCREPANCIAS ===", flush=True)

if __name__ == "__main__":
    main()
