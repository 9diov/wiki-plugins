---
name: process-chapters
description: Process one or more source chapters into summaries, concepts, and examples. Use when the user asks to transform chapter files into wiki-ready summary, concept, and example notes.
---

Process one or more source chapters into summaries, concepts, and examples.

The user can specify chapters by number, filename, or range.

---

## Inputs

- `BOOK_ID` (for namespacing outputs, e.g. `hom`, `tps`, `tpp`)
- `SOURCE_DIR` (default pattern: `sources/<book-id>/`)
- `SUMMARY_DIR` (default pattern: `content/summaries/<book-id>/`)
- `CONCEPT_DIR` (default: `content/concepts/`)
- `EXAMPLE_DIR` (default: `content/examples/`)

---

## Step 1 — Read source chapters

Read the specified chapter files from `SOURCE_DIR`.
Capture the filename prefix (for example `09-`, `14-`) so summary filenames mirror source ordering.

---

## Step 2 — Create chapter summaries

Create one summary file per chapter in `SUMMARY_DIR`.

Filename pattern:
- `<prefix>-Chapter <chapter number>-<Simplified Title>.md`

Structure: check `SUMMARY_DIR/TEMPLATE.md` for structure. If it does not exist, propose an approrpiate one, or use the suggested structure:

```markdown
# Chapter N: [Title]

## Core Argument
1-2 sentence distillation of the chapter's thesis.

## Key Ideas
Extract key ideas (a meaningful statement), each use 2-3 sentences to describe.


## Key Concepts

**[Concept Name]**
2-5 sentence explanation with a concrete example when useful.

## Key Quotes (when appropriate)
Include key quotes from characters (for fiction) or figures (for non-fiction).

## Illustrative Examples
Brief examples and what each illustrates.
```

Include `## Illustrative Examples` only when there are meaningful examples to call out.

---

## Step 3 — Extract concepts

For each distinct concept:
1. Check if a matching concept file already exists in `CONCEPT_DIR` (recursively).
2. If it exists, do not duplicate.
3. If not, create a new concept file.

Filename convention:
- Normal casing with spaces, no dashes (for example `Limiting Step.md`).

Suggested template:

```markdown
---
concept-type: "[[Framework]]"
description: "One sentence summary."
related-concepts:
  - "[[Other Concept]]"
sources:
  - "[[source-file|display title]]"
---

# [Concept Name]

One-line definition.

## Why It Matters
Concise explanation.
```

Concept type guidance:
- `[[Framework]]`: diagnostic mental model
- `[[Practice]]`: actionable method/process

---

## Step 4 — Extract examples

For each concrete case/example:
1. Check if it already exists in `EXAMPLE_DIR` (recursively).
2. If it exists, do not duplicate.
3. If not, create a new example file.

Filename convention:
- Normal casing with spaces, no dashes (for example `Intel College Recruiting.md`).

Suggested template:

```markdown
---
description: "One sentence summary."
related-concepts:
  - "[[Concept Name]]"
sources:
  - "[[source-file|display title]]"
---

# [Example Name]

Brief setup.

## What It Illustrates
Which concepts this example demonstrates and why.

*Concepts: [[Concept A]], [[Concept B]]*
*Source: [Chapter/section title]*
```

---

## Step 5 — Link examples from concepts

For each concept file created in Step 3, add an `## Examples` section when relevant:

```markdown
## Examples
- **[[Example Name]]** — one-line relevance note
```

Omit this section if no strong example exists.

---

## Step 6 — Link inline mentions in summaries

Re-read each new summary and replace clear concept/example mentions with wiki links.

Rules:
- Bold concept headers: `**Limiting Step**` -> `**[[Limiting Step]]**`
- Alias when needed: `**[[Production Operations|Three Types of Production Operations]]**`
- Inline terms: `[[Concept Name|display text]]`
- Named examples: `[[Example Name|display text]]`
- Avoid ambiguous links.

---

## Step 7 — Cross-linking check

After all files are created, verify that every wikilink written in this session resolves to an actual file.

1. Collect every `[[Link]]` and `[[Link|alias]]` written across all new and updated files.
2. For each link, check whether a matching file exists anywhere under `content/` (search by filename, case-insensitive, stripping the `.md` extension).
3. Report any broken links — wikilinks with no matching file — grouped by the file that contains them.
4. For broken links that represent genuinely missing content (not typos), create stub files so the link resolves:

**Concept stub:**
```markdown
---
concept-type: "[[Framework]]"
description: "TODO"
sources: []
---

# [Concept Name]

TODO
```

**Example stub:**
```markdown
---
description: "TODO"
related-concepts: []
sources: []
---

# [Example Name]

TODO
```

Fix typos in the link text rather than creating stubs for them.

---

## Step 8 — Fill in stubs

For each stub file created in Step 7, go back to the source chapter(s) and write the full content.

Follow the same templates as Steps 3 and 4. A stub should never remain in the vault after a session ends.

---

## Conventions

- Replace error-prone characters in file names (e.g. slash) with a suitable alternative (e.g. dash)
- Keep filenames human-readable and stable.
- Use Obsidian wiki links in frontmatter and body.
- Check for existing files before creating new ones.
- Prefer parallel reads when inspecting multiple files.
