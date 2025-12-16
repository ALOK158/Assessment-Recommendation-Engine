import json
import os
from collections import Counter

# CONFIG
FILE_PATH = os.path.join("data", "raw_assessments.json")

def inspect_data():
    if not os.path.exists(FILE_PATH):
        print("[ERROR] File not found.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    print(f"--- DATA AUDIT REPORT (N={total}) ---")

    # 1. DUPLICATE CHECK
    urls = [d['url'] for d in data]
    unique_urls = set(urls)
    if len(urls) != len(unique_urls):
        print(f"[WARN] Found {len(urls) - len(unique_urls)} duplicate URLs. We will need to dedup.")
    else:
        print("[PASS] No duplicates found.")

    # 2. QUALITY CHECK (Empty Fields)
    empty_desc = sum(1 for d in data if not d.get('description') or len(d.get('description')) < 20)
    empty_name = sum(1 for d in data if not d.get('name'))
    
    if empty_desc > 0:
        print(f"[FAIL] {empty_desc} items have missing/short descriptions.")
    else:
        print("[PASS] All descriptions look valid.")

    # 3. TEST TYPE DISTRIBUTION
    # We need to ensure we didn't just tag everything as "General"
    all_types = []
    for d in data:
        all_types.extend(d.get('test_type', []))
    
    type_counts = Counter(all_types)
    print("\n--- TEST TYPE DISTRIBUTION ---")
    for t, c in type_counts.items():
        print(f"  - {t}: {c}")

    # 4. RANDOM SAMPLE (Visual Check)
    print("\n--- RANDOM SAMPLE (Check this manually) ---")
    import random
    sample = random.choice(data)
    print(json.dumps(sample, indent=2))

if __name__ == "__main__":
    inspect_data()