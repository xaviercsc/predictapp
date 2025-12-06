import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

SAVE_DIR = "/home/xmjs_cptc/predictapp/inputdata/"

def download_pdf(url):
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Get HTML
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # Find PDF link
    pdf_link = None
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if ".pdf" in href.lower():
            pdf_link = href
            break

    if not pdf_link:
        print("❌ PDF link NOT FOUND in this page.")
        return

    # Convert relative URL
    if pdf_link.startswith("/"):
        base = "https://result.keralalotteries.com"
        pdf_link = base + pdf_link

    # Download PDF
    pdf_data = requests.get(pdf_link).content
    filename = f"lottery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(pdf_data)

    print(f"✅ PDF saved: {filepath}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 download.py <lottery_result_page_url>")
        sys.exit(1)

    download_pdf(sys.argv[1])
