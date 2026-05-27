#!/usr/bin/env python3
"""Convert a PDF to Markdown + images using the datalab.to Marker API."""

import argparse
import base64
import os
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api.datalab.to/api/v1/marker"
POLL_INTERVAL = 5  # seconds between status checks
MAX_WAIT = 600     # give up after 10 minutes


def submit(pdf_path: Path, api_key: str, **kwargs) -> str:
    """Upload the PDF and return the request_id."""
    with open(pdf_path, "rb") as fh:
        files = {"file": (pdf_path.name, fh, "application/pdf")}
        data = {k: v for k, v in kwargs.items() if v is not None}
        resp = requests.post(
            API_BASE,
            headers={"X-API-Key": api_key},
            files=files,
            data=data,
            timeout=120,
        )
    resp.raise_for_status()
    body = resp.json()
    request_id = body.get("request_id")
    if not request_id:
        sys.exit(f"Unexpected response: {body}")
    print(f"Job submitted. request_id={request_id}")
    return request_id


def poll(request_id: str, api_key: str) -> dict:
    """Poll until the job is complete and return the result payload."""
    url = f"{API_BASE}/{request_id}"
    deadline = time.time() + MAX_WAIT
    while time.time() < deadline:
        resp = requests.get(url, headers={"X-API-Key": api_key}, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        status = body.get("status", "unknown")
        if status == "complete":
            return body
        if status == "error":
            sys.exit(f"API reported error: {body.get('error')}")
        print(f"  status={status}, waiting {POLL_INTERVAL}s …")
        time.sleep(POLL_INTERVAL)
    sys.exit("Timed out waiting for conversion to complete.")


def save(result: dict, out_dir: Path, stem: str) -> None:
    """Write markdown file and images/ sub-folder."""
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"

    # Save images first so we can rewrite image refs in the markdown
    images: dict = result.get("images", {})
    if images:
        images_dir.mkdir(exist_ok=True)
        for filename, b64data in images.items():
            img_path = images_dir / filename
            img_path.write_bytes(base64.b64decode(b64data))
        print(f"Saved {len(images)} image(s) to {images_dir}/")

    # Rewrite image references from bare filenames to relative images/ paths
    markdown: str = result.get("markdown", "")
    if images:
        for filename in images:
            markdown = markdown.replace(f"]({filename})", f"](images/{filename})")

    md_path = out_dir / f"{stem}.md"
    md_path.write_text(markdown, encoding="utf-8")
    print(f"Saved markdown to {md_path}")

    score = result.get("parse_quality_score")
    pages = result.get("page_count")
    print(f"Pages: {pages}  |  Quality score: {score}/5")
    if score is not None and score < 3.0:
        print("  ⚠  Low quality score — consider re-running with --mode accurate or --use-llm")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown via datalab.to")
    parser.add_argument("pdf", help="Path to the source PDF file")
    parser.add_argument("--api-key", default=os.environ.get("DATALAB_API_KEY"),
                        help="datalab.to API key (or set DATALAB_API_KEY env var)")
    parser.add_argument("--out-dir", help="Output directory (default: <pdf-stem>/)")
    parser.add_argument("--langs", help="Comma-separated OCR languages, e.g. en,fr")
    parser.add_argument("--mode", choices=["fast", "balanced", "accurate"],
                        default="balanced")
    parser.add_argument("--use-llm", action="store_true",
                        help="Enable LLM enhancement for better accuracy")
    parser.add_argument("--force-ocr", action="store_true",
                        help="Force OCR on every page")
    parser.add_argument("--page-range",
                        help="Pages to convert, e.g. 0,5-10 (0-indexed)")
    parser.add_argument("--max-pages", type=int,
                        help="Maximum number of pages to convert")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("API key required: pass --api-key or set DATALAB_API_KEY env var")

    pdf_path = Path(args.pdf)
    if not pdf_path.is_file():
        sys.exit(f"File not found: {pdf_path}")

    out_dir = Path(args.out_dir) if args.out_dir else Path(pdf_path.stem)

    print(f"Converting: {pdf_path.name}")
    print(f"Output dir: {out_dir}/")

    request_id = submit(
        pdf_path,
        args.api_key,
        output_format="markdown",
        mode=args.mode,
        langs=args.langs,
        use_llm="true" if args.use_llm else None,
        force_ocr="true" if args.force_ocr else None,
        page_range=args.page_range,
        max_pages=args.max_pages,
    )

    print("Waiting for conversion …")
    result = poll(request_id, args.api_key)
    save(result, out_dir, pdf_path.stem)


if __name__ == "__main__":
    main()
