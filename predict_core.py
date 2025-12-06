import os
import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

INPUT_DIR = "/home/xmjs_cptc/predictapp/inputdata/"
EXTRACT_DIR = "/home/xmjs_cptc/predictapp/extracted/"
PREDICT_DIR = "/home/xmjs_cptc/predictapp/predictions/"

os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(PREDICT_DIR, exist_ok=True)


def extract_numbers_from_pdf(pdf_path):
    """Extract all 4-digit sequences from PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    import re
    numbers = re.findall(r"\b\d{4}\b", text)
    return [int(n) for n in numbers]


def build_dataset():
    """Scan folder → extract → build CSV dataset."""
    all_numbers = []

    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            nums = extract_numbers_from_pdf(pdf_path)
            all_numbers.extend(nums)

    df = pd.DataFrame({"number": all_numbers})
    csv_path = os.path.join(EXTRACT_DIR, "lottery_data.csv")
    df.to_csv(csv_path, index=False)
    return df


def train_model(df):
    """Very simple ML model to fit number frequency pattern."""
    df_freq = df["number"].value_counts().reset_index()
    df_freq.columns = ["number", "count"]

    # Create features
    df_freq["d1"] = df_freq["number"] // 1000
    df_freq["d2"] = (df_freq["number"] // 100) % 10
    df_freq["d3"] = (df_freq["number"] // 10) % 10
    df_freq["d4"] = df_freq["number"] % 10

    X = df_freq[["d1", "d2", "d3", "d4"]]
    y = df_freq["count"]

    model = RandomForestClassifier()
    model.fit(X, y)
    return model


def predict_next(model, top_n=20):
    """Predict most likely next 4-digit numbers."""
    candidates = list(range(0, 10000))

    preds = []
    for num in candidates:
        d1 = num // 1000
        d2 = (num // 100) % 10
        d3 = (num // 10) % 10
        d4 = num % 10
        score = model.predict([[d1, d2, d3, d4]])[0]
        preds.append((num, score))

    preds_sorted = sorted(preds, key=lambda x: x[1], reverse=True)
    best = preds_sorted[:top_n]

    # Save
    out_path = os.path.join(PREDICT_DIR, "predictions.txt")
    with open(out_path, "w") as f:
        for num, score in best:
            f.write(f"{num:04d} (score={score})\n")

    return best
