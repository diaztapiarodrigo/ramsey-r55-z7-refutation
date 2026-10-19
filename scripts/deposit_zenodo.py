#!/usr/bin/env python3
"""
deposit_zenodo.py - Automated or manual deposition to Zenodo (CERN) for permanent DOI attribution.
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

ZENODO_BASE_URL = "https://zenodo.org/api"
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"

def main():
    parser = argparse.ArgumentParser(description="Deposit preprint and artifacts to Zenodo for DOI generation")
    parser.add_argument("--token", help="Zenodo Personal Access Token", default=os.environ.get("ZENODO_TOKEN"))
    parser.add_argument("--sandbox", action="store_true", help="Use Zenodo Sandbox environment for testing")
    parser.add_argument("--publish", action="store_true", help="Publish deposition immediately (irreversible)")
    args = parser.parse_args()

    base_url = ZENODO_SANDBOX_URL if args.sandbox else ZENODO_BASE_URL

    if not args.token:
        print("=" * 72)
        print("  ZENODO PERMANENT DOI DEPOSITION GUIDE")
        print("=" * 72)
        print("\nTo obtain an official, permanent DOI (10.5281/zenodo.XXXXX) backed by CERN:")
        print("\nOPTION A (Automated via API):")
        print("  1. Create a Zenodo account at https://zenodo.org (or login with GitHub / ORCID)")
        print("  2. Generate a Personal Access Token at https://zenodo.org/account/settings/applications/tokens/new/")
        print("     (Check the 'deposit:actions' and 'deposit:write' scopes)")
        print("  3. Run this script:")
        print("     python scripts/deposit_zenodo.py --token YOUR_TOKEN")
        print("\nOPTION B (Direct Web Upload - 2 minutes):")
        print("  1. Go to https://zenodo.org/deposit/new")
        print("  2. Upload 'zenodo_package.zip' and 'arxiv_ramsey_r55_n43.pdf' from this repository")
        print("  3. Copy title, authors, and abstract from '.zenodo.json'")
        print("  4. Click 'Save' and 'Publish'")
        print("\nOPTION C (GitHub Automated Archiving):")
        print("  1. Go to https://zenodo.org/account/settings/github/")
        print("  2. Toggle ON the repository 'diaztapiarodrigo/ramsey-r55-z7-refutation'")
        print("  3. Whenever a new GitHub Release is created, Zenodo will automatically archive it and assign a DOI.")
        print("=" * 72)
        return 0

    headers = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json"
    }

    print(f"Connecting to Zenodo ({base_url})...")
    
    # 1. Load metadata from .zenodo.json
    meta_path = os.path.join(os.path.dirname(__file__), "..", ".zenodo.json")
    if not os.path.exists(meta_path):
        meta_path = ".zenodo.json"
    
    with open(meta_path, "r", encoding="utf-8") as f:
        zenodo_meta = json.load(f)

    # 2. Create deposition
    req = urllib.request.Request(f"{base_url}/deposit/depositions", data=json.dumps({"metadata": zenodo_meta}).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            dep_data = json.loads(resp.read().decode())
            dep_id = dep_data["id"]
            bucket_url = dep_data["links"]["bucket"]
            reserved_doi = dep_data.get("metadata", {}).get("prereserve_doi", {}).get("doi", "N/A")
            print(f"[✓] Created Deposition ID: {dep_id}")
            print(f"[✓] Pre-reserved DOI: {reserved_doi}")
    except urllib.error.HTTPError as e:
        print(f"[-] Error creating deposition ({e.code}): {e.read().decode()}")
        return 1

    # 3. Upload files to bucket
    files_to_upload = ["zenodo_package.zip", "arxiv_ramsey_r55_n43.pdf"]
    for filename in files_to_upload:
        filepath = os.path.join(os.path.dirname(__file__), "..", filename)
        if not os.path.exists(filepath):
            filepath = filename
        
        if os.path.exists(filepath):
            print(f"Uploading {filename} ({os.path.getsize(filepath)} bytes)...")
            with open(filepath, "rb") as fp:
                file_data = fp.read()
            upload_req = urllib.request.Request(
                f"{bucket_url}/{filename}",
                data=file_data,
                headers={"Authorization": f"Bearer {args.token}", "Content-Type": "application/octet-stream"},
                method="PUT"
            )
            with urllib.request.urlopen(upload_req) as u_resp:
                print(f"  [✓] Uploaded {filename} (HTTP {u_resp.status})")

    print(f"\n[✓] Deposition prepared successfully at: https://zenodo.org/deposit/{dep_id}")
    if reserved_doi != "N/A":
        print(f"[✓] Reserved DOI: https://doi.org/{reserved_doi}")

    if args.publish:
        print("Publishing deposition...")
        pub_req = urllib.request.Request(f"{base_url}/deposit/depositions/{dep_id}/actions/publish", headers=headers, method="POST")
        with urllib.request.urlopen(pub_req) as pub_resp:
            pub_data = json.loads(pub_resp.read().decode())
            print(f"[✓] Published! DOI: {pub_data.get('doi')}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
