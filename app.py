"""
CS Operations Intelligence Dashboard
=====================================
A comprehensive tool for Customer Success Operations teams combining:
- Renewal & Churn Forecasting (Option A)
- EBR Preparation Workflow (Option B)
- Automated Reporting & Alerts (Option C)

Built to demonstrate operational excellence for CS Ops leadership.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="CS Ops Intelligence Dashboard",
    page_icon="https://www.sumologic.com/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Design System ---
COLORS = {
    "primary": "#0F2B46",       # Deep navy
    "primary_light": "#1A3F5C",
    "accent": "#00B4D8",        # Vibrant cyan
    "accent_alt": "#7B61FF",    # Purple accent
    "success": "#06D6A0",       # Mint green
    "warning": "#FFB703",       # Amber
    "danger": "#EF476F",        # Coral red
    "danger_dark": "#C1334A",
    "text": "#0F172A",
    "text_muted": "#334155",
    "bg_card": "#FFFFFF",
    "bg_page": "#F1F5F9",
    "bg_sidebar": "#0F2B46",
    "border": "#E2E8F0",
    "gradient_start": "#0F2B46",
    "gradient_end": "#00B4D8",
}

CHART_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color=COLORS["text"], size=12),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(gridcolor="#F1F5F9", gridwidth=1, zeroline=False),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
)

# --- Custom CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {{
        background-color: {COLORS["bg_page"]};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Hide default Streamlit header bar for cleaner look */
    header[data-testid="stHeader"] {{
        background: linear-gradient(135deg, {COLORS["gradient_start"]} 0%, {COLORS["primary_light"]} 100%);
        height: 0px;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS["bg_sidebar"]} 0%, #0A1F33 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {{
        color: #CBD5E1 !important;
        font-size: 0.9rem;
    }}
    section[data-testid="stSidebar"] .stRadio label span {{
        color: #E2E8F0 !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.08);
    }}

    /* Main titles */
    .page-title {{
        font-size: 2rem;
        font-weight: 800;
        color: {COLORS["primary"]};
        margin-bottom: 2px;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }}
    .page-subtitle {{
        font-size: 1rem;
        color: {COLORS["text_muted"]};
        margin-bottom: 24px;
        font-weight: 400;
    }}

    /* Metric cards */
    .metric-row {{
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }}
    .metric-card {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 20px 24px;
        flex: 1;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s, transform 0.2s;
    }}
    .metric-card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }}
    .metric-card.primary::before {{ background: {COLORS["accent"]}; }}
    .metric-card.success::before {{ background: {COLORS["success"]}; }}
    .metric-card.warning::before {{ background: {COLORS["warning"]}; }}
    .metric-card.danger::before {{ background: {COLORS["danger"]}; }}
    .metric-card.purple::before {{ background: {COLORS["accent_alt"]}; }}
    .metric-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: {COLORS["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }}
    .metric-value {{
        font-size: 1.85rem;
        font-weight: 800;
        color: {COLORS["text"]};
        line-height: 1.1;
    }}
    .metric-delta {{
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 6px;
    }}
    .metric-delta.positive {{ color: {COLORS["success"]}; }}
    .metric-delta.negative {{ color: {COLORS["danger"]}; }}

    /* Section cards */
    .section-card {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .section-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {COLORS["primary"]};
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Streamlit metric overrides */
    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    div[data-testid="stMetric"] label {{
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: {COLORS["text"]} !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["accent_alt"]} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 12px 24px;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(0,180,216,0.25);
    }}
    .stButton > button:hover {{
        box-shadow: 0 4px 16px rgba(0,180,216,0.35);
        transform: translateY(-1px);
    }}

    /* Download buttons */
    .stDownloadButton > button {{
        background: white;
        color: {COLORS["primary"]};
        border: 2px solid {COLORS["border"]};
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }}
    .stDownloadButton > button:hover {{
        border-color: {COLORS["accent"]};
        color: {COLORS["accent"]};
        background: #F0FBFF;
    }}

    /* Dataframes */
    .stDataFrame {{
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 8px;
    }}

    /* Multiselect */
    .stMultiSelect > div {{
        border-radius: 10px;
    }}

    /* Selectbox */
    .stSelectbox > div > div {{
        border-radius: 10px;
    }}

    /* Info/Warning/Success boxes */
    .stAlert {{
        border-radius: 10px;
        border-left-width: 4px;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }}

    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: {COLORS["border"]};
        margin: 20px 0;
    }}

    /* Sidebar logo area */
    .sidebar-brand {{
        text-align: center;
        padding: 8px 0 16px 0;
    }}
    .sidebar-brand h2 {{
        color: white;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .sidebar-brand p {{
        color: {COLORS["accent"]};
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 4px 0 0 0;
    }}

    /* Nav items in sidebar */
    .nav-item {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: 8px;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 2px;
        transition: all 0.15s;
    }}
    .nav-item:hover {{
        background: rgba(255,255,255,0.06);
        color: white;
    }}
    .nav-item.active {{
        background: rgba(0,180,216,0.15);
        color: {COLORS["accent"]};
    }}

    /* Alert cards for Automated Alerts page */
    .alert-card {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid;
        transition: box-shadow 0.2s;
    }}
    .alert-card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }}
    .alert-card.critical {{ border-left-color: {COLORS["danger"]}; }}
    .alert-card.high {{ border-left-color: {COLORS["warning"]}; }}
    .alert-card.medium {{ border-left-color: {COLORS["accent"]}; }}
    .alert-account {{
        font-weight: 700;
        color: {COLORS["text"]};
        font-size: 0.95rem;
    }}
    .alert-detail {{
        color: {COLORS["text_muted"]};
        font-size: 0.85rem;
        margin-top: 4px;
    }}
    .alert-action {{
        color: {COLORS["primary"]};
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 6px;
    }}
    .priority-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .priority-badge.critical {{ background: #FEE2E8; color: {COLORS["danger"]}; }}
    .priority-badge.high {{ background: #FEF3C7; color: #D97706; }}
    .priority-badge.medium {{ background: #E0F2FE; color: #0284C7; }}

    /* EBR sections */
    .ebr-section {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }}
    .ebr-section-num {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["accent_alt"]} 100%);
        color: white;
        font-weight: 700;
        font-size: 0.8rem;
        margin-right: 10px;
    }}

    /* Risk tag */
    .risk-tag {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 8px;
        margin-right: 8px;
    }}
    .risk-tag.danger {{ background: #FEE2E8; color: {COLORS["danger_dark"]}; }}
    .risk-tag.warning {{ background: #FEF3C7; color: #92400E; }}
    .risk-tag.success {{ background: #D1FAE5; color: #065F46; }}

    /* Hide streamlit branding */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Scrollbar styling */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: #CBD5E1; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #94A3B8; }}
</style>
""", unsafe_allow_html=True)


# --- Helper functions ---
def render_metric_card(label, value, variant="primary", delta=None, delta_dir="positive"):
    delta_html = ""
    if delta:
        delta_html = f'<div class="metric-delta {delta_dir}">{delta}</div>'
    return f"""
    <div class="metric-card {variant}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def render_page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def render_section_title(icon, title):
    st.markdown(f'<div class="section-title">{icon} {title}</div>', unsafe_allow_html=True)

def apply_chart_style(fig, height=380):
    fig.update_layout(**CHART_TEMPLATE, height=height)
    return fig


# --- Data Loading ---
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df, None
    else:
        accounts = pd.read_csv("data/renewal_churn_data.csv")
        metrics = pd.read_csv("data/monthly_metrics.csv")
        return accounts, metrics


def load_default_data():
    accounts = pd.read_csv("data/renewal_churn_data.csv")
    metrics = pd.read_csv("data/monthly_metrics.csv")
    return accounts, metrics


# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>CS Ops Intelligence</h2>
        <p>Operations Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    data_source = st.radio("Data Source", ["Sample Data", "Upload Your Own"], index=0, label_visibility="collapsed")

    uploaded_file = None
    if data_source == "Upload Your Own":
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
        if uploaded_file:
            st.success(f"Loaded: {uploaded_file.name}")

    st.markdown("---")

    NAV_ICONS = {
        "Executive Summary": "&#9632;",
        "Renewal Forecast": "&#9654;",
        "Churn Analysis": "&#9660;",
        "Account Health": "&#9829;",
        "EBR Preparation": "&#9733;",
        "PS & Training": "&#9881;",
        "Automated Alerts": "&#9888;",
    }

    page = st.radio(
        "Navigate",
        list(NAV_ICONS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(f"""
    <div style="text-align:center; padding: 8px 0;">
        <div style="color: #475569; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">
            Built with Claude Code
        </div>
        <div style="color: #64748B; font-size: 0.65rem; margin-top: 2px;">
            CS Ops Demo &middot; v1.0
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Load Data ---
if data_source == "Upload Your Own" and uploaded_file:
    accounts, metrics = load_data(uploaded_file)
    if metrics is None:
        metrics = pd.read_csv("data/monthly_metrics.csv")
else:
    accounts, metrics = load_default_data()

for col in ["Renewal_Date", "Contract_Start", "Churn_Date"]:
    if col in accounts.columns:
        accounts[col] = pd.to_datetime(accounts[col], errors="coerce")

if "Month" in metrics.columns:
    metrics["Month"] = pd.to_datetime(metrics["Month"])


# =====================================================================
# PAGE: Executive Summary
# =====================================================================
if page == "Executive Summary":
    render_page_header("Executive Summary", "Real-time overview of Customer Success Operations KPIs")

    total_arr = accounts["ARR"].sum()
    total_accounts = len(accounts)
    churned = accounts[accounts["Status"] == "Churned"]
    churn_rate = len(churned) / total_accounts * 100
    churned_arr = churned["ARR"].sum()
    active_accounts = accounts[accounts["Status"] != "Churned"]
    at_risk = accounts[accounts["Health_Score"].isin(["At Risk", "Critical"])]

    st.markdown(f"""
    <div class="metric-row">
        {render_metric_card("Total ARR", f"${total_arr/1e6:.1f}M", "primary")}
        {render_metric_card("Active Accounts", f"{len(active_accounts)}", "success")}
        {render_metric_card("Churn Rate", f"{churn_rate:.1f}%", "danger", f"Target: <10%")}
        {render_metric_card("Churned ARR", f"${churned_arr/1e3:.0f}K", "warning")}
        {render_metric_card("At-Risk Accounts", f"{len(at_risk)}", "purple")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128200;", "ARR Trend & Net Revenue Retention")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=metrics["Month"], y=metrics["Total_ARR"], name="Total ARR",
                       fill="tozeroy", fillcolor="rgba(0,180,216,0.08)",
                       line=dict(color=COLORS["accent"], width=2.5)),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=metrics["Month"], y=metrics["NRR_Pct"], name="NRR %",
                       line=dict(color=COLORS["accent_alt"], dash="dot", width=2)),
            secondary_y=True,
        )
        fig = apply_chart_style(fig, 370)
        fig.update_yaxes(title_text="ARR ($)", secondary_y=False, gridcolor="#F1F5F9")
        fig.update_yaxes(title_text="NRR %", secondary_y=True, gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128202;", "ARR Movement (Waterfall)")
        latest = metrics.iloc[-1]
        waterfall_data = {
            "Category": ["Starting ARR", "Expansion", "New Logo", "Contraction", "Churn", "Ending ARR"],
            "Amount": [
                metrics.iloc[-2]["Total_ARR"] if len(metrics) > 1 else latest["Total_ARR"],
                latest["Expansion_ARR"],
                latest["New_Logo_ARR"],
                -latest["Contraction_ARR"],
                -latest["Churned_ARR"],
                latest["Total_ARR"],
            ],
            "Type": ["total", "relative", "relative", "relative", "relative", "total"],
        }
        fig = go.Figure(go.Waterfall(
            x=waterfall_data["Category"],
            y=waterfall_data["Amount"],
            measure=waterfall_data["Type"],
            connector={"line": {"color": "#CBD5E1", "width": 1}},
            increasing={"marker": {"color": COLORS["success"]}},
            decreasing={"marker": {"color": COLORS["danger"]}},
            totals={"marker": {"color": COLORS["accent"]}},
        ))
        fig = apply_chart_style(fig, 370)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128308;", "Account Health Distribution")
        health_counts = accounts["Health_Score"].value_counts()
        health_colors = {"Healthy": COLORS["success"], "Needs Attention": COLORS["warning"],
                         "At Risk": "#FB923C", "Critical": COLORS["danger"]}
        fig = px.pie(
            names=health_counts.index,
            values=health_counts.values,
            color=health_counts.index,
            color_discrete_map=health_colors,
            hole=0.55,
        )
        fig.update_traces(textinfo="percent+label", textfont_size=12,
                          marker=dict(line=dict(color="white", width=2)))
        fig = apply_chart_style(fig, 370)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128337;", "Renewal Rate Trend")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=metrics["Month"], y=metrics["Gross_Renewal_Rate"],
            name="Gross Renewal Rate %",
            marker=dict(color=COLORS["accent"], cornerradius=4),
        ))
        fig.add_hline(y=90, line_dash="dash", line_color=COLORS["danger"],
                      annotation_text="Target: 90%", annotation_font_color=COLORS["danger"])
        fig = apply_chart_style(fig, 370)
        fig.update_layout(yaxis_range=[70, 100])
        st.plotly_chart(fig, use_container_width=True)


# =====================================================================
# PAGE: Renewal Forecast
# =====================================================================
elif page == "Renewal Forecast":
    render_page_header("Renewal Forecast & Pipeline", "Forecast renewal outcomes by quarter, segment, and category")

    col1, col2, col3 = st.columns(3)
    with col1:
        segment_filter = st.multiselect("Segment", accounts["Segment"].unique(), default=accounts["Segment"].unique())
    with col2:
        region_filter = st.multiselect("Region", accounts["Region"].unique(), default=accounts["Region"].unique())
    with col3:
        csm_filter = st.multiselect("CSM", accounts["CSM"].unique(), default=accounts["CSM"].unique())

    filtered = accounts[
        (accounts["Segment"].isin(segment_filter)) &
        (accounts["Region"].isin(region_filter)) &
        (accounts["CSM"].isin(csm_filter))
    ]

    today = pd.Timestamp("2026-03-06")
    upcoming = filtered[
        (filtered["Renewal_Date"] >= today) &
        (filtered["Renewal_Date"] <= today + timedelta(days=180)) &
        (filtered["Status"] == "Active")
    ].copy()

    commit = upcoming[upcoming["Forecast_Category"] == "Commit"]["ARR"].sum()
    at_risk_arr = upcoming[upcoming["Forecast_Category"] == "At Risk"]["ARR"].sum()

    st.markdown(f"""
    <div class="metric-row">
        {render_metric_card("Renewals Due (6mo)", f"{len(upcoming)}", "primary")}
        {render_metric_card("ARR at Renewal", f"${upcoming['ARR'].sum()/1e6:.2f}M", "success")}
        {render_metric_card("Commit", f"${commit/1e6:.2f}M", "success")}
        {render_metric_card("At Risk ARR", f"${at_risk_arr/1e6:.2f}M", "danger")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    cat_colors = {"Commit": COLORS["success"], "Best Case": COLORS["accent"],
                  "Pipeline": COLORS["warning"], "At Risk": COLORS["danger"]}

    with col1:
        render_section_title("&#128202;", "Renewal Forecast by Category")
        forecast_summary = upcoming.groupby("Forecast_Category")["ARR"].agg(["sum", "count"]).reset_index()
        forecast_summary.columns = ["Category", "ARR", "Count"]
        fig = px.bar(
            forecast_summary, x="Category", y="ARR", color="Category",
            color_discrete_map=cat_colors, text="Count",
        )
        fig.update_traces(texttemplate="%{text} accounts", textposition="outside",
                          marker=dict(cornerradius=6))
        fig = apply_chart_style(fig, 400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128197;", "Renewal Timeline (Monthly)")
        upcoming["Renewal_Month"] = upcoming["Renewal_Date"].dt.to_period("M").astype(str)
        monthly_renewals = upcoming.groupby(["Renewal_Month", "Forecast_Category"])["ARR"].sum().reset_index()
        fig = px.bar(
            monthly_renewals, x="Renewal_Month", y="ARR", color="Forecast_Category",
            color_discrete_map=cat_colors, barmode="stack",
        )
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        render_section_title("&#128201;", "Forecast by Segment")
        seg_forecast = upcoming.groupby("Segment")["ARR"].sum().reset_index()
        fig = px.bar(seg_forecast, x="Segment", y="ARR", color="Segment",
                     color_discrete_sequence=[COLORS["accent"], COLORS["accent_alt"], COLORS["success"]])
        fig.update_traces(marker=dict(cornerradius=6))
        fig = apply_chart_style(fig, 360)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#127758;", "Forecast by Region")
        reg_forecast = upcoming.groupby("Region")["ARR"].sum().reset_index()
        fig = px.bar(reg_forecast, x="Region", y="ARR", color="Region",
                     color_discrete_sequence=[COLORS["accent"], "#818CF8", "#F472B6", COLORS["success"]])
        fig.update_traces(marker=dict(cornerradius=6))
        fig = apply_chart_style(fig, 360)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    render_section_title("&#128203;", "Upcoming Renewal Details")
    display_cols = ["Account_ID", "Account_Name", "Segment", "Region", "CSM", "ARR",
                    "Renewal_Date", "Health_Score", "Forecast_Category", "Churn_Probability", "NPS_Score"]
    display_cols = [c for c in display_cols if c in upcoming.columns]
    st.dataframe(upcoming[display_cols].sort_values("Renewal_Date"), use_container_width=True, height=400)

    csv = upcoming[display_cols].to_csv(index=False)
    st.download_button("Download Renewal Forecast CSV", csv, "renewal_forecast.csv", "text/csv")


# =====================================================================
# PAGE: Churn Analysis
# =====================================================================
elif page == "Churn Analysis":
    render_page_header("Churn Analysis & Risk Intelligence", "Deep dive into churn patterns, root causes, and predictive signals")

    churned = accounts[accounts["Status"] == "Churned"].copy()
    active = accounts[accounts["Status"] != "Churned"]
    logo_churn = len(churned) / len(accounts) * 100

    st.markdown(f"""
    <div class="metric-row">
        {render_metric_card("Total Churned", f"{len(churned)}", "danger")}
        {render_metric_card("Churned ARR", f"${churned['ARR'].sum()/1e3:.0f}K", "danger")}
        {render_metric_card("Avg Churned ARR", f"${churned['ARR'].mean()/1e3:.0f}K", "warning")}
        {render_metric_card("Logo Churn Rate", f"{logo_churn:.1f}%", "purple")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128269;", "Churn Reasons (by ARR)")
        reason_arr = churned.groupby("Churn_Reason")["ARR"].sum().sort_values(ascending=True).reset_index()
        fig = px.bar(reason_arr, x="ARR", y="Churn_Reason", orientation="h",
                     color="ARR", color_continuous_scale=[[0, "#FCA5A5"], [1, COLORS["danger"]]])
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 400)
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128200;", "Churn by Segment")
        churn_seg = churned.groupby("Segment").agg(
            Accounts=("Account_ID", "count"),
            ARR=("ARR", "sum")
        ).reset_index()
        fig = px.bar(churn_seg, x="Segment", y=["Accounts", "ARR"], barmode="group",
                     color_discrete_sequence=[COLORS["danger"], COLORS["danger_dark"]])
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128161;", "Risk Signals vs Churn Probability")
        scatter_data = accounts[accounts["Status"] != "Churned"].copy()
        health_colors_map = {"Healthy": COLORS["success"], "Needs Attention": COLORS["warning"],
                             "At Risk": "#FB923C", "Critical": COLORS["danger"]}
        fig = px.scatter(
            scatter_data, x="License_Utilization_Pct", y="Churn_Probability",
            color="Health_Score", size="ARR",
            color_discrete_map=health_colors_map,
            hover_data=["Account_Name", "Segment"],
        )
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128202;", "Churn Probability Distribution")
        status_colors = {"Active": COLORS["accent"], "Churned": COLORS["danger"], "Renewed": COLORS["success"]}
        fig = px.histogram(
            accounts, x="Churn_Probability", color="Status",
            nbins=30, barmode="overlay",
            color_discrete_map=status_colors,
        )
        fig.update_traces(opacity=0.75)
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    render_section_title("&#128200;", "Monthly Churn Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=metrics["Month"], y=metrics["Churned_ARR"],
        fill="tozeroy", fillcolor="rgba(239,71,111,0.1)",
        name="Churned ARR", line=dict(color=COLORS["danger"], width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=metrics["Month"], y=metrics["Churned_Accounts"] * 10000,
        name="Churned Accounts (scaled)", line=dict(color=COLORS["danger_dark"], dash="dot", width=2),
    ))
    fig = apply_chart_style(fig, 320)
    st.plotly_chart(fig, use_container_width=True)

    render_section_title("&#9888;", "Current High-Risk Accounts (Action Required)")
    high_risk = active[active["Churn_Probability"] >= 0.30].sort_values("ARR", ascending=False)
    if len(high_risk) > 0:
        display_cols = ["Account_ID", "Account_Name", "Segment", "CSM", "ARR",
                        "Health_Score", "Churn_Probability", "License_Utilization_Pct",
                        "Support_Tickets_Open", "Escalations_Last_90d", "Last_Login_Days_Ago"]
        display_cols = [c for c in display_cols if c in high_risk.columns]
        st.dataframe(high_risk[display_cols], use_container_width=True, height=300)
    else:
        st.success("No high-risk accounts detected!")


# =====================================================================
# PAGE: Account Health
# =====================================================================
elif page == "Account Health":
    render_page_header("Account Health Overview", "Monitor health scores, engagement metrics, and adoption trends")

    active = accounts[accounts["Status"] != "Churned"].copy()
    healthy_pct = len(active[active["Health_Score"] == "Healthy"]) / len(active) * 100
    avg_util = active["License_Utilization_Pct"].mean()
    avg_nps = active["NPS_Score"].mean()
    open_tickets = active["Support_Tickets_Open"].sum()

    st.markdown(f"""
    <div class="metric-row">
        {render_metric_card("Healthy Accounts", f"{healthy_pct:.0f}%", "success")}
        {render_metric_card("Avg Utilization", f"{avg_util:.0f}%", "primary")}
        {render_metric_card("Avg NPS", f"{avg_nps:.1f}/10", "purple")}
        {render_metric_card("Open Tickets", f"{open_tickets}", "warning")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128202;", "Health by Segment (ARR weighted)")
        health_seg = active.groupby(["Segment", "Health_Score"])["ARR"].sum().reset_index()
        health_colors_map = {"Healthy": COLORS["success"], "Needs Attention": COLORS["warning"],
                             "At Risk": "#FB923C", "Critical": COLORS["danger"]}
        fig = px.bar(health_seg, x="Segment", y="ARR", color="Health_Score",
                     color_discrete_map=health_colors_map, barmode="stack")
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128161;", "Utilization vs NPS by Segment")
        fig = px.scatter(
            active, x="License_Utilization_Pct", y="NPS_Score",
            color="Segment", size="ARR",
            color_discrete_sequence=[COLORS["accent"], COLORS["accent_alt"], COLORS["success"]],
            hover_data=["Account_Name", "Health_Score"],
        )
        fig = apply_chart_style(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    render_section_title("&#128101;", "CSM Portfolio Health")
    csm_health = active.groupby("CSM").agg(
        Total_Accounts=("Account_ID", "count"),
        Total_ARR=("ARR", "sum"),
        Avg_Health=("NPS_Score", "mean"),
        At_Risk=("Health_Score", lambda x: (x.isin(["At Risk", "Critical"])).sum()),
        Avg_Utilization=("License_Utilization_Pct", "mean"),
    ).reset_index()
    csm_health["At_Risk_Pct"] = (csm_health["At_Risk"] / csm_health["Total_Accounts"] * 100).round(1)
    csm_health = csm_health.sort_values("Total_ARR", ascending=False)
    st.dataframe(csm_health, use_container_width=True, hide_index=True)

    render_section_title("&#128200;", "Average Health Score Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=metrics["Month"], y=metrics["Avg_Health_Score"],
        fill="tozeroy", fillcolor="rgba(0,180,216,0.08)",
        line=dict(color=COLORS["accent"], width=2.5),
    ))
    fig.add_hline(y=75, line_dash="dash", line_color=COLORS["warning"],
                  annotation_text="Target: 75", annotation_font_color=COLORS["warning"])
    fig = apply_chart_style(fig, 300)
    st.plotly_chart(fig, use_container_width=True)


# =====================================================================
# PAGE: EBR Preparation
# =====================================================================
elif page == "EBR Preparation":
    render_page_header("Executive Business Review", "AI-assisted workflow to prepare comprehensive EBR materials")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,180,216,0.08) 0%, rgba(123,97,255,0.08) 100%);
                border: 1px solid rgba(0,180,216,0.2); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <div style="font-weight: 600; color: {COLORS['primary']}; margin-bottom: 4px;">
            Automated EBR Preparation
        </div>
        <div style="color: {COLORS['text_muted']}; font-size: 0.9rem;">
            Select an account below to auto-generate a complete EBR brief with risk assessment,
            expansion opportunities, and executive talking points.
        </div>
    </div>
    """, unsafe_allow_html=True)

    active_accounts = accounts[accounts["Status"] != "Churned"].sort_values("ARR", ascending=False)
    account_options = [f"{row['Account_Name']} ({row['Segment']}) - ${row['ARR']:,.0f} ARR"
                       for _, row in active_accounts.iterrows()]

    selected_idx = st.selectbox("Select Account for EBR", range(len(account_options)),
                                format_func=lambda x: account_options[x])

    acct = active_accounts.iloc[selected_idx]

    if st.button("Generate EBR Brief", type="primary", use_container_width=True):
        with st.spinner("Generating EBR materials..."):
            progress = st.progress(0)
            steps = [
                "Pulling account data from CRM...",
                "Analyzing usage patterns...",
                "Reviewing support history...",
                "Calculating ROI metrics...",
                "Generating executive summary...",
                "Preparing recommendations...",
            ]
            import time
            for i, step in enumerate(steps):
                st.text(step)
                time.sleep(0.3)
                progress.progress((i + 1) / len(steps))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['success']}15 0%, {COLORS['success']}05 100%);
                    border: 1px solid {COLORS['success']}40; border-radius: 12px; padding: 16px; margin: 16px 0;">
            <span style="color: {COLORS['success']}; font-weight: 700;">EBR Brief Generated Successfully</span>
        </div>
        """, unsafe_allow_html=True)

        # --- EBR Document ---
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
                    border-radius: 16px; padding: 32px; margin: 16px 0; color: white;">
            <div style="font-size: 1.6rem; font-weight: 800; margin-bottom: 4px;">
                EBR Brief: {acct['Account_Name']}
            </div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                Prepared: {datetime.now().strftime('%B %d, %Y')} &middot; CSM: {acct['CSM']} &middot; TAE: {acct['TAE']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Section 1: Account Overview
        st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; margin: 20px 0 12px 0;">
            <span class="ebr-section-num">1</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}">Account Overview</span>
        </div>""", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current ARR", f"${acct['ARR']:,.0f}")
        with col2:
            st.metric("Segment", acct["Segment"])
        with col3:
            st.metric("Health Score", acct["Health_Score"])
        with col4:
            st.metric("NPS Score", f"{acct['NPS_Score']}/10")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Industry", acct["Industry"])
        with col2:
            st.metric("Region", acct["Region"])
        with col3:
            st.metric("Contract Term", f"{acct['Contract_Term_Months']}mo")
        with col4:
            st.metric("Product", acct["Product"])

        # Section 2: Engagement
        st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; margin: 28px 0 12px 0;">
            <span class="ebr-section-num">2</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}">Engagement & Adoption Metrics</span>
        </div>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=acct["License_Utilization_Pct"],
                title={"text": "License Utilization", "font": {"size": 14, "color": COLORS["text_muted"]}},
                number={"suffix": "%", "font": {"size": 36, "color": COLORS["text"]}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "white"},
                    "bar": {"color": COLORS["accent"], "thickness": 0.7},
                    "bgcolor": "#F1F5F9",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "rgba(239,71,111,0.15)"},
                        {"range": [40, 70], "color": "rgba(255,183,3,0.15)"},
                        {"range": [70, 100], "color": "rgba(6,214,160,0.15)"},
                    ],
                },
            ))
            fig.update_layout(height=220, margin=dict(l=20, r=20, t=50, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"""
            <div class="ebr-section">
                <div style="font-weight:700; color:{COLORS['primary']}; margin-bottom:12px;">Support Activity</div>
                <div style="display:grid; gap:8px;">
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Open Tickets</span>
                        <span style="font-weight:700">{acct['Support_Tickets_Open']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Escalations (90d)</span>
                        <span style="font-weight:700">{acct['Escalations_Last_90d']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Last Login</span>
                        <span style="font-weight:700">{acct['Last_Login_Days_Ago']} days ago</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Training</span>
                        <span style="font-weight:700; color:{'#06D6A0' if acct['Training_Completed'] else '#EF476F'}">{'Completed' if acct['Training_Completed'] else 'Pending'}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0;">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Exec Sponsor</span>
                        <span style="font-weight:700; color:{'#06D6A0' if acct['Executive_Sponsor'] else '#EF476F'}">{'Yes' if acct['Executive_Sponsor'] else 'No'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            renewal_dt = acct["Renewal_Date"]
            days_to_renewal = (renewal_dt - pd.Timestamp("2026-03-06")).days
            st.markdown(f"""
            <div class="ebr-section">
                <div style="font-weight:700; color:{COLORS['primary']}; margin-bottom:12px;">Renewal Outlook</div>
                <div style="display:grid; gap:8px;">
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Renewal Date</span>
                        <span style="font-weight:700">{renewal_dt.strftime('%Y-%m-%d')}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Days to Renewal</span>
                        <span style="font-weight:700">{days_to_renewal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Forecast</span>
                        <span style="font-weight:700">{acct['Forecast_Category']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid {COLORS['border']}">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Churn Probability</span>
                        <span style="font-weight:700; color:{'#EF476F' if acct['Churn_Probability'] > 0.3 else '#06D6A0'}">{acct['Churn_Probability']*100:.0f}%</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; padding:6px 0;">
                        <span style="color:{COLORS['text_muted']}; font-size:0.85rem">Multi-Year</span>
                        <span style="font-weight:700">{'Yes' if acct['Multi_Year'] else 'No'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Section 3: Risk Assessment
        st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; margin: 28px 0 12px 0;">
            <span class="ebr-section-num">3</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}">Risk Assessment & Action Items</span>
        </div>""", unsafe_allow_html=True)

        risks = []
        actions = []

        if acct["License_Utilization_Pct"] < 50:
            risks.append(f"Low license utilization ({acct['License_Utilization_Pct']:.0f}%) - risk of downsell or churn")
            actions.append("Schedule product adoption workshop with key users")
            actions.append("Identify unused features and create enablement plan")
        if acct["Last_Login_Days_Ago"] > 14:
            risks.append(f"Low engagement - last login {acct['Last_Login_Days_Ago']} days ago")
            actions.append("Reach out to primary contact to re-engage")
        if acct["Support_Tickets_Open"] > 3:
            risks.append(f"High support volume ({acct['Support_Tickets_Open']} open tickets)")
            actions.append("Coordinate with Support team to prioritize resolution")
        if acct["Escalations_Last_90d"] > 0:
            risks.append(f"{acct['Escalations_Last_90d']} escalation(s) in last 90 days")
            actions.append("Review escalation root causes and present resolution timeline")
        if not acct["Executive_Sponsor"]:
            risks.append("No executive sponsor identified")
            actions.append("Work with champion to identify and engage executive sponsor")
        if not acct["Training_Completed"]:
            risks.append("Training not completed")
            actions.append("Schedule training session and provide self-service resources")
        if acct["Churn_Probability"] > 0.3:
            risks.append(f"Elevated churn probability ({acct['Churn_Probability']*100:.0f}%)")
            actions.append("Develop retention plan with specific value demonstrations")
        if days_to_renewal < 90 and days_to_renewal > 0:
            risks.append(f"Renewal approaching in {days_to_renewal} days")
            actions.append("Initiate renewal conversation and prepare commercial proposal")

        if risks:
            risk_html = ""
            for r in risks:
                risk_html += f'<span class="risk-tag danger">{r}</span>'
            st.markdown(f'<div style="margin-bottom:16px;">{risk_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-tag success" style="display:inline-flex;">
                Account is in good standing - no significant risks identified
            </div>
            """, unsafe_allow_html=True)

        if actions:
            st.markdown(f"<div style='font-weight:700; color:{COLORS['primary']}; margin: 12px 0 8px 0;'>Recommended Actions</div>", unsafe_allow_html=True)
            for i, a in enumerate(actions, 1):
                st.markdown(f"""<div style="display:flex; gap:10px; padding:8px 0; border-bottom:1px solid {COLORS['border']};">
                    <span style="color:{COLORS['accent']}; font-weight:700; min-width:20px;">{i}.</span>
                    <span style="color:{COLORS['text']};">{a}</span>
                </div>""", unsafe_allow_html=True)

        # Section 4: Expansion
        st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; margin: 28px 0 12px 0;">
            <span class="ebr-section-num">4</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}">Expansion Opportunities</span>
        </div>""", unsafe_allow_html=True)

        opps = []
        if acct["License_Utilization_Pct"] > 80:
            opps.append("High utilization suggests need for additional capacity/licenses")
        if acct["Product"] != "Cloud SIEM":
            opps.append("Cross-sell opportunity: Cloud SIEM for security operations")
        if acct["Product"] != "Cloud SOAR":
            opps.append("Cross-sell opportunity: Cloud SOAR for security automation")
        if not acct["Multi_Year"]:
            opps.append("Convert to multi-year agreement for better pricing and commitment")
        if acct["PS_Hours_Purchased"] == 0:
            opps.append("Professional Services engagement for deeper implementation")
        elif acct["PS_Hours_Used"] >= acct["PS_Hours_Purchased"] * 0.8:
            opps.append("PS hours nearly depleted - upsell additional PS hours")

        for o in opps:
            st.markdown(f"""<div style="display:flex; gap:10px; padding:8px 12px; margin-bottom:6px;
                        background:rgba(0,180,216,0.06); border-radius:8px; border-left:3px solid {COLORS['accent']};">
                <span style="color:{COLORS['text']}; font-size:0.9rem;">{o}</span>
            </div>""", unsafe_allow_html=True)

        # Section 5: Talking Points
        st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; margin: 28px 0 12px 0;">
            <span class="ebr-section-num">5</span>
            <span style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}">Executive Talking Points</span>
        </div>""", unsafe_allow_html=True)

        talking_points = [
            ("Opening", f"Thank the customer for their partnership. Reference their tenure and growth with {acct['Product']}."),
            ("Value Delivered", f"Deployed across their {acct['Industry']} operations in {acct['Region']}. "
                               f"License utilization at {acct['License_Utilization_Pct']:.0f}% "
                               f"{'(strong adoption)' if acct['License_Utilization_Pct'] > 60 else '(opportunity to improve)'}. "
                               f"{'Training completed - team is well-enabled.' if acct['Training_Completed'] else 'Training opportunity to accelerate value.'}"),
            ("Strategic Alignment", f"Discuss upcoming roadmap features relevant to {acct['Industry']}. "
                                    f"Explore how AI/ML capabilities can enhance their security operations. "
                                    f"Review integration opportunities with their existing toolchain."),
            ("The Ask", f"{'Discuss renewal terms and potential multi-year agreement.' if not acct['Multi_Year'] else 'Confirm multi-year renewal satisfaction.'} "
                        f"{'Identify executive sponsor for stronger partnership.' if not acct['Executive_Sponsor'] else 'Maintain executive sponsorship engagement.'} "
                        f"Expand into additional use cases."),
        ]

        for title, content in talking_points:
            st.markdown(f"""
            <div style="background:white; border:1px solid {COLORS['border']}; border-radius:10px;
                        padding:16px; margin-bottom:10px;">
                <div style="font-weight:700; color:{COLORS['accent_alt']}; font-size:0.8rem;
                            text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">{title}</div>
                <div style="color:{COLORS['text']}; font-size:0.9rem; line-height:1.5;">{content}</div>
            </div>
            """, unsafe_allow_html=True)

        # Export
        ebr_text = f"""
EXECUTIVE BUSINESS REVIEW - {acct['Account_Name']}
{'='*60}
Date: {datetime.now().strftime('%B %d, %Y')}
CSM: {acct['CSM']} | TAE: {acct['TAE']}

ACCOUNT OVERVIEW
- ARR: ${acct['ARR']:,.0f}
- Segment: {acct['Segment']} | Industry: {acct['Industry']} | Region: {acct['Region']}
- Product: {acct['Product']}
- Health: {acct['Health_Score']} | NPS: {acct['NPS_Score']}/10

ENGAGEMENT
- License Utilization: {acct['License_Utilization_Pct']:.0f}%
- Last Login: {acct['Last_Login_Days_Ago']} days ago
- Open Support Tickets: {acct['Support_Tickets_Open']}
- Escalations (90d): {acct['Escalations_Last_90d']}

RENEWAL
- Date: {renewal_dt.strftime('%Y-%m-%d')} ({days_to_renewal} days)
- Forecast: {acct['Forecast_Category']}
- Churn Probability: {acct['Churn_Probability']*100:.0f}%

RISKS
{chr(10).join(f'- {r}' for r in risks) if risks else '- No significant risks'}

ACTIONS
{chr(10).join(f'{i+1}. {a}' for i, a in enumerate(actions)) if actions else '- Maintain current engagement cadence'}

EXPANSION OPPORTUNITIES
{chr(10).join(f'- {o}' for o in opps)}
"""
        st.download_button("Download EBR Brief (TXT)", ebr_text, f"EBR_{acct['Account_Name']}.txt")


# =====================================================================
# PAGE: PS & Training
# =====================================================================
elif page == "PS & Training":
    render_page_header("Professional Services & Training", "Track PS utilization, project delivery, and training adoption")

    active = accounts[accounts["Status"] != "Churned"]
    ps_accounts = active[active["PS_Hours_Purchased"] > 0].copy()

    total_purchased = ps_accounts["PS_Hours_Purchased"].sum()
    total_used = ps_accounts["PS_Hours_Used"].sum()
    util_pct = total_used / total_purchased * 100 if total_purchased > 0 else 0

    st.markdown(f"""
    <div class="metric-row">
        {render_metric_card("PS Accounts", f"{len(ps_accounts)}", "primary")}
        {render_metric_card("Hours Purchased", f"{total_purchased}", "purple")}
        {render_metric_card("Hours Used", f"{total_used}", "success")}
        {render_metric_card("PS Utilization", f"{util_pct:.0f}%", "warning")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#128202;", "PS Utilization by Account")
        ps_accounts["Utilization_Pct"] = (ps_accounts["PS_Hours_Used"] / ps_accounts["PS_Hours_Purchased"] * 100).round(1)
        ps_sorted = ps_accounts.sort_values("Utilization_Pct", ascending=True).tail(20)
        fig = px.bar(ps_sorted, y="Account_Name", x="Utilization_Pct", orientation="h",
                     color="Utilization_Pct",
                     color_continuous_scale=[[0, COLORS["danger"]], [0.5, COLORS["warning"]], [1, COLORS["success"]]])
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 500)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128176;", "PS Revenue Trend")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=metrics["Month"], y=metrics["PS_Revenue"],
                             marker=dict(color=COLORS["accent"], cornerradius=4)))
        fig.add_trace(go.Scatter(x=metrics["Month"], y=metrics["PS_Utilization_Pct"] * 1000,
                                 name="Utilization % (scaled)",
                                 line=dict(color=COLORS["accent_alt"], dash="dot", width=2)))
        fig = apply_chart_style(fig, 500)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        render_section_title("&#127891;", "Training Adoption")
        training_data = active["Training_Completed"].value_counts()
        fig = px.pie(names=["Completed", "Not Completed"],
                     values=[training_data.get(True, 0), training_data.get(False, 0)],
                     color_discrete_sequence=[COLORS["success"], COLORS["danger"]], hole=0.55)
        fig.update_traces(textinfo="percent+label", textfont_size=12,
                          marker=dict(line=dict(color="white", width=2)))
        fig = apply_chart_style(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_section_title("&#128200;", "Training Impact on Health")
        trained = active[active["Training_Completed"] == True]
        untrained = active[active["Training_Completed"] == False]
        comparison = pd.DataFrame({
            "Metric": ["Avg NPS", "Avg Utilization %", "Avg Churn Prob %", "Avg Open Tickets"],
            "Trained": [trained["NPS_Score"].mean(), trained["License_Utilization_Pct"].mean(),
                        trained["Churn_Probability"].mean() * 100, trained["Support_Tickets_Open"].mean()],
            "Untrained": [untrained["NPS_Score"].mean(), untrained["License_Utilization_Pct"].mean(),
                          untrained["Churn_Probability"].mean() * 100, untrained["Support_Tickets_Open"].mean()],
        }).round(1)
        st.dataframe(comparison, use_container_width=True, hide_index=True)


# =====================================================================
# PAGE: Automated Alerts
# =====================================================================
elif page == "Automated Alerts":
    render_page_header("Automated Alerts", "Proactive monitoring with automated alert rules and recommendations")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(239,71,111,0.06) 0%, rgba(255,183,3,0.06) 100%);
                border: 1px solid rgba(239,71,111,0.15); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <div style="font-weight: 600; color: {COLORS['primary']}; margin-bottom: 4px;">
            Operational Intelligence Engine
        </div>
        <div style="color: {COLORS['text_muted']}; font-size: 0.9rem;">
            Automated identification of accounts requiring attention, replacing manual weekly review processes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    active = accounts[accounts["Status"] != "Churned"].copy()
    today = pd.Timestamp("2026-03-06")

    alerts = []

    upcoming_renewals = active[
        (active["Renewal_Date"] <= today + timedelta(days=60)) &
        (active["Renewal_Date"] >= today) &
        (active["Churn_Probability"] >= 0.20)
    ]
    for _, row in upcoming_renewals.iterrows():
        alerts.append({
            "Priority": "CRITICAL",
            "Account": row["Account_Name"],
            "Alert": f"Renewal in {(row['Renewal_Date'] - today).days} days with {row['Churn_Probability']*100:.0f}% churn probability",
            "ARR": row["ARR"],
            "CSM": row["CSM"],
            "Action": "Immediate executive engagement required",
        })

    critical_accounts = active[active["Health_Score"] == "Critical"]
    for _, row in critical_accounts.iterrows():
        alerts.append({
            "Priority": "HIGH",
            "Account": row["Account_Name"],
            "Alert": f"Critical health score - Utilization {row['License_Utilization_Pct']:.0f}%, {row['Support_Tickets_Open']} open tickets",
            "ARR": row["ARR"],
            "CSM": row["CSM"],
            "Action": "Schedule health check call within 48 hours",
        })

    low_engagement = active[active["Last_Login_Days_Ago"] > 30]
    for _, row in low_engagement.iterrows():
        alerts.append({
            "Priority": "MEDIUM",
            "Account": row["Account_Name"],
            "Alert": f"No login for {row['Last_Login_Days_Ago']} days",
            "ARR": row["ARR"],
            "CSM": row["CSM"],
            "Action": "Send re-engagement email and schedule check-in",
        })

    high_esc = active[active["Escalations_Last_90d"] >= 2]
    for _, row in high_esc.iterrows():
        alerts.append({
            "Priority": "HIGH",
            "Account": row["Account_Name"],
            "Alert": f"{row['Escalations_Last_90d']} escalations in last 90 days",
            "ARR": row["ARR"],
            "CSM": row["CSM"],
            "Action": "Root cause analysis and executive remediation plan",
        })

    alerts_df = pd.DataFrame(alerts)

    if len(alerts_df) > 0:
        critical = len(alerts_df[alerts_df["Priority"] == "CRITICAL"])
        high = len(alerts_df[alerts_df["Priority"] == "HIGH"])
        medium = len(alerts_df[alerts_df["Priority"] == "MEDIUM"])
        total_arr_risk = alerts_df["ARR"].sum()

        st.markdown(f"""
        <div class="metric-row">
            {render_metric_card("Critical Alerts", f"{critical}", "danger")}
            {render_metric_card("High Alerts", f"{high}", "warning")}
            {render_metric_card("Medium Alerts", f"{medium}", "primary")}
            {render_metric_card("ARR at Risk", f"${total_arr_risk/1e3:.0f}K", "purple")}
        </div>
        """, unsafe_allow_html=True)

        priority_filter = st.multiselect("Filter by Priority", ["CRITICAL", "HIGH", "MEDIUM"],
                                          default=["CRITICAL", "HIGH"])
        filtered_alerts = alerts_df[alerts_df["Priority"].isin(priority_filter)]

        render_section_title("&#128202;", "Alert Distribution by CSM")
        csm_alerts = filtered_alerts.groupby(["CSM", "Priority"]).size().reset_index(name="Count")
        fig = px.bar(csm_alerts, x="CSM", y="Count", color="Priority",
                     color_discrete_map={"CRITICAL": COLORS["danger"], "HIGH": COLORS["warning"], "MEDIUM": COLORS["accent"]},
                     barmode="stack")
        fig.update_traces(marker=dict(cornerradius=4))
        fig = apply_chart_style(fig, 350)
        st.plotly_chart(fig, use_container_width=True)

        for priority in ["CRITICAL", "HIGH", "MEDIUM"]:
            p_alerts = filtered_alerts[filtered_alerts["Priority"] == priority]
            if len(p_alerts) > 0:
                priority_lower = priority.lower()
                with st.expander(f"{priority} Alerts ({len(p_alerts)})", expanded=(priority == "CRITICAL")):
                    for _, alert in p_alerts.sort_values("ARR", ascending=False).iterrows():
                        st.markdown(f"""
                        <div class="alert-card {priority_lower}">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="alert-account">{alert['Account']}</span>
                                <div>
                                    <span class="priority-badge {priority_lower}">{priority}</span>
                                    <span style="color:{COLORS['text_muted']}; font-size:0.85rem; margin-left:8px;">${alert['ARR']:,.0f} ARR</span>
                                </div>
                            </div>
                            <div class="alert-detail">CSM: {alert['CSM']} &middot; {alert['Alert']}</div>
                            <div class="alert-action">Action: {alert['Action']}</div>
                        </div>
                        """, unsafe_allow_html=True)

        csv = filtered_alerts.to_csv(index=False)
        st.download_button("Download Alerts CSV", csv, "cs_alerts.csv", "text/csv")

        st.markdown("---")
        render_section_title("&#128231;", "Weekly Digest Preview")
        st.markdown(f"""
        <div style="background:white; border:1px solid {COLORS['border']}; border-radius:12px; padding:24px;">
            <div style="font-size:1.1rem; font-weight:700; color:{COLORS['primary']}; margin-bottom:16px;">
                CS Operations Weekly Alert Digest
                <span style="color:{COLORS['text_muted']}; font-weight:400; font-size:0.85rem;">
                    &middot; Week of {datetime.now().strftime('%B %d, %Y')}
                </span>
            </div>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px;">
                <div style="text-align:center; padding:12px; background:{COLORS['danger']}10; border-radius:8px;">
                    <div style="font-size:1.5rem; font-weight:800; color:{COLORS['danger']}">{critical}</div>
                    <div style="font-size:0.75rem; color:{COLORS['text_muted']}; text-transform:uppercase;">Critical</div>
                </div>
                <div style="text-align:center; padding:12px; background:{COLORS['warning']}15; border-radius:8px;">
                    <div style="font-size:1.5rem; font-weight:800; color:#D97706">{high}</div>
                    <div style="font-size:0.75rem; color:{COLORS['text_muted']}; text-transform:uppercase;">High</div>
                </div>
                <div style="text-align:center; padding:12px; background:{COLORS['accent']}10; border-radius:8px;">
                    <div style="font-size:1.5rem; font-weight:800; color:{COLORS['accent']}">{medium}</div>
                    <div style="font-size:0.75rem; color:{COLORS['text_muted']}; text-transform:uppercase;">Medium</div>
                </div>
                <div style="text-align:center; padding:12px; background:{COLORS['accent_alt']}10; border-radius:8px;">
                    <div style="font-size:1.5rem; font-weight:800; color:{COLORS['accent_alt']}">${total_arr_risk/1e3:.0f}K</div>
                    <div style="font-size:0.75rem; color:{COLORS['text_muted']}; text-transform:uppercase;">ARR Impacted</div>
                </div>
            </div>
            <div style="font-weight:600; color:{COLORS['primary']}; margin-bottom:8px;">Top Priority Actions</div>
        """, unsafe_allow_html=True)

        for _, alert in filtered_alerts[filtered_alerts["Priority"] == "CRITICAL"].head(5).iterrows():
            st.markdown(f"""<div style="padding:8px 12px; margin-bottom:4px; border-left:3px solid {COLORS['danger']};
                        background:{COLORS['danger']}08; border-radius:0 6px 6px 0; font-size:0.9rem;">
                <strong>{alert['Account']}</strong> - {alert['Alert']} &rarr; <em>{alert['Action']}</em>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("No active alerts - all accounts are in good standing!")
