---
name: ingest-ebook
description: Process ebook files from sources/unprocessed into organized Markdown source files. Use when new .epub or .pdf files need to be converted, cleaned, and added to the vault.
---

Convert and organize new ebook files from `sources/unprocessed/` into clean Markdown source files.

---

## Step 1 — Scan for new ebooks

Check `sources/unprocessed/` for `.epub` and `.pdf` files.

---

## Step 2 — Create book folder

Based on the book title, create a short 3–5 character ID (e.g. "7 Powers" → `7pw`, "Understanding Michael Porter" → `ump`).

Create `sources/<book-id>/` if it does not exist.

Move the ebook file into that folder.

---

## Step 3 — Convert to Markdown

**For `.epub` files:**

Ensure `epub2md` is installed:
```
npm install epub2md -g
```

Run `epub2md` on the file to generate Markdown output.

**For `.pdf` files:**

Use a PDF extraction tool to generate Markdown from the text.

Prefer `PyMuPDF4LLM` with OCR enabled (`force_ocr=True`) for scanned or image-only PDFs. If plain extraction returns empty text, rerun with OCR.

If chapter detection is unreliable, split into page-range files:
- `00-Pages 1-12.md`, `01-Pages 13-24.md`, …

---

## Step 4 — Organize output

Move the final Markdown files and any `images/` directory directly into `sources/<book-id>/` — not into a nested subfolder.

---

## Step 5 — Clean and rename

Clean up each file so it contains one coherent section of the book (Preface, Introduction, Chapter N, Index, etc.).

Rename to the format `xx-Part Name.md`:
- `00-Preface.md`
- `01-Introduction.md`
- `02-Chapter 1.md`
- …

---

## Step 6 — Remove temporary files

Delete raw conversion outputs and temporary folders (e.g. `_raw`, `_pdf_raw`, empty nested conversion directories) after cleanup is complete.
