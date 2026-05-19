---
name: link-mentions
description: Scan summary notes and turn plain-text mentions of concepts or examples into Obsidian wiki links. Use after concept/example files are added or renamed and summaries need link refresh.
---

Scan summary notes and turn plain-text mentions of concepts/examples into Obsidian wiki links.

Use this after creating or renaming concept/example files, or anytime links in summaries need a refresh.

---

## Inputs

- `CONCEPT_DIR` (default: `content/concepts/`)
- `EXAMPLE_DIR` (default: `content/examples/`)
- `SUMMARY_DIR` (default: `content/summaries/`)

---

## Step 1 — Build link targets

List all files in `CONCEPT_DIR` and `EXAMPLE_DIR` recursively. Use filenames (without `.md`) as canonical link targets.

---

## Step 2 — Scan summaries

Read all markdown files in `SUMMARY_DIR` recursively. Identify mentions that clearly refer to known concept/example filenames.

### Link patterns

| Pattern | Link as |
|---|---|
| Bold section/header matches target exactly | `**[[Target Name]]**` |
| Bold section/header differs from target wording | `**[[Target Name\|Header Text]]**` |
| Inline concept/example mention | `[[Target Name\|display text]]` |

### Do not link

- Ambiguous or partial matches
- Mentions already linked
- Frontmatter content
- Code blocks or inline code

---

## Step 3 — Apply edits

Update summary files with identified links.

Rules:
- Use `[[File Name|display text]]` when display text differs from filename.
- Preserve existing wording and formatting.
- Read each file before editing it.
