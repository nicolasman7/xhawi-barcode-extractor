import streamlit as st
import pandas as pd
import re
from pathlib import Path

# Page setup
st.set_page_config(page_title="XHAWI Barcode Extractor", layout="centered")

# ✅ Centered logo using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=300)

# Title
st.markdown("<h1 style='text-align: center; font-size: 36px;'>Barcode Extractor</h1>", unsafe_allow_html=True)

# Subheading
st.subheader("Upload a CSV or Excel file")

# Extract barcode from filename
def extract_barcode(filename):
    name = Path(filename).stem
    name_clean = re.sub(r'\s+', '', name)
    name_clean = re.sub(r'\(\d+\)', '', name_clean)
    
    # Match just the barcode between underscores if other text exists
    if "_" in name_clean:
        parts = name_clean.split("_")
        for part in parts:
            if re.fullmatch(r"\d{6,}", part):
                return part
    else:
        # Fallback: match any consecutive digits
        match = re.search(r'\d{6,}', name_clean)
        return match.group(0) if match else ""

    return ""

# File uploader
data_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if data_file:
    try:
        if data_file.name.endswith(".csv"):
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)

        if 'Filename' in df.columns:
            df['Barcode'] = df['Filename'].apply(extract_barcode)
            st.success("✅ Barcodes extracted!")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Updated CSV", csv, "updated_barcodes.csv", "text/csv")
        else:
            st.error("❌ File must contain a 'Filename' column.")
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
