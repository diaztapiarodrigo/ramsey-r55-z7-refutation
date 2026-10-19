import subprocess
import time

def verify_leaves_with_drat_trim():
    print("=" * 72)
    print("  VEKTOR-INTELLIGENCE: REAL DRAT-TRIM TRACE RE-VERIFICATION")
    print("  Running drat-trim inside isolated Docker container (vektor-sat-verifier)")
    print("=" * 72)

    # 1. Start long-lived verification container
    subprocess.run(['docker', 'rm', '-f', 'vektor_drat_runner'], capture_output=True)
    subprocess.run(['docker', 'run', '-d', '--name', 'vektor_drat_runner', 'vektor-sat-verifier:latest', 'sleep', '1200'], check=True)
    
    # 2. Copy drat-trim binary into container
    subprocess.run(['docker', 'cp', 'scratch/bin/drat-trim', 'vektor_drat_runner:/usr/local/bin/drat-trim'], check=True)
    subprocess.run(['docker', 'exec', '-i', 'vektor_drat_runner', 'chmod', '+x', '/usr/local/bin/drat-trim'], check=True)

    # 3. Test suite of leaves: several small leaves + 1 medium leaf
    leaves_to_test = [
        ('c214_m1', 'scratch/c214_leaves/c214_m1.cnf', 'scratch/c214_leaves/c214_m1.drat'),
        ('c214_m2', 'scratch/c214_leaves/c214_m2.cnf', 'scratch/c214_leaves/c214_m2.drat'),
        ('c214_m3', 'scratch/c214_leaves/c214_m3.cnf', 'scratch/c214_leaves/c214_m3.drat'),
        ('c202_m0_s0', 'scratch/c202_leaves/c202_m0_s0.cnf', 'scratch/c202_leaves/c202_m0_s0.drat'),
        ('c202_m0_s1', 'scratch/c202_leaves/c202_m0_s1.cnf', 'scratch/c202_leaves/c202_m0_s1.drat'),
        ('c202_m0_s3', 'scratch/c202_leaves/c202_m0_s3.cnf', 'scratch/c202_leaves/c202_m0_s3.drat'),
        ('c202_m1', 'scratch/c202_leaves/c202_m1.cnf', 'scratch/c202_leaves/c202_m1.drat'),
        ('c202_m2', 'scratch/c202_leaves/c202_m2.cnf', 'scratch/c202_leaves/c202_m2.drat'),
        ('c202_m3', 'scratch/c202_leaves/c202_m3.cnf', 'scratch/c202_leaves/c202_m3.drat'),
    ]

    results = []
    for name, cnf_path, drat_path in leaves_to_test:
        print(f"\n[CHECK] Re-verifying proof trace for leaf: {name} ...")
        # Copy CNF and DRAT into container
        subprocess.run(['docker', 'cp', cnf_path, f'vektor_drat_runner:/tmp/{name}.cnf'], check=True)
        subprocess.run(['docker', 'cp', drat_path, f'vektor_drat_runner:/tmp/{name}.drat'], check=True)

        t0 = time.perf_counter()
        p = subprocess.run(['docker', 'exec', '-i', 'vektor_drat_runner',
                            '/usr/local/bin/drat-trim', f'/tmp/{name}.cnf', f'/tmp/{name}.drat', '-t', '300'],
                           capture_output=True, text=True)
        dt = time.perf_counter() - t0

        out = p.stdout.replace('\r', '\n')
        is_verified = ("s VERIFIED" in out) and ("NOT VERIFIED" not in out) and (p.returncode == 0)
        
        status_str = "VERIFIED (s VERIFIED)" if is_verified else "FAILED"
        print(f"  Result: {status_str} [exit {p.returncode}] in {dt:.2f}s")
        for line in out.splitlines():
            line_s = line.strip()
            if line_s.startswith("s ") or line_s.startswith("c verification") or "conflict" in line_s or "parsed" in line_s:
                print(f"    {line_s}")

        # Clean up temporary files inside container
        subprocess.run(['docker', 'exec', '-i', 'vektor_drat_runner', 'rm', '-f', f'/tmp/{name}.cnf', f'/tmp/{name}.drat'], capture_output=True)

        results.append((name, is_verified, dt, p.returncode))

    subprocess.run(['docker', 'rm', '-f', 'vektor_drat_runner'], capture_output=True)

    print("\n" + "=" * 72)
    print("  RE-VERIFICATION SUMMARY:")
    all_ok = True
    for name, ok, dt, code in results:
        mark = "[PASS]" if ok else "[FAIL]"
        print(f"    {mark} {name:15s} : {dt:6.2f}s (exit {code})")
        if not ok:
            all_ok = False
    print("=" * 72)
    if all_ok:
        print("  ALL TESTED DRAT PROOF TRACES FORMALLY ACCEPTED BY DRAT-TRIM (EXIT 0)")
    else:
        print("  VERIFICATION FAILED ON AT LEAST ONE TRACE")
    return 0 if all_ok else 1

if __name__ == '__main__':
    import sys
    sys.exit(verify_leaves_with_drat_trim())
