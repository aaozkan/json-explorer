import streamlit as st
import json
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="JSON Explorer", layout="wide")

st.title("🗂️ Extracted JSON Explorer")

json_folder = Path("output_jsons")
json_files = sorted(json_folder.glob("*.json"))

if not json_files:
    st.warning("No JSON files found in output_jsons/")
    st.stop()

# Optional: Load all JSONs into a list of dicts for table/search
records = []
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        data["__filename"] = file.name
        records.append(data)

df = pd.DataFrame(records)

# Simple search/filter
with st.sidebar:
    st.header("🔎 Filter")
    search_text = st.text_input("Text search (in any field)")
    select_field = st.selectbox("Filter by field", ["(none)"] + [c for c in df.columns if c != "__filename"])
    value = None
    if select_field != "(none)":
        value = st.text_input(f"Value for {select_field}")

# Apply search
filtered_df = df
if search_text:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)
    filtered_df = df[mask]
if select_field != "(none)" and value:
    filtered_df = filtered_df[filtered_df[select_field].astype(str).str.contains(value, case=False)]

st.write(f"**{len(filtered_df)} files match.**")

# Show as a table
st.dataframe(filtered_df.drop(columns="__filename"), use_container_width=True)

# Select and view details
filename = st.selectbox("Select a file for details", filtered_df["__filename"].tolist())
if filename:
    data = next(rec for rec in records if rec["__filename"] == filename)
    st.subheader(f"Details for: `{filename}`")
    st.json(data)

st.markdown("---")
st.caption("Simple Streamlit browser for your JSON output. Modify as you wish!")
