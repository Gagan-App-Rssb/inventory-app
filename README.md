# 📦 Inventory Pro — Desktop Inventory Management System

A complete, production-ready inventory management app built with **Python + Streamlit**.  
All data is stored in **Excel files** — no database required.

---

## 🗂️ Folder Structure

```
inventory_app/
├── app.py                  ← Main Streamlit application
├── data_manager.py         ← All Excel read/write & business logic
├── create_sample_data.py   ← Script to generate sample Excel files
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── materials.xlsx          ← Auto-created on first run
└── transactions.xlsx       ← Auto-created on first run
```

---

## 🚀 Installation & Setup

### 1. Install Python
Download Python 3.9+ from https://python.org

### 2. Create a Virtual Environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Load Sample Data
```bash
python create_sample_data.py
```
This creates `materials.xlsx` and `transactions.xlsx` with 10 materials and ~100 transactions.

### 5. Run the App
```bash
streamlit run app.py
```
Open your browser at: **http://localhost:8501**

---

## 📋 Features

| Feature | Details |
|---|---|
| **Material Master** | Add / Edit / Delete materials with code, name, category, unit, description |
| **Transactions** | Record Purchase & Sale transactions; Amount auto-calculated |
| **Live Stock Balance** | Real-time stock panel on the right side of the transaction screen |
| **Dashboard** | KPI cards + Purchase vs Sale trend chart + Stock pie chart |
| **Reports** | Stock, Purchase, Sales, Material Ledger with date & material filters |
| **Import** | Upload Excel files for bulk import with preview & error report |
| **Export** | Download Materials, Transactions, Stock Balance, Full Report as Excel |
| **Backup** | Download ZIP containing all data files |
| **Date Filters** | Global From/To date filter in sidebar applies everywhere |
| **Search** | Search materials and transactions by any field |
| **Dark / Light Mode** | Toggle in sidebar |
| **Confirm Delete** | Two-step confirmation before any delete action |

---

## 📊 Excel File Structure

### `materials.xlsx`
| Column | Description |
|---|---|
| Material Code | Unique identifier (e.g. MAT-001) |
| Material Name | Full descriptive name |
| Category | Material category |
| Unit | Unit of measure (KG, Bag, Pcs…) |
| Description | Optional notes |

### `transactions.xlsx`
| Column | Description |
|---|---|
| Date | Transaction date |
| Material Code | Reference to material |
| Material Name | Material name (denormalized for readability) |
| Type | Purchase or Sale |
| Quantity | Transaction quantity |
| Rate | Unit rate |
| Amount | Auto-calculated (Qty × Rate) |
| Remarks | Optional notes |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **Pandas** — Data manipulation
- **OpenPyXL** — Excel read/write
- **XlsxWriter** — Excel export with formatting
- **Plotly** — Charts & visualizations

---

## 💡 Tips

- Excel files are created automatically on first launch — no manual setup needed.
- The app reads and writes Excel on every action — changes are always saved.
- Use **Import** to bulk-load existing data from your spreadsheets.
- Use **Backup** before making large changes.
- The **Date Filter** in the sidebar applies to the Dashboard, Transactions view, and all Reports.
