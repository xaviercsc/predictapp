# predictor_app

A lightweight Streamlit-based application that analyzes historical PDF data, extracts numerical patterns, and generates predicted 4-digit number combinations using statistical and machine learning models.

---

## 📁 Project Structure

predictor_app/
│
├── app.py
├── download.py
├── predict.py
├── requirements.txt
└── README.md


---

## 🚀 Features

- Extracts numbers from all PDF files stored inside a folder.
- Applies statistical frequency analysis.
- Applies ML-based models (RandomForest) for prediction.
- Generates likely 4-digit combinations.
- Allows predictions through a user-friendly Streamlit UI.
- Saves generated predictions into text files.

---

## 🔧 Installation

### 1️⃣ Update system

```bash
sudo apt update && sudo apt upgrade -y

2️⃣ Install Python
sudo apt install python3 python3-pip python3-venv -y

3️⃣ Create and activate virtual environment
cd predictor_app
python3 -m venv venv
source venv/bin/activate

4️⃣ Install all dependencies
pip install -r requirements.txt

📥 Downloading Data (PDF Files)

Use the download.py script to download a PDF by passing the URL as an argument.

Example:
python3 download.py "https://example.com/sample.pdf"


The file is automatically saved into:

/home/xmjs_cptc/predictapp/inputdata/


Filename format:

result_YYYYMMDD_HHMMSS.pdf

🔮 Running Predictions

To generate predictions (without UI):

python3 predict.py


This creates:

predictions.txt

🌐 Running Streamlit Web App

Start the UI:

streamlit run app.py


Streamlit runs on:

http://localhost:8501/

🐳 Running With Gunicorn (optional)

Streamlit normally runs standalone, but if needed:

gunicorn app:app


(Only useful if wrapping Streamlit inside a custom wrapper endpoint.)

📌 Notes

Only place PDF files inside /home/xmjs_cptc/predictapp/inputdata/.

The system automatically extracts numbers and trains models.

Generated predictions are deterministic but depend on extracted patterns.

No external APIs are used; everything runs locally.

📄 License

This project is open for personal use, modification, and learning.
