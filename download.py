#!/usr/bin/env python3
"""
Robust download.py

Usage:
    python3 download.py "https://result.keralalotteries.com/viewlotisresult.php?drawserial=75104"

Saves PDF to: /home/xmjs_cptc/predictapp/inputdata/results_YYYYMMDD_HHMMSS.pdf
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SAVE_DIR = "/home/xmjs_cptc/predictapp/inputdata/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def build_filename(prefix="results", ext="pdf"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{now}.{ext}"

def save_binary_content(content, out_path):
    with open(out_path, "wb") as f:
        f.write(content)
    print(f"[OK] Saved binary to: {out_path}")

def get_response(url, stream=False, timeout=15):
    r = requests.get(url, headers=HEADERS, timeout=timeout, stream=stream)
    r.raise_for_status()
    return r

def find_pdf_link_from_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    # 1) Search for any <a href> that ends with .pdf
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.lower().endswith(".pdf"):
            return requests.compat.urljoin(base_url, href)
    # 2) Search for iframe/object/embed tags with PDF src
    for tag in soup.find_all(["iframe", "object", "embed"]):
        src = tag.get("src") or tag.get("data") or ""
        if src and src.lower().endswith(".pdf"):
            return requests.compat.urljoin(base_url, src)
    return None

def render_page_to_pdf(url, out_path):
    try:
        import pdfkit
    except Exception as e:
        print("[WARN] pdfkit not available:", e)
        return False

    try:
        options = {"enable-local-file-access": None, "quiet": ""}
        pdfkit.from_url(url, out_path, options=options)
        print(f"[OK] Rendered PDF via pdfkit: {out_path}")
        return True
    except Exception as e:
        print("[ERROR] pdfkit rendering failed:", e)
        return False

def download(url):
    ensure_dir(SAVE_DIR)

    try:
        # First request without streaming to check content-type
        r = get_response(url, stream=False)
    except Exception as e:
        print("[ERROR] Could not fetch URL:", e)
        return

    content_type = r.headers.get("Content-Type", "").lower()
    # If server returned a PDF directly
    if "application/pdf" in content_type or r.url.lower().endswith(".pdf"):
        out_pdf = os.path.join(SAVE_DIR, build_filename("results", "pdf"))
        # get content in streaming mode to avoid loading huge files entirely in memory
        try:
            r2 = get_response(r.url, stream=True)
            with open(out_pdf, "wb") as f:
                for chunk in r2.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[OK] PDF downloaded from response: {out_pdf}")
            return
        except Exception as e:
            print("[WARN] streaming download failed, trying non-stream write:", e)
            try:
                save_binary_content(r.content, out_pdf)
                return
            except Exception as e2:
                print("[ERROR] Failed to save PDF:", e2)
                return

    # If response is HTML, try to discover embedded PDF links
    html = r.text
    pdf_link = find_pdf_link_from_html(html, r.url)
    if pdf_link:
        print("[INFO] Found embedded PDF link:", pdf_link)
        try:
            rpdf = get_response(pdf_link, stream=True)
            out_pdf = os.path.join(SAVE_DIR, build_filename("results", "pdf"))
            with open(out_pdf, "wb") as f:
                for chunk in rpdf.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[OK] Embedded PDF downloaded: {out_pdf}")
            return
        except Exception as e:
            print("[WARN] Failed to download embedded PDF:", e)

    # No direct PDF found: attempt to render page to PDF via pdfkit (wkhtmltopdf)
    out_pdf = os.path.join(SAVE_DIR, build_filename("results", "pdf"))
    rendered = render_page_to_pdf(url, out_pdf)
    if rendered:
        return

    # Final fallback: save HTML for manual "Save as PDF"
    html_path = os.path.join(SAVE_DIR, os.path.splitext(os.path.basename(out_pdf))[0] + ".html")
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Saved HTML fallback to: {html_path}")
    except Exception as e:
        print("[ERROR] Failed to save HTML fallback:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 download.py <url>")
        sys.exit(1)
    download(sys.argv[1])
