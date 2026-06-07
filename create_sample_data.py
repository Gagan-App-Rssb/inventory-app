"""
Run this once to generate sample Excel data files for testing.
Usage: python create_sample_data.py
"""
import pandas as pd
from datetime import datetime, timedelta
import random

MATERIALS = [
    ("MAT-001", "Cement Bag 50 kg",         "Raw Material",  "Bag",  "OPC 53 grade cement"),
    ("MAT-002", "Steel Rod 12mm",           "Raw Material",  "KG",   "TMT steel rods"),
    ("MAT-003", "River Sand",               "Raw Material",  "CFT",  "Fine aggregate"),
    ("MAT-004", "Crushed Stone 20mm",        "Raw Material",  "CFT",  "Coarse aggregate"),
    ("MAT-005", "Fly Ash Brick",            "Building",      "Pcs",  "230x110x75 mm"),
    ("MAT-006", "PVC Pipe 4 inch",          "Plumbing",      "Mtr",  "Heavy duty ISI marked"),
    ("MAT-007", "Paint Interior 20L",       "Finishing",     "Tin",  "Emulsion paint"),
    ("MAT-008", "Plywood 18mm",             "Woodwork",      "Sheet","BWR grade"),
    ("MAT-009", "Ceramic Tile 2x2",         "Finishing",     "Box",  "Digital print"),
    ("MAT-010", "Electrical Wire 2.5 sq mm","Electrical",    "Mtr",  "Copper FR wire"),
]

df_mat = pd.DataFrame(MATERIALS, columns=["Material Code","Material Name","Category","Unit","Description"])
df_mat.to_excel("materials.xlsx", index=False)
print("✅ materials.xlsx created")

# Transactions
records = []
today = datetime.today()
rates = {
    "MAT-001": 380, "MAT-002": 68, "MAT-003": 55, "MAT-004": 48,
    "MAT-005": 9,   "MAT-006": 85, "MAT-007": 2600, "MAT-008": 1800,
    "MAT-009": 1200, "MAT-010": 22,
}

for mat_code, mat_name, *_ in MATERIALS:
    # 5-10 purchases over last 90 days
    for _ in range(random.randint(5, 10)):
        d = today - timedelta(days=random.randint(1, 90))
        qty = random.randint(10, 200)
        rate = rates[mat_code] * random.uniform(0.95, 1.05)
        records.append({
            "Date": d.strftime("%Y-%m-%d"),
            "Material Code": mat_code, "Material Name": mat_name,
            "Type": "Purchase",
            "Quantity": qty, "Rate": round(rate, 2),
            "Amount": round(qty * rate, 2),
            "Remarks": "Stock purchase"
        })
    # 3-7 sales
    for _ in range(random.randint(3, 7)):
        d = today - timedelta(days=random.randint(1, 60))
        qty = random.randint(5, 50)
        rate = rates[mat_code] * random.uniform(1.05, 1.20)
        records.append({
            "Date": d.strftime("%Y-%m-%d"),
            "Material Code": mat_code, "Material Name": mat_name,
            "Type": "Sale",
            "Quantity": qty, "Rate": round(rate, 2),
            "Amount": round(qty * rate, 2),
            "Remarks": "Site issue"
        })

df_txn = pd.DataFrame(records)
df_txn = df_txn.sort_values("Date").reset_index(drop=True)
df_txn.to_excel("transactions.xlsx", index=False)
print(f"✅ transactions.xlsx created — {len(df_txn)} records")
print("\nAll done! Run: streamlit run app.py")
