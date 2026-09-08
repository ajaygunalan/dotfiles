#!/usr/bin/env python3
"""Download papers from Sci-Hub given a DOI."""

import argparse
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

SCIHUB_MIRRORS = [
    "https://sci-hub.ru",
    "https://sci-hub.box",
]


def download(doi, output_dir="./downloads"):
    """Download a paper PDF from Sci-Hub by DOI.

    Handles both the old meta-tag format and the new sci-net.xyz iframe format.
    """
    session = requests.Session()
    session.headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    )

    # Try each mirror
    resp = None
    base = None
    for mirror in SCIHUB_MIRRORS:
        try:
            resp = session.get(f"{mirror}/{doi}", timeout=15, allow_redirects=True)
            if resp.status_code == 200:
                base = mirror
                break
        except requests.RequestException:
            continue

    if resp is None or base is None:
        return {"error": "All Sci-Hub mirrors unreachable", "doi": doi}
    if resp.status_code != 200:
        return {"error": f"Page fetch failed: HTTP {resp.status_code}", "doi": doi}

    # Check if paper is in database (Russian "absent" message)
    if "\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442" in resp.text:
        return {"error": "Paper not in Sci-Hub database", "doi": doi}

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract title — try multiple methods
    title = "unknown"
    citation_title = soup.find("meta", attrs={"name": "citation_title"})
    if citation_title and citation_title.get("content"):
        title = citation_title["content"]
    else:
        title_div = soup.find("div", class_="title")
        if title_div:
            title = title_div.get_text(strip=True)
        else:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

    # Extract PDF URL — try multiple methods
    pdf_url = None

    # Method 1: citation_pdf_url meta tag (old format)
    meta = soup.find("meta", attrs={"name": "citation_pdf_url"})
    if meta and meta.get("content"):
        pdf_url = meta["content"]

    # Method 2: iframe src (new sci-net.xyz format)
    if not pdf_url:
        iframe = soup.find("iframe")
        if iframe and iframe.get("src"):
            pdf_url = iframe["src"]

    # Method 3: embed tag
    if not pdf_url:
        embed = soup.find("embed", attrs={"type": "application/pdf"})
        if embed and embed.get("src"):
            pdf_url = embed["src"]

    if not pdf_url:
        return {"error": "No PDF link found on page", "doi": doi, "title": title}

    # Normalize the URL
    if pdf_url.startswith("//"):
        pdf_url = f"https:{pdf_url}"
    elif not pdf_url.startswith("http"):
        pdf_url = f"{resp.url.rstrip('/')}/{pdf_url.lstrip('/')}"

    # Download PDF
    pdf_resp = session.get(pdf_url, timeout=60)
    if pdf_resp.status_code != 200:
        return {"error": f"PDF download failed: HTTP {pdf_resp.status_code}", "doi": doi}

    if pdf_resp.content[:5] != b"%PDF-":
        return {"error": "Downloaded content is not a PDF", "doi": doi}

    # Save
    os.makedirs(output_dir, exist_ok=True)
    safe_name = re.sub(r"[^\w\-.]", "_", doi)
    filepath = os.path.join(output_dir, f"{safe_name}.pdf")

    with open(filepath, "wb") as f:
        f.write(pdf_resp.content)

    return {
        "status": "downloaded",
        "path": filepath,
        "title": title,
        "doi": doi,
        "size_kb": len(pdf_resp.content) // 1024,
    }


def main():
    parser = argparse.ArgumentParser(description="Download papers from Sci-Hub")
    parser.add_argument("doi", help="DOI of the paper (e.g. 10.1038/s41586-021-03819-2)")
    parser.add_argument(
        "--output-dir", default="./downloads", help="Download directory (default: ./downloads)"
    )
    args = parser.parse_args()

    result = download(args.doi, args.output_dir)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
