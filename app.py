"""
Inventory Management System — Streamlit App
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go

import data_manager as dm

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Inventory Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── theme / CSS ───────────────────────────────────────────────────────────────
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
  --bg: #0d0f14;
  --surface: #161b24;
  --surface2: #1e2535;
  --border: #2a3347;
  --accent: #4f8ef7;
  --accent2: #f76c4f;
  --green: #2dd4a0;
  --yellow: #f0c040;
  --text: #e8ecf4;
  --muted: #7a8599;
  --radius: 10px;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Syne', sans-serif !important;
}

[data-testid="stSidebar"] {
  background-color: var(--surface) !important;
  border-right: 1px solid var(--border);
}

.block-container { padding-top: 1.5rem !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

.stButton > button {
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  transition: opacity .2s;
}
.stButton > button:hover { opacity: .85; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea,
.stDateInput > div > div > input {
  background: var(--surface2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.4rem;
  margin-bottom: .6rem;
}
.metric-card .label { color: var(--muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; }
.metric-card .value { color: var(--text); font-size: 1.8rem; font-weight: 800; margin-top: .2rem; }
.metric-card .value.accent  { color: var(--accent); }
.metric-card .value.green   { color: var(--green); }
.metric-card .value.yellow  { color: var(--yellow); }
.metric-card .value.red     { color: var(--accent2); }

.section-header {
  font-size: 1.05rem; font-weight: 700; color: var(--accent);
  border-bottom: 2px solid var(--accent); padding-bottom: .4rem; margin-bottom: 1rem;
}

div[data-testid="stDataFrame"] { border-radius: var(--radius) !important; }
div[data-testid="stDataFrame"] table { background: var(--surface) !important; }

.stTabs [data-baseweb="tab"] { font-family: 'Syne', sans-serif !important; font-weight: 600; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom-color: var(--accent) !important; }

.success-pill {
  background: rgba(45,212,160,.15); color: var(--green);
  border: 1px solid rgba(45,212,160,.3); border-radius: 20px;
  padding: .2rem .8rem; font-size: .8rem; display: inline-block;
}
.danger-pill {
  background: rgba(247,108,79,.15); color: var(--accent2);
  border: 1px solid rgba(247,108,79,.3); border-radius: 20px;
  padding: .2rem .8rem; font-size: .8rem; display: inline-block;
}
.info-pill {
  background: rgba(79,142,247,.15); color: var(--accent);
  border: 1px solid rgba(79,142,247,.3); border-radius: 20px;
  padding: .2rem .8rem; font-size: .8rem; display: inline-block;
}

.logo-text {
  font-size: 1.4rem; font-weight: 800; color: var(--accent);
  letter-spacing: -.02em; padding: .5rem 0 1.2rem;
}
.logo-text span { color: var(--green); }

div[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
  --bg: #f4f6fb;
  --surface: #ffffff;
  --surface2: #f0f3fa;
  --border: #d8dff0;
  --accent: #2563eb;
  --accent2: #ef4444;
  --green: #059669;
  --yellow: #d97706;
  --text: #0f172a;
  --muted: #64748b;
  --radius: 10px;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Syne', sans-serif !important;
}
[data-testid="stSidebar"] {
  background-color: var(--surface) !important;
  border-right: 1px solid var(--border);
}
.block-container { padding-top: 1.5rem !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
.stButton > button {
  background: var(--accent) !important; color: #fff !important;
  border: none !important; border-radius: var(--radius) !important;
  font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
}
.stButton > button:hover { opacity: .85; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea,
.stDateInput > div > div > input {
  background: var(--surface2) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; border-radius: 8px !important;
}
.metric-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1.2rem 1.4rem; margin-bottom: .6rem;
}
.metric-card .label { color: var(--muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; }
.metric-card .value { color: var(--text); font-size: 1.8rem; font-weight: 800; margin-top: .2rem; }
.metric-card .value.accent { color: var(--accent); }
.metric-card .value.green  { color: var(--green); }
.metric-card .value.yellow { color: var(--yellow); }
.metric-card .value.red    { color: var(--accent2); }
.section-header {
  font-size: 1.05rem; font-weight: 700; color: var(--accent);
  border-bottom: 2px solid var(--accent); padding-bottom: .4rem; margin-bottom: 1rem;
}
.success-pill { background: #ecfdf5; color: var(--green); border: 1px solid #6ee7b7; border-radius: 20px; padding: .2rem .8rem; font-size: .8rem; display: inline-block; }
.danger-pill  { background: #fef2f2; color: var(--accent2); border: 1px solid #fca5a5; border-radius: 20px; padding: .2rem .8rem; font-size: .8rem; display: inline-block; }
.info-pill    { background: #eff6ff; color: var(--accent); border: 1px solid #93c5fd; border-radius: 20px; padding: .2rem .8rem; font-size: .8rem; display: inline-block; }
.logo-text { font-size: 1.4rem; font-weight: 800; color: var(--accent); letter-spacing: -.02em; padding: .5rem 0 1.2rem; }
.logo-text span { color: var(--green); }
div[data-testid="stExpander"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; }
</style>
"""


# ── session state ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

st.markdown(DARK_CSS if st.session_state.dark_mode else LIGHT_CSS, unsafe_allow_html=True)


# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-text">Inventory<span>Pro</span></div>', unsafe_allow_html=True)

    pages = {
        "📊 Dashboard": "Dashboard",
        "🧱 Materials": "Materials",
        "↔️ Transactions": "Transactions",
        "📈 Reports": "Reports",
        "📥 Import": "Import",
        "📤 Export": "Export",
        "⚙️ Settings": "Settings",
    }
    for label, key in pages.items():
        active = st.session_state.page == key
        if st.button(label, use_container_width=True, type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.divider()
    st.caption("Global Date Filter")
    from_date = st.date_input("From", value=date.today() - timedelta(days=90), key="global_from")
    to_date   = st.date_input("To",   value=date.today(),                       key="global_to")

    st.divider()
    dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_toggle
        st.rerun()

page = st.session_state.page


# ── helpers ───────────────────────────────────────────────────────────────────

def metric_card(label: str, value, cls: str = "accent"):
    return f"""
<div class="metric-card">
  <div class="label">{label}</div>
  <div class="value {cls}">{value}</div>
</div>"""


def filter_txn_by_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    mask = (df["Date"].dt.date >= from_date) & (df["Date"].dt.date <= to_date)
    return df[mask]


def fmt_num(n, decimals=0):
    if decimals:
        return f"{n:,.{decimals}f}"
    return f"{int(n):,}"


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.title("📊 Dashboard")

    df_txn  = filter_txn_by_dates(dm.load_transactions())
    df_mat  = dm.load_materials()
    df_stock = dm.calc_stock(df_txn)

    total_mats     = len(df_mat)
    total_purchase = df_txn[df_txn["Type"] == "Purchase"]["Quantity"].sum()
    total_sales    = df_txn[df_txn["Type"] == "Sale"]["Quantity"].sum()
    current_stock  = total_purchase - total_sales
    inv_value      = df_txn[df_txn["Type"] == "Purchase"].apply(lambda r: r["Quantity"] * r["Rate"], axis=1).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(metric_card("Total Materials",      fmt_num(total_mats),     "accent"),  unsafe_allow_html=True)
    c2.markdown(metric_card("Total Purchased",      fmt_num(total_purchase), "green"),   unsafe_allow_html=True)
    c3.markdown(metric_card("Total Sold",           fmt_num(total_sales),    "yellow"),  unsafe_allow_html=True)
    c4.markdown(metric_card("Current Stock",        fmt_num(current_stock),  "green"),   unsafe_allow_html=True)
    c5.markdown(metric_card("Inventory Value ₹",    fmt_num(inv_value, 2),   "accent"),  unsafe_allow_html=True)

    st.markdown("---")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header">Purchase vs Sale Trend</div>', unsafe_allow_html=True)
        if not df_txn.empty:
            trend = df_txn.copy()
            trend["Month"] = trend["Date"].dt.to_period("M").astype(str)
            trend_g = trend.groupby(["Month", "Type"])["Quantity"].sum().reset_index()
            fig = px.bar(trend_g, x="Month", y="Quantity", color="Type",
                         barmode="group",
                         color_discrete_map={"Purchase": "#4f8ef7", "Sale": "#f76c4f"},
                         template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              legend=dict(orientation="h", y=-0.2), margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No transactions in selected date range.")

    with col_right:
        st.markdown('<div class="section-header">Stock by Material</div>', unsafe_allow_html=True)
        if not df_stock.empty and df_stock["Current Stock"].sum() > 0:
            top = df_stock[df_stock["Current Stock"] > 0].nlargest(8, "Current Stock")
            fig2 = px.pie(top, names="Material Name", values="Current Stock",
                          hole=.45,
                          color_discrete_sequence=px.colors.qualitative.Bold,
                          template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No stock data.")

    st.markdown('<div class="section-header">Recent Transactions</div>', unsafe_allow_html=True)
    if not df_txn.empty:
        recent = df_txn.sort_values("Date", ascending=False).head(10).copy()
        recent["Date"] = recent["Date"].dt.strftime("%d-%b-%Y")
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: MATERIALS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Materials":
    st.title("🧱 Material Master")

    df_mat = dm.load_materials()

    tab_list, tab_add, tab_edit = st.tabs(["📋 Material List", "➕ Add Material", "✏️ Edit / Delete"])

    # ── list ──────────────────────────────────────────────────────────────────
    with tab_list:
        search = st.text_input("🔍 Search materials", placeholder="Search by code, name, category…")
        df_show = df_mat.copy()
        if search:
            mask = df_show.apply(lambda r: search.lower() in r.astype(str).str.lower().str.cat(sep=" "), axis=1)
            df_show = df_show[mask]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_show)} of {len(df_mat)} materials shown")

    # ── add ───────────────────────────────────────────────────────────────────
    with tab_add:
        st.markdown('<div class="section-header">New Material</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            n_code  = st.text_input("Material Code *", placeholder="e.g. MAT-001")
            n_name  = st.text_input("Material Name *", placeholder="e.g. Cement Bag 50 kg")
            n_cat   = st.text_input("Category",        placeholder="e.g. Raw Material")
        with a2:
            n_unit  = st.text_input("Unit",            placeholder="e.g. KG, Bag, Pcs")
            n_desc  = st.text_area("Description",      placeholder="Optional description", height=120)
        if st.button("💾 Save Material", type="primary"):
            if not n_code.strip() or not n_name.strip():
                st.error("Material Code and Name are required.")
            else:
                ok, msg = dm.add_material(n_code.strip(), n_name.strip(), n_cat, n_unit, n_desc)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # ── edit / delete ─────────────────────────────────────────────────────────
    with tab_edit:
        if df_mat.empty:
            st.info("No materials yet.")
        else:
            selected_code = st.selectbox("Select Material to Edit/Delete",
                                         options=df_mat["Material Code"].tolist(),
                                         format_func=lambda c: f"{c} — {df_mat.loc[df_mat['Material Code']==c,'Material Name'].values[0]}")
            row = df_mat[df_mat["Material Code"] == selected_code].iloc[0]
            e1, e2 = st.columns(2)
            with e1:
                e_name = st.text_input("Material Name", value=row["Material Name"], key="e_name")
                e_cat  = st.text_input("Category",      value=row["Category"],      key="e_cat")
                e_unit = st.text_input("Unit",           value=row["Unit"],          key="e_unit")
            with e2:
                e_desc = st.text_area("Description", value=row["Description"], height=130, key="e_desc")

            col_save, col_del = st.columns([1, 1])
            with col_save:
                if st.button("💾 Update Material", type="primary"):
                    ok, msg = dm.update_material(selected_code, e_name, e_cat, e_unit, e_desc)
                    st.success(msg) if ok else st.error(msg)
                    st.rerun()
            with col_del:
                if st.session_state.confirm_delete == ("mat", selected_code):
                    st.warning(f"Confirm delete **{selected_code}**?")
                    if st.button("✅ Yes, Delete", type="primary"):
                        ok, msg = dm.delete_material(selected_code)
                        st.session_state.confirm_delete = None
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()
                    if st.button("❌ Cancel"):
                        st.session_state.confirm_delete = None
                        st.rerun()
                else:
                    if st.button("🗑️ Delete Material"):
                        st.session_state.confirm_delete = ("mat", selected_code)
                        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TRANSACTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Transactions":
    st.title("↔️ Inventory Transactions")

    df_mat  = dm.load_materials()
    df_txn  = dm.load_transactions()
    df_txn_filtered = filter_txn_by_dates(df_txn)

    left, right = st.columns([3, 2])

    # ── left: form + list ─────────────────────────────────────────────────────
    with left:
        tab_add, tab_list, tab_edit = st.tabs(["➕ New Transaction", "📋 Transaction List", "✏️ Edit / Delete"])

        with tab_add:
            st.markdown('<div class="section-header">Record Transaction</div>', unsafe_allow_html=True)
            if df_mat.empty:
                st.warning("Please add materials first.")
            else:
                r1, r2 = st.columns(2)
                with r1:
                    t_date = st.date_input("Transaction Date", value=date.today())
                    mat_options = df_mat.apply(lambda r: f"{r['Material Code']} — {r['Material Name']}", axis=1).tolist()
                    mat_sel = st.selectbox("Material *", options=mat_options)
                    mat_code = mat_sel.split(" — ")[0]
                    mat_name = mat_sel.split(" — ")[1] if " — " in mat_sel else mat_sel
                with r2:
                    t_type = st.selectbox("Type", ["Purchase", "Sale"])
                    t_qty  = st.number_input("Quantity *", min_value=0.0, step=1.0, format="%.2f")
                    t_rate = st.number_input("Rate ₹ *",   min_value=0.0, step=0.01, format="%.2f")

                t_amount  = round(t_qty * t_rate, 2)
                t_remarks = st.text_input("Remarks", placeholder="Optional note")

                st.markdown(f"**Auto Amount: ₹ {t_amount:,.2f}**")

                if st.button("💾 Save Transaction", type="primary"):
                    if t_qty <= 0 or t_rate < 0:
                        st.error("Quantity must be > 0.")
                    else:
                        ok, msg = dm.add_transaction(t_date, mat_code, mat_name, t_type, t_qty, t_rate, t_remarks)
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()

        with tab_list:
            search_t = st.text_input("🔍 Search transactions")
            df_show  = df_txn_filtered.copy()
            if search_t:
                mask = df_show.apply(lambda r: search_t.lower() in r.astype(str).str.lower().str.cat(sep=" "), axis=1)
                df_show = df_show[mask]
            df_show_display = df_show.copy()
            df_show_display["Date"] = df_show_display["Date"].dt.strftime("%d-%b-%Y")
            st.dataframe(df_show_display, use_container_width=True, hide_index=True)
            st.caption(f"{len(df_show)} transactions")

        with tab_edit:
            if df_txn_filtered.empty:
                st.info("No transactions in date range.")
            else:
                df_txn_full = dm.load_transactions()
                # Build display labels with original global index
                txn_labels = []
                txn_indices = []
                for gi, row in df_txn_full.iterrows():
                    d = row["Date"]
                    d_str = d.strftime("%d-%b-%Y") if pd.notna(d) else "?"
                    txn_labels.append(f"#{gi} | {d_str} | {row['Material Name']} | {row['Type']} | {row['Quantity']}")
                    txn_indices.append(gi)

                sel_label = st.selectbox("Select Transaction", options=txn_labels)
                sel_idx   = txn_indices[txn_labels.index(sel_label)]
                row = df_txn_full.iloc[sel_idx]

                ea, eb = st.columns(2)
                with ea:
                    ed_date = st.date_input("Date", value=row["Date"].date() if pd.notna(row["Date"]) else date.today(), key="ed_d")
                    ed_type = st.selectbox("Type", ["Purchase", "Sale"], index=0 if row["Type"]=="Purchase" else 1, key="ed_t")
                    ed_qty  = st.number_input("Quantity", value=float(row["Quantity"]), min_value=0.0, step=1.0, key="ed_q")
                with eb:
                    ed_rate = st.number_input("Rate", value=float(row["Rate"]), min_value=0.0, step=0.01, key="ed_r")
                    ed_rem  = st.text_input("Remarks", value=str(row["Remarks"]), key="ed_rem")

                ed_amount = round(ed_qty * ed_rate, 2)
                st.markdown(f"**Amount: ₹ {ed_amount:,.2f}**")

                col_u, col_d = st.columns(2)
                with col_u:
                    if st.button("💾 Update", type="primary"):
                        ok, msg = dm.update_transaction(sel_idx, ed_date, row["Material Code"], row["Material Name"], ed_type, ed_qty, ed_rate, ed_rem)
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()
                with col_d:
                    if st.session_state.confirm_delete == ("txn", sel_idx):
                        st.warning("Confirm delete?")
                        if st.button("✅ Yes, Delete", type="primary"):
                            ok, msg = dm.delete_transaction(sel_idx)
                            st.session_state.confirm_delete = None
                            st.success(msg) if ok else st.error(msg)
                            st.rerun()
                        if st.button("❌ Cancel"):
                            st.session_state.confirm_delete = None
                            st.rerun()
                    else:
                        if st.button("🗑️ Delete"):
                            st.session_state.confirm_delete = ("txn", sel_idx)
                            st.rerun()

    # ── right: live stock ─────────────────────────────────────────────────────
    with right:
        st.markdown('<div class="section-header">📦 Live Stock Balance</div>', unsafe_allow_html=True)
        df_stock = dm.calc_stock()  # always full stock

        mat_filter = st.text_input("Filter materials", placeholder="Type to filter…", key="stock_filter")
        df_s = df_stock.copy()
        if mat_filter:
            df_s = df_s[df_s["Material Name"].str.contains(mat_filter, case=False, na=False)]

        for _, row in df_s.iterrows():
            stock_cls = "green" if row["Current Stock"] > 0 else ("yellow" if row["Current Stock"] == 0 else "red")
            st.markdown(f"""
<div class="metric-card" style="margin-bottom:.5rem;padding:.8rem 1rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div class="label">{row['Material Code']}</div>
      <div style="font-weight:700;font-size:.95rem;">{row['Material Name']}</div>
    </div>
    <div class="value {stock_cls}" style="font-size:1.4rem;">{fmt_num(row['Current Stock'])}</div>
  </div>
  <div style="display:flex;gap:1rem;margin-top:.5rem;font-size:.78rem;color:var(--muted);">
    <span>🟢 In: {fmt_num(row['Purchase Qty'])}</span>
    <span>🔴 Out: {fmt_num(row['Sale Qty'])}</span>
    <span>💰 ₹{fmt_num(row['Inventory Value'],2)}</span>
  </div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REPORTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Reports":
    st.title("📈 Reports")

    df_txn  = filter_txn_by_dates(dm.load_transactions())
    df_mat  = dm.load_materials()
    df_stock = dm.calc_stock(df_txn)

    mat_options = ["All"] + df_mat["Material Name"].tolist()
    mat_filter  = st.selectbox("Filter by Material", mat_options)

    tab_stock, tab_purchase, tab_sales, tab_ledger = st.tabs(
        ["📦 Stock Report", "🛒 Purchase Report", "💰 Sales Report", "📒 Material Ledger"])

    def apply_mat_filter(df: pd.DataFrame) -> pd.DataFrame:
        if mat_filter != "All":
            df = df[df["Material Name"] == mat_filter]
        return df

    with tab_stock:
        st.markdown('<div class="section-header">Stock Report</div>', unsafe_allow_html=True)
        df_s = apply_mat_filter(df_stock) if mat_filter != "All" else df_stock.copy()
        st.dataframe(df_s, use_container_width=True, hide_index=True)

        fig = px.bar(df_s.nlargest(15, "Current Stock"), x="Material Name", y="Current Stock",
                     color="Current Stock", color_continuous_scale="blues",
                     template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab_purchase:
        st.markdown('<div class="section-header">Purchase Report</div>', unsafe_allow_html=True)
        df_p = df_txn[df_txn["Type"] == "Purchase"].copy()
        df_p = apply_mat_filter(df_p)
        df_p["Date"] = df_p["Date"].dt.strftime("%d-%b-%Y")
        st.dataframe(df_p, use_container_width=True, hide_index=True)
        st.metric("Total Purchase Amount", f"₹ {df_p['Amount'].sum():,.2f}")

    with tab_sales:
        st.markdown('<div class="section-header">Sales Report</div>', unsafe_allow_html=True)
        df_sl = df_txn[df_txn["Type"] == "Sale"].copy()
        df_sl = apply_mat_filter(df_sl)
        df_sl["Date"] = df_sl["Date"].dt.strftime("%d-%b-%Y")
        st.dataframe(df_sl, use_container_width=True, hide_index=True)
        st.metric("Total Sales Amount", f"₹ {df_sl['Amount'].sum():,.2f}")

    with tab_ledger:
        st.markdown('<div class="section-header">Material Ledger</div>', unsafe_allow_html=True)
        if mat_filter == "All":
            st.info("Select a specific material to see its ledger.")
        else:
            df_l = df_txn[df_txn["Material Name"] == mat_filter].copy().sort_values("Date")
            running_stock = 0
            rows = []
            for _, r in df_l.iterrows():
                if r["Type"] == "Purchase":
                    running_stock += r["Quantity"]
                else:
                    running_stock -= r["Quantity"]
                rows.append({**r, "Running Stock": running_stock})
            df_ledger = pd.DataFrame(rows)
            if not df_ledger.empty:
                df_ledger["Date"] = df_ledger["Date"].dt.strftime("%d-%b-%Y")
            st.dataframe(df_ledger, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: IMPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Import":
    st.title("📥 Excel Import")
    tab_m, tab_t = st.tabs(["📦 Import Materials", "↔️ Import Transactions"])

    with tab_m:
        st.markdown('<div class="section-header">Import Materials from Excel</div>', unsafe_allow_html=True)
        st.caption("Required columns: Material Code, Material Name. Optional: Category, Unit, Description")
        uploaded = st.file_uploader("Upload materials Excel file", type=["xlsx", "xls"], key="imp_mat")
        if uploaded:
            try:
                df_prev = pd.read_excel(uploaded)
                st.markdown("**Preview (first 10 rows):**")
                st.dataframe(df_prev.head(10), use_container_width=True, hide_index=True)

                missing = [c for c in ["Material Code", "Material Name"] if c not in df_prev.columns]
                if missing:
                    st.error(f"Missing required columns: {missing}")
                else:
                    if st.button("✅ Import Materials", type="primary"):
                        added, skipped, errors = dm.import_materials_from_df(df_prev)
                        st.success(f"Imported: {added} | Skipped: {skipped}")
                        if errors:
                            with st.expander("⚠️ Error Report"):
                                for e in errors:
                                    st.text(e)
                        st.rerun()
            except Exception as ex:
                st.error(f"Error reading file: {ex}")

    with tab_t:
        st.markdown('<div class="section-header">Import Transactions from Excel</div>', unsafe_allow_html=True)
        st.caption("Required columns: Date, Material Code, Material Name, Type, Quantity, Rate. Optional: Remarks")
        uploaded2 = st.file_uploader("Upload transactions Excel file", type=["xlsx", "xls"], key="imp_txn")
        if uploaded2:
            try:
                df_prev2 = pd.read_excel(uploaded2)
                st.markdown("**Preview (first 10 rows):**")
                st.dataframe(df_prev2.head(10), use_container_width=True, hide_index=True)
                req_cols = ["Date", "Material Code", "Quantity", "Rate", "Type"]
                missing2 = [c for c in req_cols if c not in df_prev2.columns]
                if missing2:
                    st.error(f"Missing required columns: {missing2}")
                else:
                    if st.button("✅ Import Transactions", type="primary"):
                        added2, skipped2, errors2 = dm.import_transactions_from_df(df_prev2)
                        st.success(f"Imported: {added2} | Skipped: {skipped2}")
                        if errors2:
                            with st.expander("⚠️ Error Report"):
                                for e in errors2:
                                    st.text(e)
                        st.rerun()
            except Exception as ex:
                st.error(f"Error reading file: {ex}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Export":
    st.title("📤 Excel Export")

    df_mat  = dm.load_materials()
    df_txn  = filter_txn_by_dates(dm.load_transactions())
    df_stock = dm.calc_stock(df_txn)

    st.markdown('<div class="section-header">Download Reports</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📦 Material List**")
        mat_bytes = dm.export_to_excel_bytes({"Materials": df_mat})
        st.download_button("⬇️ Download Materials.xlsx", data=mat_bytes,
                           file_name="Materials.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("**📈 Stock Balance**")
        stock_bytes = dm.export_to_excel_bytes({"Stock Balance": df_stock})
        st.download_button("⬇️ Download StockBalance.xlsx", data=stock_bytes,
                           file_name="StockBalance.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col2:
        st.markdown("**↔️ Transactions**")
        txn_bytes = dm.export_to_excel_bytes({"Transactions": df_txn})
        st.download_button("⬇️ Download Transactions.xlsx", data=txn_bytes,
                           file_name="Transactions.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("**📑 Full Inventory Report**")
        df_p  = df_txn[df_txn["Type"] == "Purchase"].copy()
        df_s  = df_txn[df_txn["Type"] == "Sale"].copy()
        report_bytes = dm.export_to_excel_bytes({
            "Materials": df_mat,
            "Transactions": df_txn,
            "Stock Balance": df_stock,
            "Purchases": df_p,
            "Sales": df_s,
        })
        st.download_button("⬇️ Download FullReport.xlsx", data=report_bytes,
                           file_name="InventoryReport.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.divider()
    st.markdown('<div class="section-header">🔒 Backup</div>', unsafe_allow_html=True)
    st.caption("Download a ZIP backup of all Excel data files.")
    backup_bytes = dm.create_backup()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button("⬇️ Download Backup.zip", data=backup_bytes,
                       file_name=f"inventory_backup_{ts}.zip", mime="application/zip")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Settings":
    st.title("⚙️ Settings")

    st.markdown('<div class="section-header">Application Info</div>', unsafe_allow_html=True)
    df_mat = dm.load_materials()
    df_txn = dm.load_transactions()
    i1, i2, i3 = st.columns(3)
    i1.metric("Total Materials",    len(df_mat))
    i2.metric("Total Transactions", len(df_txn))
    i3.metric("Data Files",         "2 (xlsx)")

    st.markdown('<div class="section-header">Danger Zone</div>', unsafe_allow_html=True)
    st.warning("⚠️ The following actions are irreversible. Make a backup first.")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.session_state.confirm_delete == "clear_txn":
            st.error("This will delete ALL transactions!")
            if st.button("✅ Confirm Clear Transactions", type="primary"):
                dm.save_transactions(pd.DataFrame(columns=dm.TRANSACTIONS_COLS))
                st.session_state.confirm_delete = None
                st.success("All transactions cleared.")
                st.rerun()
            if st.button("❌ Cancel"):
                st.session_state.confirm_delete = None
                st.rerun()
        else:
            if st.button("🗑️ Clear All Transactions"):
                st.session_state.confirm_delete = "clear_txn"
                st.rerun()

    with col_b:
        if st.session_state.confirm_delete == "clear_all":
            st.error("This will delete ALL materials AND transactions!")
            if st.button("✅ Confirm Clear Everything", type="primary"):
                dm.save_materials(pd.DataFrame(columns=dm.MATERIALS_COLS))
                dm.save_transactions(pd.DataFrame(columns=dm.TRANSACTIONS_COLS))
                st.session_state.confirm_delete = None
                st.success("All data cleared.")
                st.rerun()
            if st.button("❌ Cancel "):
                st.session_state.confirm_delete = None
                st.rerun()
        else:
            if st.button("💣 Clear ALL Data"):
                st.session_state.confirm_delete = "clear_all"
                st.rerun()

    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown("""
**Inventory Pro** — Desktop Inventory Management System

- **Storage**: Excel files (`materials.xlsx`, `transactions.xlsx`)
- **Framework**: Streamlit + Pandas + OpenPyXL
- **Features**: Material master, Transactions, Stock balance, Reports, Import/Export, Backup
""")
