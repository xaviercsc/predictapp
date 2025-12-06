#!/usr/bin/env python3
"""
download.py

Usage:
    python3 download.py "https://result.keralalotteries.com/viewlotisresult.php?drawserial=75104"

Saves PDF as: /home/xmjs_cptc/predictapp/inputdata/results_YYYYMMDD_HHMMSS.pdf

Behavior:
1) If the page contains a direct .pdf link, downloads it.
2) Otherwise, tries to render the page to PDF via pdfkit (wkhtmltopdf).
3) If pdfkit is unavailable, saves the HTML to an .html file as a fallback.
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SAVE_DIR = "/home/xmjs_cptc/predictapp/inputdata/"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_page(url, timeout=15):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r

def find_pdf_link_from_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    # common places: <a href="...pdf"> or direct link inside iframe/object
    # 1) Search links
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.lower().endswith(".pdf"):
            # make absolute
            return requests.compat.urljoin(base_url, href)
    # 2) Search iframe/object src
    for tag in soup.find_all(["iframe", "object"], src=True):
        src = tag.get("src", "").strip()
        if src.lower().endswith(".pdf"):
            return requests.compat.urljoin(base_url, src)
    # 3) Search embed tags
    for tag in soup.find_all("embed", src=True):
        src = tag.get("src", "").strip()
        if src.lower().endswith(".pdf"):
            return requests.compat.urljoin(base_url, src)
    return None

def download_binary(url, out_path):
    print(f"[INFO] Downloading binary: {url}")
    r = get_page(url)
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"[OK] Saved binary to: {out_path}")

def render_page_to_pdf(url, out_path):
    # try to import pdfkit (which requires wkhtmltopdf system binary)
    try:
        import pdfkit
    except Exception as e:
        print("[WARN] pdfkit not installed or import failed:", e)
        return False

    # try to render
    print("[INFO] Rendering page to PDF via pdfkit (wkhtmltopdf)...")
    try:
        # you can pass options if needed
        options = {
            "enable-local-file-access": None,
            "quiet": ""
        }
        pdfkit.from_url(url, out_path, options=options)
        print(f"[OK] Rendered PDF saved to: {out_path}")
        return True
    except Exception as e:
        print("[ERROR] pdfkit rendering failed:", e)
        return False

def save_html_fallback(html, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Saved HTML fallback to: {out_path}")

def build_filename(prefix="results"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{now}.pdf"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 download.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    ensure_dir(SAVE_DIR)

    try:
        r = get_page(url)
    except Exception as e:
        print("[ERROR] Could not fetch page:", e)
        sys.exit(1)

    pdf_link = find_pdf_link_from_html(r.text, url)
    out_pdf_path = os.path.join(SAVE_DIR, build_filename())

    if pdf_link:
        try:
            download_binary(pdf_link, out_pdf_path)
            return
        except Exception as e:
            print("[WARN] Failed to download direct PDF link:", e)
            # fallthrough to render

    # If no direct PDF link or download failed, try rendering
    rendered_ok = render_page_to_pdf(url, out_pdf_path)
    if rendered_ok:
        return

    # Fallback: save HTML so you can open and "Save as PDF" manually
    html_path = os.path.join(SAVE_DIR, os.path.splitext(os.path.basename(out_pdf_path))[0] + ".html")
    save_html_fallback(r.text, html_path)
    print("[INFO] As a fallback the page HTML has been saved; open in a browser and Print→Save as PDF.")

if __name__ == "__main__":
    main()
