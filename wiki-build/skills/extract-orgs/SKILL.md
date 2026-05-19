---
name: extract-orgs
description: Go through one book's example files and generate org notes in
content/org/. Creates new org notes or updates existing ones. Use when
processing a new book's examples to populate the org index.
---

Extract org notes from a book's example files.

The user specifies a book by its ID (e.g. `ctc`, `7pw`). Read all examples for
 that book, identify every org mentioned, then create or update org notes in
`content/org/`.

---

## Inputs

- `BOOK_ID` — the book's folder ID (e.g. `7pw`, `ctc`)
- `EXAMPLE_DIR` (default: `content/examples/<book-id>/`)
- `ORG_DIR` (default: `content/org/`)

---

## Step 1 — Read all example files

Read every `.md` file in `EXAMPLE_DIR`. For each example, note:
- Its filename (used in `examples:` frontmatter links)
- Its `related-concepts` and `sources` frontmatter
- Every org mentioned in the body — both **primary orgs** (the example is
about them) and **secondary orgs** (mentioned as foils, acquirers, partners,
customers, or contrast cases)

Use parallel reads for all example files.

---

## Step 2 — Build an org inventory

Produce a working list of all distinct orgs found. For each org record:
- **name** — canonical display name (e.g. `Netflix`, `Toyota`)
- **role** — `primary` (example centres on this org) or `secondary` (mentioned
 in passing)
- **examples** — which example files feature this org
- **concepts** — union of `related-concepts` from those examples
- **sources** — union of `sources` from those examples

When an org appears in multiple examples, merge the concept and source lists
(deduplicate).

---

## Step 3 — Check existing org notes

For each org in the inventory, check whether `content/org/<Org Name>.md`
already exists.

Read any existing file before deciding what to do — note what `examples:`,
`concepts:`, and `sources:` it already contains.

---

## Step 4 — Create or update org notes

### New org

Create `content/org/<Org Name>.md` following this template:

```yaml
---
type: Org
description: "One-sentence summary of the org and why it appears in this
wiki."
industry: "Sector"
examples:
  - "[[Example Filename]]"
concepts:
  - "[[Concept Name]]"
sources:
  - "[[source-file|display title]]"
related-orgs:
  - "[[Other Org]]"
---

# [Org Name]

One-line description of what the org is (founded year, what it does).

## Strategic Significance
Why this org matters to the themes of this wiki — patterns, inflection points,
 lessons. Reference specific concepts inline as [[Concept Name]] where
natural.
```

Guidance:
- description: focus on why this org appears in the wiki, not just what it
does
- industry: plain string, not a wikilink
- related-orgs: include orgs that appear together in examples (foils,
competitors, acquirers) — leave empty rather than guessing
- Use inline [[Concept Name]] links in the body when concepts are mentioned
naturally
- Use inline [[Org Name]] links in the body when other orgs are mentioned
naturally

Existing org — merge

Add any items from the new book's examples that are not already present in
examples:, concepts:, and sources:. Do not remove or rewrite existing content.

If the existing ## Strategic Significance body doesn't mention the new
examples' angle, append a short paragraph rather than rewriting.

---
Step 5 — Cross-link related orgs

For orgs that appear together in the same example (e.g. Netflix and
Blockbuster), ensure each lists the other in related-orgs: if not already
present.

---

## Conventions

- Filename is the org's canonical name with normal casing and spaces:
Toyota.md, SAP.md.
- Read each existing file before editing it.
- Prefer parallel reads; edit sequentially.
- Do not fabricate details not present in the example files — ground
everything in the source material.

The key design choices: Step 2's inventory phase keeps the logic clean by
separating "what orgs exist" from "what files to write." Step 4's merge rule
(append, don't rewrite) protects hand-written content in existing org notes.
