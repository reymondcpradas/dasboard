"""
Palay Production Dashboard - Agusan del Sur (2021-2025, forecast to 2030)
Source: Pradas & Penaflor, "Trends in Palay Production in Agusan del Sur
(2021-2025)", Agusan del Sur State University.

Run in Visual Studio / VS Code terminal:
    pip install -r requirements.txt
    streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------ page
st.set_page_config(
    page_title="Palay Dashboard | Agusan del Sur",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Palay (rice) palette on a slightly dark, easy-to-read background
BG, CARD, LINE = "#17231c", "#223329", "#37503f"          # deep paddy-green charcoal
TXT, MUTED, TITLE = "#f1ead2", "#bcc7ab", "#d7ecae"       # cream text, soft green titles
GREEN, DEEP, GOLD, BROWN, WATER, RED = "#7cc242", "#0f3a1a", "#f2b705", "#d2ae72", "#5bb4e0", "#ef6f4f"
STRAW = "#f3e3b0"
COLORWAY = [GREEN, GOLD, BROWN, WATER, RED, "#a5d66a", "#e3c9a0"]
PIE_COLORS = [GREEN, GOLD, WATER, BROWN, RED, "#a5d66a", "#f7d56a", "#8fd0ee", "#e3c9a0",
              "#f39a80", "#5aa02c", "#c99a05", "#3d8fb8", "#b08a4e"]
RICE_SCALE = [[0, "#2a4a30"], [0.4, "#6f9a2e"], [0.75, "#e0ac0c"], [1, "#fbe58f"]]
DIV_SCALE = [[0, "#e0583a"], [0.5, "#f3e3b0"], [1, "#5fbf3a"]]

# inline SVG rice panicle used as banner pattern
PANICLE = (
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='110' viewBox='0 0 140 110'>"
    "<path d='M20 110 C22 70 40 40 85 12' fill='none' stroke='white' stroke-opacity='.25' stroke-width='2.5'/>"
    "<g fill='white' fill-opacity='.30'>"
    "<ellipse cx='30' cy='62' rx='3.5' ry='8' transform='rotate(-25 30 62)'/>"
    "<ellipse cx='44' cy='48' rx='3.5' ry='8' transform='rotate(-40 44 48)'/>"
    "<ellipse cx='60' cy='35' rx='3.5' ry='8' transform='rotate(-55 60 35)'/>"
    "<ellipse cx='76' cy='22' rx='3.5' ry='8' transform='rotate(-65 76 22)'/>"
    "<ellipse cx='36' cy='78' rx='3.5' ry='8' transform='rotate(10 36 78)'/>"
    "<ellipse cx='52' cy='60' rx='3.5' ry='8' transform='rotate(-5 52 60)'/>"
    "<ellipse cx='68' cy='46' rx='3.5' ry='8' transform='rotate(-15 68 46)'/>"
    "<ellipse cx='84' cy='32' rx='3.5' ry='8' transform='rotate(-25 84 32)'/>"
    "</g></svg>\")"
)

st.markdown(
    f"""
    <style>
      #MainMenu, footer, header[data-testid="stHeader"] {{visibility: hidden; height: 0;}}
      .block-container {{padding: 0.6rem 1.6rem 0.4rem 1.6rem; max-width: 100%;}}
      .stApp {{background: linear-gradient(180deg, {BG} 0%, #121c16 100%); color: {TXT};}}
      .stApp p, .stApp li, .stApp span, .stApp label {{color: {TXT};}}

      .banner {{background: linear-gradient(100deg, {DEEP} 0%, #2d6a24 55%, #b08a0c 130%);
               border-radius: 16px; padding: 12px 22px; color: #fff; position: relative; overflow: hidden;
               box-shadow: 0 3px 12px rgba(0,0,0,.45); border-bottom: 5px solid {GOLD};}}
      .banner::after {{content: ""; position: absolute; inset: 0; background-image: {PANICLE};
               background-repeat: repeat-x; background-position: right bottom; opacity: .9; pointer-events: none;}}
      .banner .bt {{font-size: 1.6rem; font-weight: 800; letter-spacing: .01em; color: #fff !important;}}
      .banner .bs {{font-size: .85rem; opacity: .95; color: #fff !important;}}

      .kpi {{background: {CARD}; border-radius: 14px; padding: 10px 14px; border: 1px solid {LINE};
            border-top: 5px solid {GOLD}; box-shadow: 0 2px 8px rgba(0,0,0,.35);}}
      .kpi .l {{font-size: .72rem; color: {BROWN}; text-transform: uppercase; letter-spacing: .05em; font-weight: 700;}}
      .kpi .v {{font-size: 1.5rem; font-weight: 800; color: #fff; line-height: 1.15;}}
      .kpi .d {{font-size: .78rem; font-weight: 600;}}
      .up {{color: {GREEN} !important;}} .down {{color: {RED} !important;}}

      .note {{background: #2b2e1e; border-left: 5px solid {GOLD}; border-radius: 8px; padding: 6px 12px;
             font-size: .84rem; color: {TXT}; margin: -6px 0 12px 0; line-height: 1.38;}}
      .note b {{color: {GOLD};}}

      div[data-baseweb="tab-list"] {{gap: 6px; border-bottom: 2px solid {LINE};}}
      button[data-baseweb="tab"] {{font-weight: 700; border-radius: 10px 10px 0 0;}}
      button[data-baseweb="tab"] p {{color: {MUTED} !important;}}
      button[data-baseweb="tab"][aria-selected="true"] {{background: {CARD};}}
      button[data-baseweb="tab"][aria-selected="true"] p {{color: {GOLD} !important;}}
      div[data-baseweb="tab-highlight"] {{background-color: {GOLD} !important; height: 4px;}}
      label p {{font-weight: 700; color: {TITLE} !important;}}

      .field {{margin-top: 8px; height: 26px; border-radius: 10px; text-align: center; font-size: 1rem; letter-spacing: 6px;
              overflow: hidden; white-space: nowrap; color: #fff;
              background: linear-gradient(90deg, {DEEP}, #2d6a24, #b08a0c, #2d6a24, {DEEP});}}
      .src {{font-size: .75rem; color: {MUTED} !important; text-align: center; margin-top: 4px;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ data
YEARS = [2021, 2022, 2023, 2024, 2025]

province = pd.DataFrame(
    {
        "Year": YEARS,
        "Production": [270963, 232758, 288638, 306775, 326394],
        "Area": [83634, 80358, 82211, 87039, 83555],
        "Yield": [3.24, 2.90, 3.51, 3.52, 3.91],
        "Price": [14.97, 15.28, 18.73, 19.77, 14.93],
        "Prod_S1": [152434, 119503, 157181, 160895, 163192],
        "Prod_S2": [118529, 113255, 131457, 145880, 163202],
        "Area_S1": [46222, 43967, 45569, 44912, 44747],
        "Area_S2": [37412, 36391, 36642, 42127, 38808],
        "Yield_S1": [3.30, 2.72, 3.45, 3.58, 3.65],
        "Yield_S2": [3.17, 3.11, 3.59, 3.46, 4.21],
        "Price_S1": [15.42, 15.23, 17.33, 21.95, 14.56],
        "Price_S2": [14.51, 15.32, 20.13, 17.58, 15.28],
    }
)

MUNIS = [
    "Bunawan", "City of Bayugan", "Esperanza", "La Paz", "Loreto", "Prosperidad",
    "Rosario", "San Francisco", "San Luis", "Santa Josefa", "Sibagat",
    "Talacogon", "Trento", "Veruela",
]
muni_prod = {
    "Bunawan": [29721, 24191, 29680, 30229, 23770],
    "City of Bayugan": [27989, 26203, 31402, 31675, 38530],
    "Esperanza": [26808, 26665, 32338, 38195, 38002],
    "La Paz": [7646, 7033, 8408, 10814, 12262],
    "Loreto": [17380, 13723, 16908, 19485, 23254],
    "Prosperidad": [23591, 19520, 24444, 28150, 31068],
    "Rosario": [14080, 11809, 14718, 16742, 16846],
    "San Francisco": [35805, 27574, 38727, 41381, 41910],
    "San Luis": [2355, 2612, 3423, 4743, 3886],
    "Santa Josefa": [21820, 19509, 23848, 22029, 26616],
    "Sibagat": [24, 22, 31, 8, 54],
    "Talacogon": [9027, 7176, 9562, 10557, 9758],
    "Trento": [16253, 13418, 14578, 15046, 16502],
    "Veruela": [38466, 33303, 40571, 37721, 43936],
}
muni_area = {
    "Bunawan": [9219, 8580, 8695, 8349, 7476],
    "City of Bayugan": [8736, 8702, 8739, 9363, 9270],
    "Esperanza": [8290, 9083, 9240, 10893, 9705],
    "La Paz": [2327, 2481, 2499, 3026, 3142],
    "Loreto": [5356, 4838, 4961, 5494, 6171],
    "Prosperidad": [7257, 6810, 7121, 7824, 7908],
    "Rosario": [4343, 4152, 4336, 4717, 4439],
    "San Francisco": [11154, 9907, 11183, 11499, 10470],
    "San Luis": [715, 921, 1012, 1299, 1155],
    "Santa Josefa": [6420, 6232, 6171, 6346, 6305],
    "Sibagat": [7, 9, 10, 3, 12],
    "Talacogon": [2754, 2596, 2784, 2963, 2665],
    "Trento": [5122, 4716, 4379, 4478, 4368],
    "Veruela": [11934, 11331, 11081, 10785, 10469],
}
muni_yield = {
    "Bunawan": [3.22, 2.82, 3.41, 3.62, 3.18],
    "City of Bayugan": [3.20, 3.01, 3.59, 3.38, 4.16],
    "Esperanza": [3.23, 2.94, 3.50, 3.51, 3.92],
    "La Paz": [3.29, 2.83, 3.36, 3.57, 3.90],
    "Loreto": [3.24, 2.84, 3.41, 3.55, 3.77],
    "Prosperidad": [3.25, 2.87, 3.43, 3.60, 3.93],
    "Rosario": [3.24, 2.84, 3.39, 3.55, 3.79],
    "San Francisco": [3.21, 2.78, 3.46, 3.60, 4.00],
    "San Luis": [3.29, 2.84, 3.38, 3.65, 3.36],
    "Santa Josefa": [3.40, 3.13, 3.86, 3.47, 4.22],
    "Sibagat": [3.38, 2.44, 3.10, 2.67, 4.50],
    "Talacogon": [3.28, 2.76, 3.43, 3.56, 3.66],
    "Trento": [3.17, 2.85, 3.33, 3.36, 3.78],
    "Veruela": [3.22, 2.94, 3.66, 3.50, 4.20],
}


def long(d, name):
    return (
        pd.DataFrame(d, index=YEARS).rename_axis("Year").reset_index()
        .melt("Year", var_name="Municipality", value_name=name)
    )


muni = long(muni_prod, "Production").merge(long(muni_area, "Area")).merge(long(muni_yield, "Yield"))

growth = pd.DataFrame(
    {
        "Year": [2022, 2023, 2024, 2025],
        "Production": [-14.10, 24.01, 6.28, 6.40],
        "Area": [-3.92, 2.31, 5.87, -4.00],
        "Yield": [-10.60, 21.21, 0.39, 10.83],
        "Price": [2.07, 22.62, 5.53, -24.45],
    }
)

corr_prov = pd.DataFrame(
    {
        "Variable": ["Yield", "Harvested area", "Temperature", "Farmgate price", "Rainfall"],
        "r": [0.9801, 0.6759, 0.3612, 0.2992, -0.8264],
    }
)

corr_muni = pd.DataFrame(
    {
        "Harvested area": [0.625, 0.720, 0.845, 0.958, 0.962, 0.966, 0.860, 0.670, 0.968, -0.045, 0.903, 0.802, 0.125, -0.514],
        "Yield": [0.776, 0.981, 0.858, 0.933, 0.948, 0.988, 0.970, 0.941, 0.766, 0.992, 0.883, 0.948, 0.745, 0.949],
        "Farmgate price": [0.671, 0.037, 0.484, 0.179, 0.006, 0.194, 0.395, 0.437, 0.692, -0.024, -0.541, 0.601, -0.282, -0.010],
        "Rainfall": [-0.574, -0.544, -0.800, -0.701, -0.681, -0.784, -0.907, -0.908, -0.821, -0.474, 0.149, -0.981, -0.512, -0.524],
        "Temperature": [0.880, -0.028, 0.391, 0.193, 0.150, 0.289, 0.503, 0.537, 0.568, -0.067, -0.654, 0.735, 0.138, 0.025],
    },
    index=MUNIS,
)

weather = pd.DataFrame(
    {
        "Period": ["2021 S1", "2021 S2", "2022 S1", "2022 S2", "2023 S1", "2023 S2", "2024 S1", "2024 S2", "2025 S1", "2025 S2"],
        "Rainfall": [1877.0, 1852.0, 2192.0, 2302.4, 1913.9, 1701.8, 1081.5, 1837.6, 1791.6, 1726.2],
        "Temp": [26.17, 26.33, 25.67, 26.00, 26.00, 26.50, 26.83, 26.50, 25.67, 26.17],
        "Class": ["Wet", "Wet", "Wet", "Wet", "Wet", "Dry", "Dry", "Dry", "Dry", "Dry"],
        "Production": [152434, 118529, 119503, 113255, 157181, 131457, 160895, 145880, 163192, 163202],
    }
)

fc = pd.DataFrame(
    {
        "Year": [2026, 2027, 2028, 2029, 2030],
        "Production": [340569, 359057, 377545, 396033, 414520],
        "Area": [85316, 85969, 86621, 87273, 87926],
        "Yield": [4.00, 4.20, 4.40, 4.59, 4.79],
        "Price": [18.06, 18.50, 18.95, 19.39, 19.83],
    }
)
fc["Pessimistic"] = (fc["Production"] * 0.95).round()
fc["Optimistic"] = (fc["Production"] * 1.05).round()

evaluation = pd.DataFrame(
    {
        "Indicator": ["Production (MT)", "Harvested area (ha)", "Yield (MT/ha)", "Farmgate price (₱/kg)"],
        "R²": [0.6667, 0.1774, 0.6841, 0.0903],
        "MAE": [13544, 1843, 0.164, 1.834],
        "RMSE": [18488, 1986, 0.188, 1.986],
        "Slope per year": [18488, 652, 0.196, 0.443],
    }
)

METRICS = {
    "Production": ("Production (MT)", "{:,.0f}"),
    "Area": ("Harvested area (ha)", "{:,.0f}"),
    "Yield": ("Yield (MT/ha)", "{:.2f}"),
    "Price": ("Farmgate price (₱/kg)", "₱{:.2f}"),
}




def style(fig, h=330, legend=True):
    fig.update_layout(
        height=h, margin=dict(l=10, r=10, t=38, b=10),
        paper_bgcolor=CARD, plot_bgcolor=CARD, colorway=COLORWAY,
        font=dict(size=12, color=TXT),
        title=dict(font=dict(size=14, color=TITLE)),
        showlegend=legend,
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(color=TXT)),
        hoverlabel=dict(bgcolor="#0f1a13", font_color=TXT),
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE, zeroline=False)
    fig.update_yaxes(gridcolor=LINE, linecolor=LINE, zeroline=False)
    return fig


def note(text):
    """Short discussion box shown under every chart / table."""
    st.markdown(f'<div class="note">📝 <b>Discussion:</b> {text}</div>', unsafe_allow_html=True)


def kpi(col, icon, label, value, delta=None, good_up=True):
    cls, arrow = "", ""
    if delta is not None:
        up = delta >= 0
        cls = "up" if (up == good_up) else "down"
        arrow = "▲" if up else "▼"
    d = (f'<div class="d {cls}">{arrow} {abs(delta):.1f}% vs previous year</div>'
         if delta is not None else '<div class="d">&nbsp;</div>')
    col.markdown(
        f'<div class="kpi"><div class="l">{icon} {label}</div><div class="v">{value}</div>{d}</div>',
        unsafe_allow_html=True,
    )


MFMT = {"Production": "{:,.0f} MT", "Area": "{:,.0f} ha", "Yield": "{:.2f} MT/ha"}
MUNI_METRICS = {k: METRICS[k][0] for k in MFMT}

# ------------------------------------------------------------------ header
st.markdown(
    '<div class="banner"><div class="bt">🌾 Palay Production Dashboard — Agusan del Sur</div>'
    '<div class="bs">Production · Harvested Area · Yield · Farmgate Price &nbsp;|&nbsp; '
    '2021–2025 observed, 2026–2030 linear trend forecast</div></div>',
    unsafe_allow_html=True,
)
f1, f2, f3 = st.columns([1.2, 2.2, 1.2])
year = f1.selectbox("🗓️ Year", YEARS[::-1], index=0)
muni_sel = f2.selectbox("📍 Municipality / City", ["Province (all)"] + MUNIS)
with f3:
    st.iframe(
        """
        <button id="fs" style="margin-top:26px;width:100%;padding:9px;border:0;border-radius:10px;
          background:#d9a50f;color:#1f4d1a;font-weight:800;cursor:pointer;font-size:14px;">⛶ Full screen</button>
        <script>
          document.getElementById('fs').onclick = () => {
            const d = window.parent.document.documentElement;
            if (!window.parent.document.fullscreenElement) d.requestFullscreen();
            else window.parent.document.exitFullscreen();
          };
        </script>
        """,
        height=75,
    )

# ------------------------------------------------------------------ KPIs
row = province[province.Year == year].iloc[0]
prev = province[province.Year == year - 1]


def chg(c):
    return None if prev.empty else (row[c] / prev.iloc[0][c] - 1) * 100


tot_prov = province.Production.sum()
if muni_sel == "Province (all)":
    k = st.columns(5)
    kpi(k[0], "🌾", "Production", f"{row.Production:,.0f} MT", chg("Production"))
    kpi(k[1], "🟩", "Harvested area", f"{row.Area:,.0f} ha", chg("Area"))
    kpi(k[2], "🌱", "Yield", f"{row.Yield:.2f} MT/ha", chg("Yield"))
    kpi(k[3], "💰", "Farmgate price", f"₱{row.Price:.2f}/kg", chg("Price"))
    kpi(k[4], "🔮", "2030 production forecast", f"{fc.Production.iloc[-1]:,.0f} MT")
    if prev.empty:
        note("2021 is the first year of the study, so it serves as the baseline for all later comparisons.")
    else:
        w = lambda c: "rose" if chg(c) >= 0 else "fell"
        note(f"Versus {year - 1}, production {w('Production')} {abs(chg('Production')):.1f}%, harvested area {w('Area')} "
             f"{abs(chg('Area')):.1f}%, yield {w('Yield')} {abs(chg('Yield')):.1f}% and farmgate price {w('Price')} "
             f"{abs(chg('Price')):.1f}%. Output moves mainly with yield, not with land area.")
else:
    m = muni[(muni.Municipality == muni_sel) & (muni.Year == year)].iloc[0]
    mp = muni[(muni.Municipality == muni_sel) & (muni.Year == year - 1)]
    mc = lambda c: None if mp.empty else (m[c] / mp.iloc[0][c] - 1) * 100
    share = m.Production / row.Production * 100
    k = st.columns(5)
    kpi(k[0], "🌾", f"{muni_sel} production", f"{m.Production:,.0f} MT", mc("Production"))
    kpi(k[1], "🟩", "Harvested area", f"{m.Area:,.0f} ha", mc("Area"))
    kpi(k[2], "🌱", "Yield", f"{m.Yield:.2f} MT/ha", mc("Yield"))
    kpi(k[3], "🥣", "Share of provincial output", f"{share:.1f}%")
    kpi(k[4], "💰", "Provincial farmgate price", f"₱{row.Price:.2f}/kg", chg("Price"))
    note(f"In {year}, {muni_sel} supplied {share:.1f}% of Agusan del Sur's palay. Farmgate price is a provincial "
         "figure (no municipal prices exist in the dataset), so it is the same for every municipality.")

st.write("")

# ------------------------------------------------------------------ tabs
t1, t2, t3, t4, t5 = st.tabs(
    ["🌾 Overview", "🗺️ Municipalities", "🔗 Correlation & Climate", "🔮 Forecast 2026–2030", "📋 Data & Model Fit"]
)

# ---- Overview
with t1:
    c1, c2, c3 = st.columns([1.3, 1, 1])
    with c1:
        if muni_sel == "Province (all)":
            f = go.Figure()
            f.add_bar(x=province.Year, y=province.Prod_S1, name="1st semester", marker_color=GREEN)
            f.add_bar(x=province.Year, y=province.Prod_S2, name="2nd semester", marker_color=GOLD)
            f.update_layout(barmode="stack", title="Palay production by semester (MT)")
            f.update_xaxes(dtick=1)
            st.plotly_chart(style(f), width="stretch")
            note("Output dropped to 232,758 MT in 2022, then rose every year to a record 326,394 MT in 2025. "
                 "The 1st semester was the bigger harvest until 2024; in 2025 both semesters were almost equal.")
        else:
            d = muni[muni.Municipality == muni_sel]
            f = go.Figure(go.Scatter(x=d.Year, y=d.Production, mode="lines+markers", line=dict(color=GREEN, width=3)))
            f.update_layout(title=f"{muni_sel}: production (MT)")
            f.update_xaxes(dtick=1)
            st.plotly_chart(style(f), width="stretch")
            first, last = d.Production.iloc[0], d.Production.iloc[-1]
            peak = d.loc[d.Production.idxmax(), "Year"]
            share5 = d.Production.sum() / tot_prov * 100
            note(f"{muni_sel} produced {first:,.0f} MT in 2021 and {last:,.0f} MT in 2025 ({(last / first - 1) * 100:+.1f}%), "
                 f"peaking in {peak}. It contributes {share5:.1f}% of the province's five-year total.")
    with c2:
        f = go.Figure()
        f.add_scatter(x=province.Year, y=province.Area, mode="lines+markers", name="Harvested area (ha)",
                      line=dict(color=BROWN, width=3))
        f.add_scatter(x=province.Year, y=province.Yield, mode="lines+markers", name="Yield (MT/ha)", yaxis="y2",
                      line=dict(color=GREEN, width=3))
        f.update_layout(title="Harvested area vs yield", yaxis=dict(title="ha"),
                        yaxis2=dict(title="MT/ha", overlaying="y", side="right", showgrid=False))
        f.update_xaxes(dtick=1)
        st.plotly_chart(style(f), width="stretch")
        note("Area stayed between 80,358 and 87,039 ha while yield climbed from 3.24 to 3.91 MT/ha, so recent gains "
             "come from more grain per hectare, not more land.")
    with c3:
        f = go.Figure()
        f.add_scatter(x=province.Year, y=province.Price_S1, mode="lines+markers", name="1st sem", line=dict(color=GREEN))
        f.add_scatter(x=province.Year, y=province.Price_S2, mode="lines+markers", name="2nd sem", line=dict(color=GOLD))
        f.add_scatter(x=province.Year, y=province.Price, mode="lines+markers", name="Annual avg",
                      line=dict(color=BROWN, dash="dot"))
        f.update_layout(title="Farmgate price (₱/kg)")
        f.update_xaxes(dtick=1)
        st.plotly_chart(style(f), width="stretch")
        note("Price peaked at ₱19.77/kg in 2024, then fell to ₱14.93 in 2025. In 2024 the semesters differed "
             "sharply (₱21.95 vs ₱17.58), showing how volatile prices are.")

    c4, c5 = st.columns([1.3, 2])
    with c4:
        g = growth.melt("Year", var_name="Indicator", value_name="Growth %")
        f = px.bar(g, x="Year", y="Growth %", color="Indicator", barmode="group",
                   color_discrete_sequence=[GREEN, BROWN, GOLD, WATER], title="Year-on-year growth rate (%)")
        st.plotly_chart(style(f, 300), width="stretch")
        note("2023 was the big rebound (production +24.01%, yield +21.21%). In 2025 production still grew 6.40% "
             "while price dropped 24.45%.")
    with c5:
        sh = province.assign(S1=province.Prod_S1 / province.Production * 100,
                             S2=province.Prod_S2 / province.Production * 100)
        f = go.Figure()
        f.add_bar(y=sh.Year.astype(str), x=sh.S1, orientation="h", name="1st semester share", marker_color=GREEN,
                  text=sh.S1.round(1).astype(str) + "%", textposition="inside")
        f.add_bar(y=sh.Year.astype(str), x=sh.S2, orientation="h", name="2nd semester share", marker_color=GOLD,
                  text=sh.S2.round(1).astype(str) + "%", textposition="inside")
        f.update_layout(barmode="stack", title="Semester share of annual harvest (%)")
        st.plotly_chart(style(f, 300), width="stretch")
        note("The 1st-semester share slid from 56.3% in 2021 to 50.0% in 2025, so the 2nd-semester crop is becoming "
             "just as important to the province's yearly supply.")

# ---- Municipalities
with t2:
    metric = st.radio("🌾 Indicator", list(MUNI_METRICS), format_func=lambda x: MUNI_METRICS[x], horizontal=True)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        d = muni[muni.Year == year].sort_values(metric)
        f = px.bar(d, x=metric, y="Municipality", orientation="h", color=metric, color_continuous_scale=RICE_SCALE,
                   title=f"{MUNI_METRICS[metric]} by municipality, {year}")
        f.update_layout(coloraxis_showscale=False)
        if muni_sel != "Province (all)":
            f.update_traces(marker_line_color=[RED if x == muni_sel else "rgba(0,0,0,0)" for x in d.Municipality],
                            marker_line_width=2)
        st.plotly_chart(style(f, 440, False), width="stretch")
        hi, lo = d.iloc[-1], d.iloc[0]
        extra = ""
        if muni_sel != "Province (all)":
            rank = int(d.Municipality.tolist()[::-1].index(muni_sel)) + 1
            extra = f" {muni_sel} ranks #{rank} of 14 (outlined in red)."
        note(f"In {year}, {hi.Municipality} is highest ({MFMT[metric].format(hi[metric])}) and {lo.Municipality} "
             f"lowest ({MFMT[metric].format(lo[metric])}), a wide gap, so provincial averages hide big local differences.{extra}")
    with c2:
        pv = muni.pivot(index="Municipality", columns="Year", values=metric)
        f = px.imshow(pv, aspect="auto", color_continuous_scale=RICE_SCALE,
                      text_auto=".2f" if metric == "Yield" else ",.0f", title=f"{MUNI_METRICS[metric]}: heat map")
        f.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style(f, 440, False), width="stretch")
        note({
            "Production": "Almost every municipality dipped in 2022 and recovered after. Only Bunawan ended 2025 below 2021 (−20.0%); "
                          "La Paz (+60.4%) and San Luis (+65.0%) grew fastest (Sibagat's +128% rests on a tiny base).",
            "Area": "Harvested area barely changed overall (−0.1%). Bunawan (−18.9%) and Veruela (−12.3%) lost the most land, "
                    "while San Luis (+61.5%) and La Paz (+35.0%) expanded.",
            "Yield": "Yield bottomed out in 2022 in all 14 municipalities and peaked in 2025 in 12 of 14 "
                     "(Bunawan and San Luis peaked in 2024), mirroring the provincial recovery.",
        }[metric])

    tot = muni.groupby("Municipality").Production.sum().sort_values(ascending=False)
    c3, c4 = st.columns([1, 1.6])
    with c3:
        f = px.pie(tot.reset_index(), names="Municipality", values="Production", hole=0.5,
                   title="Share of 5-year provincial production")
        f.update_traces(marker=dict(colors=PIE_COLORS, line=dict(color=CARD, width=2)))
        st.plotly_chart(style(f, 330), width="stretch")
        top4 = tot.iloc[:4]
        note(f"{', '.join(top4.index)} together produce {top4.sum() / tot.sum() * 100:.1f}% of all palay, "
             f"led by {top4.index[0]} ({top4.iloc[0] / tot.sum() * 100:.1f}%). Sibagat is almost zero.")
    with c4:
        top = muni.pivot(index="Year", columns="Municipality", values="Production")
        sel = [muni_sel] if muni_sel != "Province (all)" else list(tot.index[:5])
        f = go.Figure()
        for s in sel:
            f.add_scatter(x=top.index, y=top[s], mode="lines+markers", name=s)
        f.update_layout(title="Production trend — " + ("selected municipality" if muni_sel != "Province (all)"
                                                       else "top 5 producers (MT)"))
        f.update_xaxes(dtick=1)
        st.plotly_chart(style(f, 330), width="stretch")
        if muni_sel == "Province (all)":
            note("Veruela and San Francisco lead the province. Bayugan (+37.7%) and Esperanza (+41.8%) grew strongly, "
                 "while Bunawan is the only top-five producer that ended 2025 below its 2021 level.")
        else:
            s = top[muni_sel]
            note(f"{muni_sel} moved from {s.iloc[0]:,.0f} MT to {s.iloc[-1]:,.0f} MT over the study period; "
                 f"its lowest year was {s.idxmin()} and its highest was {s.idxmax()}.")

# ---- Correlation & climate
with t3:
    c1, c2 = st.columns([1, 1.4])
    with c1:
        d = corr_prov.sort_values("r")
        f = px.bar(d, x="r", y="Variable", orientation="h", color="r", color_continuous_scale=DIV_SCALE,
                   range_color=[-1, 1], title="Pearson r: provincial production vs …", text="r")
        f.update_traces(texttemplate="%{text:+.3f}", textposition="outside")
        f.update_layout(coloraxis_showscale=False, xaxis_range=[-1.1, 1.2])
        st.plotly_chart(style(f, 340, False), width="stretch")
        note("Yield is the strongest driver (r = +0.98). Area is moderate (+0.68), price weak (+0.30) and rainfall "
             "strongly negative (−0.83): wetter years had lower harvests.")
    with c2:
        f = px.imshow(corr_muni, aspect="auto", color_continuous_scale=DIV_SCALE, zmin=-1, zmax=1, text_auto=".2f",
                      title="Pearson r by municipality (n = 5 years each)")
        st.plotly_chart(style(f, 340, False), width="stretch")
        note("Yield correlates positively in all 14 municipalities and rainfall negatively in 13. Area varies "
             "(negative in Veruela). Price and weather are provincial series, so read these as exploratory only.")
    c3, c4 = st.columns(2)
    with c3:
        f = go.Figure()
        f.add_bar(x=weather.Period, y=weather.Rainfall, name="Rainfall (mm)",
                  marker_color=[WATER if c == "Wet" else "#e8b96a" for c in weather.Class])
        f.add_scatter(x=weather.Period, y=weather.Temp, name="Mean temp (°C)", yaxis="y2", mode="lines+markers",
                      line=dict(color=RED, width=3))
        f.update_layout(title="Rainfall (blue = Wet, tan = Dry) & mean temperature",
                        yaxis2=dict(overlaying="y", side="right", showgrid=False, range=[25, 27.5]))
        st.plotly_chart(style(f, 320), width="stretch")
        note("Semesters were classed Wet through 2023 1st sem and Dry afterward. 2024 1st semester was the driest "
             "(1,081.5 mm) yet still produced 160,895 MT. Temperature stayed narrow (25.7–26.8 °C).")
    with c4:
        f = px.scatter(weather, x="Rainfall", y="Production", color="Class", text="Period",
                       color_discrete_map={"Wet": WATER, "Dry": GOLD}, title="Semestral production vs rainfall")
        f.update_traces(textposition="top center", marker_size=12)
        st.plotly_chart(style(f, 320), width="stretch")
        note("Semesters with less rain tended to give higher output, matching the negative correlation. With only "
             "10 semesters this shows association, not proof of cause.")

# ---- Forecast
with t4:
    ind = st.radio("🌾 Indicator", list(METRICS), format_func=lambda x: METRICS[x][0], horizontal=True, key="fc_ind")
    c1, c2 = st.columns([2, 1])
    with c1:
        f = go.Figure()
        f.add_scatter(x=province.Year, y=province[ind], mode="lines+markers", name="Observed",
                      line=dict(color=GREEN, width=3))
        f.add_scatter(x=[2025] + fc.Year.tolist(), y=[province[ind].iloc[-1]] + fc[ind].tolist(), mode="lines+markers",
                      name="Linear trend forecast", line=dict(color=GOLD, width=3, dash="dash"))
        if ind == "Production":
            f.add_scatter(x=fc.Year, y=fc.Optimistic, name="Optimistic (+5%)", line=dict(color="#7cb342", dash="dot"))
            f.add_scatter(x=fc.Year, y=fc.Pessimistic, name="Pessimistic (−5%)", line=dict(color=RED, dash="dot"),
                          fill="tonexty", fillcolor="rgba(242,183,5,.18)")
        f.add_vline(x=2025.5, line_dash="dot", line_color=BROWN)
        f.update_layout(title=f"{METRICS[ind][0]}: observed 2021–2025 and projected 2026–2030")
        f.update_xaxes(dtick=1)
        st.plotly_chart(style(f, 380), width="stretch")
        note({
            "Production": "The trend adds about 18,488 MT a year, reaching 414,520 MT by 2030 (scenario range "
                          "393,794–435,247 MT). R² of 0.67 gives moderate support, but it ignores weather shocks.",
            "Area": "Area is projected to inch up from 85,316 to 87,926 ha. R² is only 0.18 because history zig-zags, "
                    "so treat this as a rough baseline.",
            "Yield": "Yield is projected to rise from 4.00 to 4.79 MT/ha, above any observed value (max 3.91). "
                     "This assumes productivity gains continue at the same pace.",
            "Price": "Price is projected to edge up from ₱18.06 to ₱19.83/kg, but R² is just 0.09 after the 2024 peak and "
                     "2025 fall. Do not read it as a market price.",
        }[ind])
    with c2:
        show = fc[["Year", ind] + (["Pessimistic", "Optimistic"] if ind == "Production" else [])].copy()
        st.markdown("**Projected values**")
        st.dataframe(show.set_index("Year"), width="stretch", height=235)
        note("Values extend the line Ŷ = a + bt (t = 6 to 10). Scenarios are ±5% of the baseline, meant as planning "
             "ranges, not probabilities.")
        r2 = evaluation.set_index("Indicator")["R²"].iloc[list(METRICS).index(ind)]
        st.metric("In-sample R² of this trend", f"{r2:.4f}")
        if r2 < 0.3:
            st.warning("Low R²: treat this projection as a very uncertain baseline.")

# ---- Data & model fit
with t5:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("**Model evaluation (in-sample, 2021–2025)**")
        st.dataframe(evaluation.set_index("Indicator"), width="stretch")
        note("Yield (R² 0.68) and production (0.67) fit moderately well. Area (0.18) and price (0.09) fit poorly. "
             "MAE and RMSE keep each indicator's units, and RMSE above MAE means some yearly errors are large.")
        f = px.bar(evaluation, x="Indicator", y="R²", color="R²", color_continuous_scale=RICE_SCALE, range_color=[0, 1],
                   title="Goodness of fit (R²)", text="R²")
        f.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        f.update_layout(coloraxis_showscale=False, yaxis_range=[0, 1])
        st.plotly_chart(style(f, 280, False), width="stretch")
        note("These are fit statistics on the same five years used to build the models, not tested accuracy for "
             "2026–2030. Low bars warn that the forecast is a baseline only.")
    with c2:
        st.markdown("**Provincial annual & semestral data**")
        st.dataframe(province.set_index("Year"), width="stretch", height=215)
        note("The S1/S2 columns show 2025's record harvest came with a 2nd-semester yield of 4.21 MT/ha, "
             "the highest in the study.")
        st.markdown(f"**Municipal records, {year}**")
        st.dataframe(muni[muni.Year == year].set_index("Municipality").drop(columns="Year"), width="stretch", height=215)
        dd = muni[muni.Year == year]
        note(f"Production ranges from {dd.Production.min():,.0f} MT ({dd.loc[dd.Production.idxmin(), 'Municipality']}) to "
             f"{dd.Production.max():,.0f} MT ({dd.loc[dd.Production.idxmax(), 'Municipality']}) in {year}, "
             "so conclusions should be made per municipality, not only for the province.")
        st.download_button("⬇ Download municipal data (CSV)", muni.to_csv(index=False).encode(),
                           "palay_municipal.csv", "text/csv")

st.markdown('<div class="field">' + "🌾 " * 60 + "</div>", unsafe_allow_html=True)
st.markdown(
    '<div class="src">Source: Pradas, R. C. &amp; Peñaflor, C. D., Agusan del Sur State University — BSIS Capstone. '
    "Data: PSA / PhilRice as reported in the study.</div>",
    unsafe_allow_html=True,
)
