# lottery_predictor.py
import os
import re
import pdfplumber
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# -----------------------------
# CONFIG
PDF_FOLDER = '/home/xmjs_cptc/predictapp/inputdata'
OUTPUT_FILE = '/home/xmjs_cptc/predictapp/outputdata/predicted_values.txt'
LOWER_PRIZE_PATTERNS = [r'\b\d{4}\b']  # matches any 4-digit number

# -----------------------------
def extract_numbers_from_pdf(pdf_path):
    numbers = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for pattern in LOWER_PRIZE_PATTERNS:
                    matches = re.findall(pattern, text)
                    numbers.extend(matches)
    return numbers

def read_all_pdfs(folder_path):
    all_numbers = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            nums = extract_numbers_from_pdf(pdf_path)
            all_numbers.extend(nums)
    return all_numbers

# -----------------------------
def prepare_dataset(numbers):
    # Count frequency
    count = Counter(numbers)
    df = pd.DataFrame(count.items(), columns=['number', 'frequency'])
    
    # Convert to numeric
    df['number'] = df['number'].astype(int)
    df['frequency'] = df['frequency'].astype(int)
    
    # Feature engineering
    df['digit_sum'] = df['number'].apply(lambda x: sum(int(d) for d in str(x)))
    df['first_digit'] = df['number'].apply(lambda x: int(str(x)[0]))
    
    # Target is probability (high frequency = more probable)
    df['target'] = (df['frequency'] >= df['frequency'].median()).astype(int)
    
    return df

# -----------------------------
def train_model(df):
    X = df[['number', 'digit_sum', 'first_digit']]
    y = df['target']
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)
    return model

# -----------------------------
def predict_numbers(model, top_n=30):
    candidates = np.arange(1000, 10000)
    X_test = pd.DataFrame({
        'number': candidates,
        'digit_sum': [sum(int(d) for d in str(n)) for n in candidates],
        'first_digit': [int(str(n)[0]) for n in candidates]
    })
    probs = model.predict_proba(X_test)[:, 1]
    top_indices = np.argsort(probs)[-top_n:][::-1]
    return X_test.iloc[top_indices]['number'].tolist()

# -----------------------------
def main():
    print("Reading PDFs...")
    numbers = read_all_pdfs(PDF_FOLDER)
    if not numbers:
        print("No numbers found in PDF folder.")
        return
    
    print(f"Total 4-digit numbers extracted: {len(numbers)}")
    
    df = prepare_dataset(numbers)
    model = train_model(df)
    
    print("Predicting probable numbers...")
    predicted_numbers = predict_numbers(model, top_n=30)
    
    # Save to file
    with open(OUTPUT_FILE, 'w') as f:
        for num in predicted_numbers:
            f.write(f"{num}\n")
    
    print(f"Predicted numbers saved to {OUTPUT_FILE}")
    print(predicted_numbers)

# -----------------------------
if __name__ == "__main__":
    main()
