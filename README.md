predictor_app

predictor_app is a lightweight AI-powered number pattern analysis and prediction system.
It extracts numerical data from PDF files, builds a statistical dataset, trains a machine-learning model, and generates a list of the most probable upcoming 4-digit sequences based on historical patterns.

The system includes:

A Streamlit web interface

A PDF data ingestion pipeline

An automated numerical pattern extractor

A machine-learning prediction engine

A text-file export of predicted results

🚀 Features

Upload multiple PDF files for processing

Automatic extraction of all 4-digit numeric sequences

Dataset generation and storage

Machine learning–based pattern scoring

Prediction of most probable upcoming 4-digit sequences

Save results into a .txt file

Lightweight and suitable for low-resource environments

📂 Project Structure
predictor_app/
│── app.py
│── download.py
│── predict_core.py
│── requirements.txt
│── README.md
│── inputdata/          # Input PDF files
│── extracted/          # Extracted CSV dataset
│── predictions/        # Output prediction files

🛠 Installation
1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

▶️ Running the Application (Web UI)

Launch the Streamlit app:

streamlit run app.py


The web interface will open in your browser at:

http://localhost:8501

📥 Downloading PDF Data

Use the automated downloader:

python3 download.py "<url_here>"


All downloaded files will be saved to:

/home/xmjs_cptc/predictapp/inputdata/


(You may modify the path in download.py if needed.)

📊 How It Works

Data Extraction:
The system reads all 4-digit numeric patterns from uploaded PDFs.

Dataset Building:
Extracted values are combined into a structured dataset.

Model Training:
A machine-learning model analyzes numeric distributions and patterns.

Prediction:
The system generates a list of highly probable 4-digit sequences.

Export:
Predictions are automatically saved inside:

/home/xmjs_cptc/predictapp/predictions/

📁 Output Format

Predicted numbers are saved as:

predictions.txt


Each line contains a 4-digit number.

🧩 Customization

You can easily modify:

number-length behavior

scoring functions

ML model type

input/output file paths

UI layout in app.py

🧧 Notes

This project is optimized for lightweight environments such as VirtualBox Ubuntu.

No external APIs are required.

All processing is done locally.

📮 Support

For enhancements, UI improvements, or additional ML features, feel free to request an updated version.
