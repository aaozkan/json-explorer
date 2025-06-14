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

records = []
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        data["__filename"] = file.name
        records.append(data)

df = pd.DataFrame(records)

with st.sidebar:
    st.header("🔎 Filter")
    select_field = st.selectbox("Filter by field", ["(none)"] + [c for c in df.columns if c != "__filename"])
    value = None
    if select_field != "(none)":
        value = st.text_input(f"Value for {select_field}")

filtered_df = df
if select_field != "(none)" and value:
    filtered_df = filtered_df[filtered_df[select_field].astype(str).str.contains(value, case=False)]

st.write(f"**{len(filtered_df)} files match.**")

st.dataframe(filtered_df.drop(columns="__filename"), use_container_width=True)

filename = st.selectbox("Select a file for details", filtered_df["__filename"].tolist())
if filename:
    data = next(rec for rec in records if rec["__filename"] == filename)
    st.subheader(f"Details for: `{filename}`")
    st.json(data)

st.markdown("---")
st.caption("Simple Streamlit browser for your JSON output. Modify as you wish!")
