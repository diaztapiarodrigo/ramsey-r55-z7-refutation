#!/usr/bin/env python3
"""
reverify_heavy_leaf.py - Standalone re-verification of the massive leaf c214_m0 (246.8 MB DRAT trace)
using the official drat-trim binary inside an isolated container.
"""
import subprocess
import time
import sys

def main():
    print("=" * 72)
    print("  VEKTOR-INTELLIGENCE: RE-VERIFYING HEAVY LEAF c214_m0 (246.8 MB)")
    print("=" * 72)
    
    subprocess.run(['docker', 'rm', '-f', 'heavy_verifier'], capture_output=True)
    subprocess.run(['docker', 'run', '-d', '--name', 'heavy_verifier', 'vektor-sat-verifier:latest', 'sleep', '2000'], check=True)
    subprocess.run(['docker', 'cp', 'scratch/bin/drat-trim', 'heavy_verifier:/usr/local/bin/drat-trim'], check=True)
    subprocess.run(['docker', 'exec', '-i', 'heavy_verifier', 'chmod', '+x', '/usr/local/bin/drat-trim'], check=True)

    print("Copying c214_m0.cnf (10.3 MB) and c214_m0.drat (246.8 MB) into container...")
    subprocess.run(['docker', 'cp', 'scratch/c214_leaves/c214_m0.cnf', 'heavy_verifier:/tmp/c214_m0.cnf'], check=True)
    subprocess.run(['docker', 'cp', 'scratch/c214_leaves/c214_m0.drat', 'heavy_verifier:/tmp/c214_m0.drat'], check=True)

    print("Launching drat-trim on c214_m0 (timeout 1800s)...")
    t0 = time.perf_counter()
    p = subprocess.run(['docker', 'exec', '-i', 'heavy_verifier',
                        '/usr/local/bin/drat-trim', '/tmp/c214_m0.cnf', '/tmp/c214_m0.drat', '-t', '1800'],
                       capture_output=True, text=True)
    dt = time.perf_counter() - t0
    
    out = p.stdout.replace('\r', '\n')
    is_verified = ("s VERIFIED" in out) and ("NOT VERIFIED" not in out) and (p.returncode == 0)
    
    print(f"\nResult: {'VERIFIED (s VERIFIED)' if is_verified else 'FAILED'} [exit {p.returncode}] in {dt:.2f}s ({dt/60:.2f} min)")
    for line in out.splitlines():
        line_s = line.strip()
        if line_s.startswith("s ") or line_s.startswith("c verification") or "conflict" in line_s or "core" in line_s:
            print(f"  {line_s}")

    subprocess.run(['docker', 'rm', '-f', 'heavy_verifier'], capture_output=True)
    return 0 if is_verified else 1

if __name__ == '__main__':
    sys.exit(main())
