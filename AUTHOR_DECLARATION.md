# Formal Declaration of Intellectual Priority and Scientific Authorship

**Work Title:** *On the Non-Existence of $(5,5,43)$-Ramsey Graphs under Order-7 Automorphisms with a Unique Fixed Point: A Certified Cube-and-Conquer Refutation*  
**Author:** Rodrigo Díaz Tapia  
**Affiliation:** Independent Researcher, Santiago, Chile  
**Contact:** `diaztapiarodrigo@gmail.com`  
**Date of Declaration & Sealing:** October 19, 2026 (14:30:00 UTC-3)  
**Permanent Repository:** [https://github.com/diaztapiarodrigo/ramsey-r55-z7-refutation](https://github.com/diaztapiarodrigo/ramsey-r55-z7-refutation)  
**Official Release Tag:** `v1.0.0`

---

## 1. Statement of Discovery & Scientific Claims

I, **Rodrigo Díaz Tapia**, declare sole scientific authorship of the research, combinatorial formulations, analytical reductions, and computational refutations presented in this work, establishing:

1. **Analytical Degree Rigidity Theorem:** Deduction from $R(4,5)=25$ that any hypothetical $(5,5,43)$-Ramsey graph invariant under an order-7 automorphism with a unique fixed point ($f=1, B=6$) unconditionally forces the fixed vertex to connect to exactly 3 orbits in red and 3 orbits in blue ($\text{deg}_{\text{red}}(0) = 21, \text{deg}_{\text{blue}}(0) = 21$), leaving zero degrees of freedom at the fixed point.
2. **Algebraic Symmetry Reduction Scheme:** Formal formulation of:
   - Intra-block multiplier normalization on block $B_0$ via $\mathbb{Z}_7^* / \{\pm 1\} \cong \mathbb{Z}_3$, soundly eliminating 4 non-minimal distance bitvectors via 4 clauses of length 3.
   - Independent phase alignment on free blocks $B_1, \dots, B_5$ via 570 lexicographic comparison clauses across the 5 anchor pairs $(B_0, B_b)$, reducing the model search space by the exact theoretical group orbit factor $7^5 \times 3 = 50,421$.
3. **Complete Partition and Proof Certification:**
   - Partitioning of the propositional search space into **237 mutually orthogonal cubes** whose exact rational weights sum strictly to $\sum_{i=1}^{237} 2^{-|c_i|} = \frac{1}{1} = 1.0$.
   - Complete formal unsatisfiability verification of all 237 leaves using CaDiCaL 1.9.5 and the independent proof checker `drat-trim` (exit code 0, `s VERIFIED`), totaling 5.97 GiB of proof traces across 20.72 hours of concurrent verification.

---

## 2. Cryptographic Hashes of Key Artifacts

The core artifacts of this work are permanently sealed under the following SHA-256 digests:

| File | SHA-256 Checksum |
| :--- | :--- |
| `arxiv_ramsey_r55_n43.pdf` | `859767e7c65621316e9a7f5c6d1cfffb1134e1ec7f1f69025d15b025cea20ec4` |
| `docs/arxiv_ramsey_r55_n43.tex` | `d720ad961b7fcf4a549ff73ebcbaef074900a6cb7b0cfeb63158c54c3757faad` |
| `ramsey_cubes_237.icnf` | `ef32b70f06536551b329a4a7ce6b82531065e89d1469e3a6a9be777f9859f9ce` |
| `manifest_ramsey_complete_237_leaves.json` | `56ba1d74b3c2f016b9bb21e89bed06384550e840d9279c133b48abe24e5fd39c` |
| `manifest_ramsey_c214.json` | `295a643d99d3fc5d9caad0d41893c834a36214f4e24eb45f3caee36f00db15c5` |
| `manifest_ramsey_c202.json` | `f28a8d50937a09c2a865664177bc954f91e92d6e32bc13d5267a544136653df3` |
| `ramsey.cnf` (Base CNF, UNIX LF) | `0a9fc55ec9a2bcbab3a27fdc77619732113a5163ac555b7e506b3b5ad5c31485` |
| `ramsey.cnf` (Base CNF, Windows CRLF) | `b055bde4271755e718fd7db964e3f4a11f59ce943af3506c7ac92e17ac3ccb8e` |

A full list of all 29 repository file hashes is recorded in `SHA256SUMS.txt`.

---

## 3. Methodological & AI Disclosure

In accordance with arXiv and academic publishing standards:
- The Antigravity agentic coding environment (Google DeepMind) was utilized to assist in software engineering, automating solver dispatch, parallel test-suite generation, and data orchestration.
- All mathematical formulations, symmetry reductions, combinatorial proofs, analytical deductions, and scientific conclusions remain the sole responsibility of the author.

---

**Signed:**  
**Rodrigo Díaz Tapia**  
*Santiago, Chile — October 19, 2026*  
`diaztapiarodrigo@gmail.com`
