"""
Data Manager - All Excel read/write operations
"""
import pandas as pd
import os
from datetime import datetime
import shutil

MATERIALS_FILE = "materials.xlsx"
TRANSACTIONS_FILE = "transactions.xlsx"

MATERIALS_COLS = ["Material Code", "Material Name", "Category", "Unit", "Description"]
TRANSACTIONS_COLS = ["Date", "Material Code", "Material Name", "Type", "Quantity", "Rate", "Amount", "Remarks"]


# ── helpers ──────────────────────────────────────────────────────────────────

def _ensure_file(path: str, columns: list) -> None:
    if not os.path.exists(path):
        df = pd.DataFrame(columns=columns)
        df.to_excel(path, index=False)


def load_materials() -> pd.DataFrame:
    _ensure_file(MATERIALS_FILE, MATERIALS_COLS)
    df = pd.read_excel(MATERIALS_FILE, dtype=str)
    for col in MATERIALS_COLS:
        if col not in df.columns:
            df[col] = ""
    return df[MATERIALS_COLS].fillna("")


def save_materials(df: pd.DataFrame) -> None:
    df.to_excel(MATERIALS_FILE, index=False)


def load_transactions() -> pd.DataFrame:
    _ensure_file(TRANSACTIONS_FILE, TRANSACTIONS_COLS)
    df = pd.read_excel(TRANSACTIONS_FILE)
    for col in TRANSACTIONS_COLS:
        if col not in df.columns:
            df[col] = None
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").fillna(0)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df["Remarks"] = df["Remarks"].fillna("")
    df["Material Code"] = df["Material Code"].fillna("").astype(str)
    df["Material Name"] = df["Material Name"].fillna("").astype(str)
    return df[TRANSACTIONS_COLS]


def save_transactions(df: pd.DataFrame) -> None:
    df.to_excel(TRANSACTIONS_FILE, index=False)


# ── material CRUD ─────────────────────────────────────────────────────────────

def add_material(code, name, category, unit, description) -> tuple[bool, str]:
    df = load_materials()
    if code in df["Material Code"].values:
        return False, f"Material Code '{code}' already exists."
    new_row = pd.DataFrame([{
        "Material Code": code, "Material Name": name,
        "Category": category, "Unit": unit, "Description": description
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_materials(df)
    return True, "Material added successfully."


def update_material(code, name, category, unit, description) -> tuple[bool, str]:
    df = load_materials()
    idx = df.index[df["Material Code"] == code].tolist()
    if not idx:
        return False, "Material not found."
    df.loc[idx[0], ["Material Name", "Category", "Unit", "Description"]] = [name, category, unit, description]
    save_materials(df)
    return True, "Material updated successfully."


def delete_material(code) -> tuple[bool, str]:
    df = load_materials()
    if code not in df["Material Code"].values:
        return False, "Material not found."
    df = df[df["Material Code"] != code]
    save_materials(df)
    return True, "Material deleted."


# ── transaction CRUD ──────────────────────────────────────────────────────────

def add_transaction(date, mat_code, mat_name, txn_type, qty, rate, remarks) -> tuple[bool, str]:
    df = load_transactions()
    amount = round(float(qty) * float(rate), 2)
    new_row = pd.DataFrame([{
        "Date": date, "Material Code": str(mat_code), "Material Name": mat_name,
        "Type": txn_type, "Quantity": float(qty), "Rate": float(rate),
        "Amount": amount, "Remarks": remarks
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_transactions(df)
    return True, "Transaction saved."


def update_transaction(idx: int, date, mat_code, mat_name, txn_type, qty, rate, remarks) -> tuple[bool, str]:
    df = load_transactions()
    if idx < 0 or idx >= len(df):
        return False, "Invalid transaction index."
    amount = round(float(qty) * float(rate), 2)
    df.loc[idx, :] = [date, str(mat_code), mat_name, txn_type, float(qty), float(rate), amount, remarks]
    save_transactions(df)
    return True, "Transaction updated."


def delete_transaction(idx: int) -> tuple[bool, str]:
    df = load_transactions()
    if idx < 0 or idx >= len(df):
        return False, "Invalid transaction index."
    df = df.drop(index=idx).reset_index(drop=True)
    save_transactions(df)
    return True, "Transaction deleted."


# ── stock calculation ─────────────────────────────────────────────────────────

def calc_stock(df_txn: pd.DataFrame = None) -> pd.DataFrame:
    if df_txn is None:
        df_txn = load_transactions()

    mats = load_materials()

    purchase = df_txn[df_txn["Type"] == "Purchase"].groupby("Material Code")["Quantity"].sum().rename("Purchase Qty")
    sales = df_txn[df_txn["Type"] == "Sale"].groupby("Material Code")["Quantity"].sum().rename("Sale Qty")
    val = df_txn[df_txn["Type"] == "Purchase"].groupby("Material Code").apply(
        lambda x: (x["Quantity"] * x["Rate"]).sum()
    ).rename("Inventory Value")

    stock = pd.DataFrame({"Material Code": mats["Material Code"], "Material Name": mats["Material Name"]})
    stock = stock.merge(purchase, on="Material Code", how="left")
    stock = stock.merge(sales, on="Material Code", how="left")
    stock = stock.merge(val, on="Material Code", how="left")
    stock = stock.fillna(0)
    stock["Current Stock"] = stock["Purchase Qty"] - stock["Sale Qty"]
    return stock[["Material Code", "Material Name", "Purchase Qty", "Sale Qty", "Current Stock", "Inventory Value"]]


# ── import helpers ────────────────────────────────────────────────────────────

def import_materials_from_df(df: pd.DataFrame) -> tuple[int, int, list]:
    existing = load_materials()
    errors = []
    added = 0
    skipped = 0
    required = ["Material Code", "Material Name"]
    for _, row in df.iterrows():
        row = row.fillna("")
        if not all(str(row.get(c, "")).strip() for c in required):
            errors.append(f"Row skipped – missing required fields: {dict(row)}")
            skipped += 1
            continue
        code = str(row.get("Material Code", "")).strip()
        if code in existing["Material Code"].values:
            skipped += 1
            continue
        new_row = pd.DataFrame([{
            "Material Code": code,
            "Material Name": str(row.get("Material Name", "")),
            "Category": str(row.get("Category", "")),
            "Unit": str(row.get("Unit", "")),
            "Description": str(row.get("Description", "")),
        }])
        existing = pd.concat([existing, new_row], ignore_index=True)
        added += 1
    save_materials(existing)
    return added, skipped, errors


def import_transactions_from_df(df: pd.DataFrame) -> tuple[int, int, list]:
    existing = load_transactions()
    errors = []
    added = 0
    skipped = 0
    for _, row in df.iterrows():
        try:
            date = pd.to_datetime(row.get("Date"), errors="coerce")
            if pd.isna(date):
                errors.append(f"Invalid date in row: {dict(row)}")
                skipped += 1
                continue
            qty = float(row.get("Quantity", 0))
            rate = float(row.get("Rate", 0))
            amount = round(qty * rate, 2)
            new_row = pd.DataFrame([{
                "Date": date,
                "Material Code": str(row.get("Material Code", "")),
                "Material Name": str(row.get("Material Name", "")),
                "Type": str(row.get("Type", "Purchase")),
                "Quantity": qty, "Rate": rate, "Amount": amount,
                "Remarks": str(row.get("Remarks", "")),
            }])
            existing = pd.concat([existing, new_row], ignore_index=True)
            added += 1
        except Exception as e:
            errors.append(f"Error in row: {e}")
            skipped += 1
    save_transactions(existing)
    return added, skipped, errors


# ── export helpers ────────────────────────────────────────────────────────────

def export_to_excel_bytes(sheets: dict) -> bytes:
    """sheets = {'Sheet Name': dataframe}"""
    from io import BytesIO
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max() if not df.empty else 0, len(col)) + 2
                ws.set_column(i, i, min(max_len, 40))
    buf.seek(0)
    return buf.read()


# ── backup ────────────────────────────────────────────────────────────────────

def create_backup() -> bytes:
    from io import BytesIO
    import zipfile
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in [MATERIALS_FILE, TRANSACTIONS_FILE]:
            if os.path.exists(f):
                zf.write(f)
    buf.seek(0)
    return buf.read()
