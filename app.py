import streamlit as st
import pandas as pd
import os
from predict_core import build_dataset, train_model, predict_next, EXTRACT_DIR

st.title("🎯 Kerala Lottery 4-Digit Predictor (AI + Statistics)")

st.write("Upload PDFs → Extract 4-digit numbers → Predict most probable next numbers.")

uploaded_files = st.file_uploader("Upload Kerala Lottery PDF files", type=["pdf"], accept_multiple_files=True)

INPUT_DIR = "/home/xmjs_cptc/predictapp/inputdata/"

if uploaded_files:
    for up in uploaded_files:
        save_path = os.path.join(INPUT_DIR, up.name)
        with open(save_path, "wb") as f:
            f.write(up.read())
    st.success("PDFs saved. Click below to process.")


if st.button("Process PDFs & Predict"):
    st.info("Extracting data...")
    df = build_dataset()
    st.write("Extracted numbers:", df.head())

    st.info("Training ML model...")
    model = train_model(df)

    st.info("Predicting next numbers...")
    predictions = predict_next(model, top_n=30)

    nums = [f"{n:04d}" for n, s in predictions]
    st.success("Predicted Most Likely 4-Digit Numbers:")

    st.write(nums)
    st.download_button("Download Predictions", "\n".join(nums), "predictions.txt")
