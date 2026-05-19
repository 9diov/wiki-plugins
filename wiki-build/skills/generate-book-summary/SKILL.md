---
name: generate-book-summary
description: Generate a full-book summary as a long-form HBR-style article from all sources, summaries, concepts, and examples for a given book. Use when the user asks to generate or write a whole-book summary article.
---

Generate a comprehensive long-form summary article for a book in this vault.

The user can specify a book by its ID (e.g. `pbig`, `7pw`) or by title.

---

## Inputs

- `BOOK_ID` — the short folder name used across `sources/`, `content/summaries/`, `content/concepts/`, and `content/examples/`

---

## Step 1 — Resolve BOOK_ID

If not provided, infer from context or ask.

Confirm the directories exist:
- `sources/<book-id>/`
- `content/summaries/<book-id>/`
- `content/concepts/<book-id>/`
- `content/examples/<book-id>/`

---

## Step 2 — Read all content in parallel

Read all files from these four directories simultaneously:

1. `content/summaries/<book-id>/` — chapter summary files (skip any existing `SUMMARY.md`)
2. `content/concepts/<book-id>/` — all concept files
3. `content/examples/<book-id>/` — all example files (filenames only, for inline linking)

Do not read raw source chapters — the processed summaries and concept/example files are sufficient.

---

## Step 3 — Draft the article

Write a long-form article in **HBR article style**:

- **Audience**: intelligent non-specialist reader — someone who has not read the book
- **Tone**: authoritative, clear, narrative-driven; no bullet lists in the main body
- **Length**: thorough enough to convey the book's full argument, but every sentence earns its place
- **Structure**: use `##` section headers as thematic breaks, not chapter-by-chapter recaps

### Article structure

```
## [Opening section — core thesis and why it matters]

## [Central framework / key insight]

## [Part I: first major theme — walk through the argument with examples]

## [Part II: second major theme]

...

## [Practical takeaway / closing]
```

### Writing rules

1. **Lead with the argument, not the table of contents.** Open with the book's central claim and its stakes.
2. **Integrate examples inline.** Don't isolate examples in separate sections — weave them into the argument as evidence.
3. **Name concepts as they appear.** Introduce concept names when first used; don't front-load a glossary.
4. **Different, not better.** Capture the book's own reasoning rather than summarizing chapter titles.
5. **No bullet lists** in the body. Prose only.

---

## Step 4 — Add inline wiki links

Every mention of a concept or example that has a corresponding file in `content/concepts/<book-id>/` or `content/examples/<book-id>/` should become an Obsidian wiki link.

Link format:
- `[[content/concepts/<book-id>/Concept Name|Concept Name]]`
- `[[content/examples/<book-id>/Example Name|Example Name]]`

Rules:
- Link the **first meaningful mention** of each concept/example; don't repeat the link on every occurrence
- Use display text that reads naturally in the sentence
- Do not link generic words that happen to match a filename

---

## Step 5 — Write frontmatter and output

Create `content/summaries/<book-id>/SUMMARY.md`.

Frontmatter:
```yaml
---
type: summary
book-id: <book-id>
title: "<Full Book Title>"
authors: "<Author Names>"
---
```

If `SUMMARY.md` already exists, confirm with the user before overwriting.

---

## Conventions

- Prefer parallel reads when loading many files
- Check for existing `SUMMARY.md` before writing
- Keep filenames and wiki links stable — use exact concept/example filenames
