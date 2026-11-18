from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "network_ids.joblib"
SAMPLE_PATH = ROOT / "sample_flows.csv"

st.set_page_config(page_title="Network Intrusion Detection")
st.title("Network Intrusion Detection")
st.write(
    "This project classifies network flows as Benign or Suspicious. "
    "The classifier uses numeric flow statistics and was trained on CIC-IDS2017. "
    "Suspicious predictions can help analysts prioritize flows for review."
)

@st.cache_resource
def load_model():
    # Load the project artifact bundled with the app.
    return joblib.load(MODEL_PATH)

if not MODEL_PATH.is_file():
    st.error("Add network_ids.joblib from the Colab output ZIP beside streamlit_app.py.")
    st.stop()

artifact = load_model()
st.write(f"Trained classifier: {artifact['model_name']}")
uploaded = st.file_uploader("Upload an unlabeled CSV of network flows", type=["csv"])
use_sample = st.button("Run sample flows")

if SAMPLE_PATH.is_file():
    st.download_button("Download sample CSV", SAMPLE_PATH.read_bytes(),
                       file_name=SAMPLE_PATH.name, mime="text/csv")

if use_sample and not SAMPLE_PATH.is_file():
    st.error("Add sample_flows.csv from the Colab output ZIP beside streamlit_app.py.")
    st.stop()

source = SAMPLE_PATH if use_sample else uploaded
if source is None:
    st.stop()

# Apply the same feature order and numeric conversion as the Colab demo.
required = artifact["feature_columns"]
try:
    rows = pd.read_csv(source)
    missing = sorted(set(required) - set(rows.columns))
    if missing:
        raise ValueError(f"Missing input columns: {', '.join(missing)}")
    if rows.empty:
        raise ValueError("The CSV must contain at least one flow.")
    inputs = rows.loc[:, required].apply(pd.to_numeric, errors="raise")
    inputs = inputs.astype("float32").replace([np.inf, -np.inf], np.nan)
except (ValueError, UnicodeError) as error:
    st.error(f"Could not read the network flows: {error}")
    st.stop()

predictions = artifact["pipeline"].predict(inputs)
results = pd.DataFrame({
    "Flow row": np.arange(1, len(rows) + 1),
    "Prediction": np.where(predictions == 1, "Suspicious", "Benign"),
})
st.metric("Suspicious flows", int((predictions == 1).sum()))
st.dataframe(results, hide_index=True)
st.download_button("Download predictions", results.to_csv(index=False),
                   file_name="predictions.csv", mime="text/csv")
