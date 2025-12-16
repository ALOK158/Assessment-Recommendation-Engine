import json
import pandas as pd
import os

# CONFIG
FILE_PATH = os.path.join("data", "raw_assessments.json")

def validate_data():
    if not os.path.exists(FILE_PATH):
        print("[ERROR] File not found at: " + FILE_PATH)
        return

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load JSON: {e}")
        return

    df = pd.DataFrame(data)
    
    print("--- DATA HEALTH REPORT ---")
    print(f"Total Records Scraped: {len(df)}")
    
    # 1. QUANTITY CHECK
    if len(df) >= 377:
        print("[PASS] Requirement Met: >= 377 assessments found.")
    else:
        print(f"[WARN] Count is low ({len(df)}). Check pagination or filters.")

    # 2. NULL CHECK (Critical for RAG)
    if 'description' in df.columns:
        empty_desc = df[df['description'].str.strip() == ""].shape[0]
        if empty_desc == 0:
            print("[PASS] Quality Check: All descriptions are populated.")
        else:
            print(f"[FAIL] CRITICAL: {empty_desc} items have EMPTY descriptions.")
    else:
        print("[FAIL] Column 'description' not found!")

    # 3. SCHEMA CHECK
    if 'test_type' in df.columns:
        # Check if 'test_type' is actually a list and not empty
        empty_types = df[df['test_type'].apply(lambda x: len(x) == 0)].shape[0]
        print(f"[INFO] Items with 'General' or missing Test Type: {empty_types}")
    else:
        print("[FAIL] Column 'test_type' not found!")
    
    # 4. SPOT CHECK PREVIEW
    print("\n--- RANDOM SPOT CHECK (Top 3) ---")
    if not df.empty:
        cols_to_show = [c for c in ['name', 'duration', 'test_type'] if c in df.columns]
        print(df[cols_to_show].sample(min(3, len(df))).to_string())

if __name__ == "__main__":
    validate_data()