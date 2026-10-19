#!/usr/bin/env python3
"""
reverify_direct_leaves.py - Re-solve and re-verify a sample of direct partition leaves
from first principles using CaDiCaL + drat-trim inside the isolated container.
"""
import subprocess
import time
import sys
from pathlib import Path

def main():
    print("=" * 72)
    print("  VEKTOR-INTELLIGENCE: RE-SOLVING & RE-VERIFYING DIRECT LEAVES (0..4)")
    print("=" * 72)

    # 1. Parse cubes from ramsey_all_leaves.icnf
    cubes = []
    with open("ramsey_all_leaves.icnf", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("a "):
                lits = [int(x) for x in line.split()[1:] if int(x) != 0]
                cubes.append(lits)
    
    print(f"Loaded {len(cubes)} root cubes. Testing leaves 0..4...")

    subprocess.run(['docker', 'rm', '-f', 'direct_verifier'], capture_output=True)
    subprocess.run(['docker', 'run', '-d', '--name', 'direct_verifier', 'vektor-sat-verifier:latest', 'sleep', '600'], check=True)
    subprocess.run(['docker', 'cp', 'scratch/bin/cadical', 'direct_verifier:/usr/local/bin/cadical'], check=True)
    subprocess.run(['docker', 'cp', 'scratch/bin/drat-trim', 'direct_verifier:/usr/local/bin/drat-trim'], check=True)
    subprocess.run(['docker', 'exec', '-i', 'direct_verifier', 'chmod', '+x', '/usr/local/bin/cadical', '/usr/local/bin/drat-trim'], check=True)

    # Read base ramsey.cnf
    with open("ramsey.cnf", "r") as f:
        base_lines = f.readlines()
    
    header = base_lines[0].strip().split()
    nvars = int(header[2])
    nclauses = int(header[3])

    results = []
    for idx in range(5):
        c = cubes[idx]
        print(f"\n--- Testing direct_leaf_{idx} (cube: {c}) ---")
        
        # Build leaf CNF
        leaf_clauses = nclauses + len(c)
        leaf_cnf_lines = [f"p cnf {nvars} {leaf_clauses}\n"] + base_lines[1:]
        for lit in c:
            leaf_cnf_lines.append(f"{lit} 0\n")
            
        leaf_cnf_path = f"scratch/test_direct_leaf_{idx}.cnf"
        with open(leaf_cnf_path, "w", newline="\n") as f:
            f.writelines(leaf_cnf_lines)

        # Copy to container
        subprocess.run(['docker', 'cp', leaf_cnf_path, f'direct_verifier:/tmp/leaf_{idx}.cnf'], check=True)

        # Run CaDiCaL
        t0 = time.perf_counter()
        p_cad = subprocess.run(['docker', 'exec', '-i', 'direct_verifier',
                                '/usr/local/bin/cadical', '-q', '--no-binary',
                                f'/tmp/leaf_{idx}.cnf', f'/tmp/leaf_{idx}.drat'],
                               capture_output=True, text=True)
        t_solver = time.perf_counter() - t0
        solver_status = {10: "SAT", 20: "UNSAT"}.get(p_cad.returncode, "UNKNOWN")
        print(f"  CaDiCaL: {solver_status} [code {p_cad.returncode}] in {t_solver:.2f}s")
        assert solver_status == "UNSAT", f"Expected UNSAT, got {solver_status}"

        # Run drat-trim
        t0 = time.perf_counter()
        p_trim = subprocess.run(['docker', 'exec', '-i', 'direct_verifier',
                                 '/usr/local/bin/drat-trim', f'/tmp/leaf_{idx}.cnf', f'/tmp/leaf_{idx}.drat'],
                                capture_output=True, text=True)
        t_checker = time.perf_counter() - t0
        out_trim = p_trim.stdout.replace('\r', '\n')
        is_verified = ("s VERIFIED" in out_trim) and ("NOT VERIFIED" not in out_trim) and (p_trim.returncode == 0)
        print(f"  drat-trim: {'VERIFIED (s VERIFIED)' if is_verified else 'FAILED'} [code {p_trim.returncode}] in {t_checker:.2f}s")
        
        results.append((f"direct_leaf_{idx}", is_verified, t_solver, t_checker))
        
        # Cleanup
        Path(leaf_cnf_path).unlink(missing_ok=True)
        subprocess.run(['docker', 'exec', '-i', 'direct_verifier', 'rm', '-f', f'/tmp/leaf_{idx}.cnf', f'/tmp/leaf_{idx}.drat'], capture_output=True)

    subprocess.run(['docker', 'rm', '-f', 'direct_verifier'], capture_output=True)

    print("\n" + "=" * 72)
    print("  DIRECT LEAVES SUMMARY:")
    all_ok = True
    for name, ok, ts, tc in results:
        mark = "[PASS]" if ok else "[FAIL]"
        print(f"    {mark} {name:15s} : Solver {ts:.2f}s, Checker {tc:.2f}s (Total {ts+tc:.2f}s)")
        if not ok:
            all_ok = False
    print("=" * 72)
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
