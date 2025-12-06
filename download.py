#!/usr/bin/env python3

import sys
import os
import datetime
import pdfkit

# Fixed download folder
DOWNLOAD_FOLDER = "/home/xmjs_cptc/predictapp/inputdata/"

def download_lottery_pdf(url):
    # Check if folder exists
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    # Generate filename with current date and time
    now = datetime.datetime.now()
    filename = f"results_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    try:
        pdfkit.from_url(url, output_path)
        print(f"PDF saved successfully: {output_path}")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 download_lottery_pdf.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    download_lottery_pdf(url)
