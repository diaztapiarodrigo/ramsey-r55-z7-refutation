#!/usr/bin/env python3
"""
verify_encoder_reproduction.py - Clean-Room Encoder Regeneration & Hash Verification

This script verifies that the boolean formula ramsey.cnf can be deterministically
regenerated from mathematical first principles via RamseyZ7Instance:
1. Generates 309 variables (129 base edge orbits, 180 comparator auxiliaries).
2. Generates exactly 275,608 clauses (275,028 clique clauses, 6 degree unit clauses,
   4 multiplier clauses, 570 lexicographic symmetry breaking clauses).
3. Computes LF and CRLF SHA-256 checksums and validates a byte-for-byte match
   against canonical hashes.

Usage:
    python scripts/verify_encoder_reproduction.py
"""

import sys
import hashlib
from core.frontier_encoders import RamseyZ7Instance

CANONICAL_HASHES = {
    "lf": "0a9fc55ec9a2bcbab3a27fdc77619732113a5163ac555b7e506b3b5ad5c31485",
    "crlf": "b055bde4271755e718fd7db964e3f4a11f59ce943af3506c7ac92e17ac3ccb8e",
}

def main():
    print("=" * 72)
    print("  VEKTOR-INTELLIGENCE: CLEAN-ROOM ENCODER REGENERATION (n=43, f=1, B=6)")
    print("=" * 72)
    print("Generating formula from first principles via RamseyZ7Instance...")
    
    inst = RamseyZ7Instance(
        n_blocks=6,
        k_red=5,
        k_blue=5,
        red_blocks_of_0=[0, 1, 2],
        symmetry_breaking=True,
        keep_clauses=True
    )
    
    num_vars = inst.b.num_vars
    num_clauses = inst.b.num_clauses
    base_vars = inst.base_vars
    
    print(f"  -> Variables: {num_vars} (base edge variables: {base_vars}, auxiliaries: {num_vars - base_vars})")
    print(f"  -> Clauses:   {num_clauses:,}")
    
    assert num_vars == 309, f"Expected 309 variables, got {num_vars}"
    assert num_clauses == 275608, f"Expected 275,608 clauses, got {num_clauses}"
    assert base_vars == 129, f"Expected 129 base variables, got {base_vars}"
    
    print("\nComputing SHA-256 checksums from regenerated clause stream...")
    
    # Check LF
    h_lf = hashlib.sha256()
    h_lf.update(f"p cnf {num_vars} {num_clauses}\n".encode("ascii"))
    for cl in inst.b.clauses:
        h_lf.update((" ".join(map(str, cl)) + " 0\n").encode("ascii"))
    lf_hash = h_lf.hexdigest()
    
    # Check CRLF
    h_crlf = hashlib.sha256()
    h_crlf.update(f"p cnf {num_vars} {num_clauses}\r\n".encode("ascii"))
    for cl in inst.b.clauses:
        h_crlf.update((" ".join(map(str, cl)) + " 0\r\n").encode("ascii"))
    crlf_hash = h_crlf.hexdigest()
    
    print(f"  -> Regenerated LF SHA-256:   {lf_hash}")
    print(f"     Expected LF SHA-256:      {CANONICAL_HASHES['lf']}")
    assert lf_hash == CANONICAL_HASHES["lf"], "LF hash mismatch!"
    print("     [MATCH - 100% BYTE-FOR-BYTE IDENTICAL]")
    
    print(f"\n  -> Regenerated CRLF SHA-256: {crlf_hash}")
    print(f"     Expected CRLF SHA-256:    {CANONICAL_HASHES['crlf']}")
    assert crlf_hash == CANONICAL_HASHES["crlf"], "CRLF hash mismatch!"
    print("     [MATCH - 100% BYTE-FOR-BYTE IDENTICAL]")
    
    print("\n" + "=" * 72)
    print("  [PASS] CLEAN-ROOM ENCODER REGENERATION CONFIRMED (EXIT 0)")
    print("=" * 72)
    return 0

if __name__ == "__main__":
    sys.exit(main())
