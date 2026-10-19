#!/usr/bin/env python3
"""
run_all_verifications.py - One-command master verification runner for reviewers.
"""
import subprocess
import sys

def main():
    print("=" * 72)
    print("  RAMSEY R(5,5,43) Z7 (f=1) - AUDIT & REPRODUCTION SUITE")
    print("=" * 72)

    tests = [
        ("Step 1: Manifest, Cubes & Weight Sum Verification", "scripts/verify_reproduction.py"),
        ("Step 2: Clean-Room CNF Regeneration (LF and CRLF Hashes)", "scripts/verify_encoder_reproduction.py"),
        ("Step 3: Exhaustive 100% Orbit-by-Orbit Bijection (137,514 Orbits)", "scripts/test_all_137514_orbits_exhaustive.py"),
        ("Step 4: Boundary & Transition Sensitivity on n=43 (140 Colorings)", "scripts/test_encoder_boundary_and_low_cliques.py"),
    ]

    all_passed = True
    for title, script in tests:
        print(f"\n>>> Running {title}...")
        res = subprocess.run([sys.executable, script])
        if res.returncode != 0:
            print(f"[-] FAILED: {script} exited with code {res.returncode}")
            all_passed = False
        else:
            print(f"[✓] PASSED: {title}")

    print("\n" + "=" * 72)
    if all_passed:
        print("  ALL CORE REPRODUCTION AUDITS PASSED WITH EXIT CODE 0.")
    else:
        print("  ONE OR MORE AUDITS FAILED.")
    print("=" * 72)
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
