import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import streamlit.components.v1 as components
import io
import os

# ---------------------------
# Streamlit Page Configuration
# ---------------------------
st.set_page_config(
    layout="wide",
    page_title="Starvation Fishery Dashboard"
)

# ---------------------------
# Helper: Create placeholder image if missing
# ---------------------------
def placeholder_image(label: str, size=(600, 400)):
    img = Image.new('RGB', size, color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    text = f"[ {label} Placeholder ]"

    try:
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[0]
        draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill=(200, 200, 200), font=font)
    except Exception:
        draw.text((20, size[1]/2 - 10), text, fill=(200, 200, 200))

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# ---------------------------
# Custom CSS Styling
# ---------------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f4f5;
            font-family: 'Segoe UI', sans-serif;
            color: #1f2937;
        }
        .block-container {
            padding: 2rem 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #e5e7eb;
        }
        .stSelectbox, .stTextArea, .stButton > button {
            background-color: #e2e8f0;
            color: #1f2937;
            border-radius: 8px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #334155;
        }
        .stDataFrame thead tr th {
            background-color: #cbd5e1;
            color: #1f2937;
        }
        .stColumn > div {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        }
        .metric-container {
            display: flex;
            justify-content: space-evenly;
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        .metric-box {
            background: #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            flex: 1 1 160px;
            color: #1e293b;
        }
        .metric-box h3 {
            margin: 0;
            font-size: 0.9rem;
            color: #334155;
        }
        .metric-box p {
            font-size: 1.3rem;
            font-weight: bold;
            margin: 0.2rem 0 0;
            color: #0f766e;
        }
        .diet-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .diet-container img {
            max-height: 320px;
            width: auto;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar Menu Update
# ---------------------------
st.sidebar.markdown("## FWIN 2025")
species_options = ["Walleye", "Smallmouth Bass", "Rainbow Trout", "Yellow Perch", "Brown Trout"]
selected_species = st.sidebar.selectbox("Select a Species", species_options)

st.sidebar.markdown("---")
st.sidebar.markdown("## Forage Netting")
st.sidebar.info("Coming soon")

# ---------------------------
# Species Key and File Paths
# ---------------------------
species_key = selected_species.lower().replace(" ", "_")
fig_dir = f"figures/{species_key}"
data_table_path = os.path.join("figures", f"{species_key}_metrics.csv")
notes_comments_path = os.path.join(fig_dir, "notes.md")

# ---------------------------
# Title
# ---------------------------
st.title(f"Starvation Reservoir Fishery Dashboard: {selected_species}")

# ---------------------------
# Metric Cards
# ---------------------------
if os.path.exists(data_table_path):
    df_metrics = pd.read_csv(data_table_path)
    if not df_metrics.empty:
        first_row = df_metrics.iloc[0]
        st.markdown("<div class='metric-container'>" +
            f"<div class='metric-box'><h3>Sample Size</h3><p>{first_row['Sample Size']}</p></div>" +
            f"<div class='metric-box'><h3>Catch Per Unit Effort</h3><p>{first_row['Catch Per Unit Effort']}</p></div>" +
            f"<div class='metric-box'><h3>Average Total Length</h3><p>{first_row['Average Total Length']} in</p></div>" +
            f"<div class='metric-box'><h3>Range Total Length</h3><p>{first_row['Range Total Length']} in</p></div>" +
            f"<div class='metric-box'><h3>Average Weight</h3><p>{first_row['Average Weight']} lb</p></div>" +
            f"<div class='metric-box'><h3>Range Weight</h3><p>{first_row['Range Weight']} lb</p></div>" +
            f"<div class='metric-box'><h3>Average Relative Weight</h3><p>{first_row['Average Relative Weight']}</p></div>" +
            "</div>", unsafe_allow_html=True)

# ---------------------------
# MAP + LENGTH FREQ
# ---------------------------
map_path = os.path.join(fig_dir, "site_map.html")
len_hist_path = os.path.join(fig_dir, "length_histogram.png")
len_notes = os.path.join(fig_dir, "length_frequency_notes.md")

if os.path.exists(map_path) or os.path.exists(len_hist_path):
    st.subheader("Sample Map & Length Distribution")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Site Map**")
        if os.path.exists(map_path):
            with open(map_path, 'r', encoding='utf-8') as f:
                map_html = f.read()
            components.html(map_html, height=650, width=650)
        else:
            st.image(placeholder_image("Map"))

    with col2:
        st.markdown("**Length Frequency Histogram**")
        if os.path.exists(len_hist_path):
            st.image(len_hist_path)
            if os.path.exists(len_notes):
                with open(len_notes, 'r', encoding='utf-8') as f:
                    st.markdown(f.read())
        else:
            st.image(placeholder_image("Length Histogram"))

# ---------------------------
# DIET COMPOSITION + MANAGEMENT NOTES
# ---------------------------
diet_path = os.path.join(fig_dir, "diet_piechart.png")
diet_notes = os.path.join(fig_dir, "diet_composition_notes.md")

if os.path.exists(diet_path) or os.path.exists(notes_comments_path):
    st.subheader("Diet Composition & Management Notes")
    diet_col, notes_col = st.columns([1.2, 1])

    with diet_col:
        st.markdown("**Diet Composition**")
        if os.path.exists(diet_path):
            st.image(diet_path)
            if os.path.exists(diet_notes):
                with open(diet_notes, 'r', encoding='utf-8') as f:
                    st.markdown(f.read())
        else:
            st.image(placeholder_image("Diet Chart"))

    with notes_col:
        st.markdown("**Management Notes**")
        if os.path.exists(notes_comments_path):
            with open(notes_comments_path, 'r', encoding='utf-8') as f:
                st.markdown(f.read())

# ---------------------------
# TREND BOARDS
# ---------------------------
trend_info = [
    ("Relative Weight Trend", "wr_trend.png", "wr_trend_notes.md"),
    ("Proportional Size Distribution Trend", "psd_trend.png", "proportional_size_distribution_trends_notes.md"),
    ("Catch Per Unit Effort Trend", "cpue_trend.png", "cpue_trend_notes.md")
]

visible_trends = []
for label, fig, note in trend_info:
    fig_path = os.path.join(fig_dir, fig)
    if os.path.exists(fig_path):
        visible_trends.append((label, fig_path, os.path.join(fig_dir, note)))

if visible_trends:
    st.subheader("Condition & Abundance Trends")
    trend_cols = st.columns(len(visible_trends))
    for col, (label, fig_path, notes_path) in zip(trend_cols, visible_trends):
        with col:
            st.markdown(f"**{label}**")
            st.image(fig_path)
            if os.path.exists(notes_path):
                with open(notes_path, 'r', encoding='utf-8') as f:
                    st.markdown(f.read())

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
---
<p style='text-align: center; color: gray;'>Generated as part of Fall 2025 Starvation Reservoir Netting Project</p>
""", unsafe_allow_html=True)
