# Certified Refutation of (5,5,43)-Ramsey Graphs under Order-7 Automorphisms with a Unique Fixed Point

[![Preprint PDF](https://img.shields.io/badge/Preprint-PDF-blue.svg)](arxiv_ramsey_r55_n43.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Verification](https://img.shields.io/badge/DRAT--trim-Certified%20UNSAT-brightgreen.svg)](#reproducibility--verification)
[![Leaves](https://img.shields.io/badge/Cubes-237%20Disjoint-orange.svg)](#partition-structure)

This repository provides the complete, self-contained replication bundle for the preprint:
> **"On the Non-Existence of $(5,5,43)$-Ramsey Graphs under Order-7 Automorphisms with a Unique Fixed Point: A Certified Cube-and-Conquer Refutation"**  
> *Rodrigo Díaz Tapia (Independent Researcher, Santiago, Chile)*

---

## 📌 Executive Summary

The classical diagonal Ramsey number $R(5,5)$ is tightly bounded between $43 \le R(5,5) \le 46$. The central hurdle to proving $R(5,5)=43$ is determining whether any $(5,5,43)$-graph exists. 

In this work, we analyze hypothetical $(5,5,43)$-graphs admitting a cyclic automorphism group $\mathbb{Z}_7$ acting with **exactly one fixed point ($f=1$) and 6 orbits of length 7 ($B=6$)**:

1. **Analytical Degree Rigidity:** We prove unconditionally from $R(4,5)=25$ (McKay & Radziszowski 1995) that the fixed vertex must have degree exactly 21, connecting in red to 3 orbits and in blue to 3 orbits (0 degrees of freedom at vertex 0).
2. **Symmetry Breaking:** Intra-block chords on $B_0$ are normalized under $\mathbb{Z}_7^* / \{\pm 1\} \cong \mathbb{Z}_3$ (eliminating 4 of 8 patterns), and phase shifts on $B_1, \dots, B_5$ are aligned via 570 lexicographic comparison clauses across the 5 anchor pairs $(B_0, B_b)$.
3. **Certified Cube-and-Conquer Refutation:** The resulting base CNF formula (309 variables, 275,608 clauses) was partitioned into **237 mutually orthogonal cubes** whose exact rational weights sum strictly to $\sum 2^{-|c_i|} = 1.0$.
4. **DRAT Proof Certification:** Every single subproblem was solved by CaDiCaL 1.9.5 and independently certified by `drat-trim` with exit code 0 (`s VERIFIED`).

---

## 🔬 Repository Structure

```text
├── arxiv_ramsey_r55_n43.pdf            # Compiled preprint (13 pages, LaTeX)
├── ramsey_cubes_237.icnf               # The 237 certified disjoint partition cubes
├── manifest_ramsey_complete_237_leaves.json  # Cryptographic manifest of all 237 certified leaves
├── run_all_verifications.py           # One-command audit runner
├── docs/                               # LaTeX sources and markdown preprint
│   ├── arxiv_ramsey_r55_n43.tex
│   └── arxiv_ramsey_r55_n43.md
├── figures/                            # Vector & raster preprint figures
│   ├── fig_structure.pdf / .png        # Geometric action of Z7 with 1 fixed point
│   ├── fig_depth.pdf / .png            # Depth distribution of the 237 cubes
│   └── fig_cost.pdf / .png             # Verification cost log-log profile
├── scripts/                            # Self-contained audit and verification tools
│   ├── verify_reproduction.py          # Weight sum (1.0), pairwise disjointness, hashes
│   ├── verify_encoder_reproduction.py  # Clean-room CNF regeneration from first principles
│   ├── test_all_137514_orbits_exhaustive.py # 100% clause-orbit bijection test
│   ├── test_encoder_boundary_and_low_cliques.py # Random boundary sweeps on n=43
│   ├── reverify_drat_traces.py         # Standalone drat-trim runner with negative control
│   └── reverify_heavy_leaf.py          # Independent verification of 246.8 MiB leaf c214_m0
└── data/                               # Supplemental manifests and subcube allocations
```

---

## 🚀 Quickstart: Reproducing the Results

### 1. Installation
Clone the repository and install the standard dependencies:
```bash
git clone https://github.com/diaztapiarodrigo/ramsey-r55-z7-refutation.git
cd ramsey-r55-z7-refutation
pip install -r requirements.txt
```

### 2. Run the Complete Verification Suite
Execute all core mathematical verifications in one step:
```bash
python run_all_verifications.py
```
This runs:
* **Cube Coverage & Orthogonality:** Confirms that all $\binom{237}{2} = 27,966$ cube pairs are disjoint and that $\sum 2^{-|c|} = 1.0$.
* **Clean-Room CNF Regeneration:** Re-encodes the 275,608 clauses from scratch and checks both LF (`0a9fc55e...`) and CRLF (`b055bde4...`) SHA-256 hashes against `ramsey.cnf`.
* **100% Orbit Bijection:** Verifies the bijection between all $\binom{43}{5}/7 = 137,514$ canonical orbits and the generated clique clauses.
* **Satisfiability Boundary Sweep:** Validates exact clique count matches on 140 random $\mathbb{Z}_7$-invariant colorings.

### 3. Direct DRAT Proof Checking
To re-check proof traces with the official `drat-trim` binary inside Docker:
```bash
python scripts/reverify_drat_traces.py
```

---

## 📜 Citation

```bibtex
@article{diaz_tapia_2026_ramsey,
  title={On the Non-Existence of (5,5,43)-Ramsey Graphs under Order-7 Automorphisms with a Unique Fixed Point: A Certified Cube-and-Conquer Refutation},
  author={D{\'i}az Tapia, Rodrigo},
  year={2026},
  month={October},
  note={Preprint and auditable code repository: \url{https://github.com/diaztapiarodrigo/ramsey-r55-z7-refutation}}
}
```

---

## 📄 License
Released under the [MIT License](LICENSE).
