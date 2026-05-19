---
name: setup-wiki
description: Bootstrap a new wiki vault from scratch — directories, AGENTS.md, CLAUDE.md, .obsidian config, .claude settings, concept-type files, .gitignore, README, and git init. Use when the user wants to create a new topic-based wiki.
---

Bootstrap a new wiki vault from scratch.

---

## Inputs

- `WIKI_SLUG` — folder name, kebab-case with `wiki-` prefix (e.g. `wiki-prnt`, `wiki-ai`)
- `WIKI_TOPIC` — plain-language topic description (e.g. "printing industry", "artificial intelligence")
- `WIKI_DESCRIPTION` — one-sentence purpose of the vault (e.g. "A personal knowledge graph built from books on the printing industry.")
- `PARENT_DIR` — parent directory where the wiki folder will be created (default: the directory containing the other wiki-* folders, typically inferred from context)
- `CONCEPT_TYPES` — list of concept type names (default: `Framework`, `Practice`)

If any required input is missing, ask before proceeding.

---

## Step 1 — Confirm inputs

Echo back the resolved values to the user:

```
WIKI_SLUG:       wiki-<slug>
WIKI_TOPIC:      <topic>
WIKI_DESCRIPTION:<description>
PARENT_DIR:      <path>
CONCEPT_TYPES:   Framework, Practice
```

Ask the user to confirm before creating any files.

---

## Step 2 — Create directory structure

Create the following directories under `PARENT_DIR/WIKI_SLUG/`:

```
sources/
sources/unprocessed/
content/
content/concepts/
content/examples/
content/summaries/
content/concept-types/
content/org/
content/synthesis/
maps/
```

Use `mkdir -p` for all directories.

---

## Step 3 — Create `.gitignore`

Create `PARENT_DIR/WIKI_SLUG/.gitignore`:

```
# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json

# Obsidian cache & temp
.obsidian/cache
.trash/

# Claude Code
.claude/settings.local.json

# macOS
.DS_Store
```

---

## Step 4 — Create `.obsidian/` config

Create the following files under `PARENT_DIR/WIKI_SLUG/.obsidian/`:

**`app.json`**
```json
{
  "alwaysUpdateLinks": true
}
```

**`core-plugins.json`**
```json
{
  "file-explorer": true,
  "global-search": true,
  "switcher": true,
  "graph": true,
  "backlink": true,
  "canvas": true,
  "outgoing-link": true,
  "tag-pane": true,
  "footnotes": false,
  "properties": true,
  "page-preview": true,
  "daily-notes": true,
  "templates": true,
  "note-composer": true,
  "command-palette": true,
  "slash-command": false,
  "editor-status": true,
  "bookmarks": true,
  "markdown-importer": false,
  "zk-prefixer": false,
  "random-note": false,
  "outline": true,
  "word-count": true,
  "slides": false,
  "audio-recorder": false,
  "workspaces": false,
  "file-recovery": true,
  "publish": false,
  "sync": true,
  "bases": true,
  "webviewer": false
}
```

**`community-plugins.json`**
```json
[
  "dataview"
]
```

**`graph.json`**
```json
{
  "collapse-filter": false,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [],
  "collapse-display": false,
  "showArrow": false,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1,
  "lineSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.518713248970312,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 250,
  "scale": 1,
  "close": true
}
```

**`appearance.json`**
```json
{}
```

**`canvas.json`**
```json
{}
```

---

## Step 5 — Create `.claude/` settings

Create `PARENT_DIR/WIKI_SLUG/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Write(.claude/skills/**)"
    ]
  }
}
```

---

## Step 6 — Create concept-type files

For each type in `CONCEPT_TYPES`, create `content/concept-types/<Type>.md`.

Use this template for each type, substituting `<Type>` and writing a one-line description appropriate to the vault topic:

**`Framework.md`** (default description: "Mental models for understanding and diagnosing situations.")
```markdown
# Framework

Mental models for understanding and diagnosing situations.

```dataview
TABLE without id file.link as "Concept", description as "Description", sources as "Sources"
FROM "content/concepts"
WHERE concept-type = [[Framework]]
SORT file.name ASC
```
```

**`Practice.md`** (default description: "Actionable methods and routines that can be applied repeatedly.")
```markdown
# Practice

Actionable methods and routines that can be applied repeatedly.

```dataview
TABLE without id file.link as "Concept", description as "Description", sources as "Sources"
FROM "content/concepts"
WHERE concept-type = [[Practice]]
SORT file.name ASC
```
```

If the user provided custom concept types instead, create analogous files with suitable descriptions.

---

## Step 7 — Create `AGENTS.md`

Create `PARENT_DIR/WIKI_SLUG/AGENTS.md` using this template, substituting `WIKI_TOPIC`, `WIKI_DESCRIPTION`, and `CONCEPT_TYPES`:

```markdown
# AGENTS.md — <WIKI_TOPIC> Wiki

This is an Obsidian vault containing a personal knowledge graph built from <WIKI_TOPIC> books.

<WIKI_DESCRIPTION>

Keep edits compatible with this vault's current conventions. Prefer small, human-readable changes over heavy restructuring.

## Directory structure

- `sources/<book-id>/` — raw Markdown chapters extracted from ebooks
- `content/concepts/<book-id>/` — one file per concept extracted from books
- `content/examples/<book-id>/` — one file per concrete example or case study
- `content/summaries/<book-id>/` — one file per chapter summary
- `content/concept-types/` — <list CONCEPT_TYPES> type definitions
- `content/synthesis/` — cross-book synthesis notes
- `content/org/` — one file per organization mentioned in the wiki; filename is the org name (e.g., `Acme Corp.md`)
- `maps/<book-id>/` — Obsidian canvas concept maps

## Core conventions

- One Markdown note per file.
- The first H1 in the body is the display title.
- Store note type in the `type:` frontmatter field.
- Frontmatter properties that start with `_` are Obsidian/tool-managed state. Leave them alone unless explicitly asked to change.

## Concept files

```yaml
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
<for each concept type, write a one-line description of when to use it>
- `[[Framework]]`: diagnostic mental model
- `[[Practice]]`: actionable method/process

## Org files

```yaml
---
type: Org
description: "One-sentence summary of the org and why it appears in this wiki."
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

One-line description of what the org is.

## Significance
Why this org matters to the themes of this wiki — patterns, lessons, inflection points.
```

## Wikilinks

- `[[filename]]` or `[[Note Title]]` for normal links
- `[[filename|display text]]` for custom display text
- Works in frontmatter values and Markdown body

## What agents should do

- Create and edit notes using the frontmatter and H1 conventions above.
- Add or modify relationships without breaking existing wikilinks.
- Update `AGENTS.md` only when the user asks for vault-level guidance changes.

## What agents should avoid

- Do not silently overwrite an existing custom `AGENTS.md`.
- Do not rewrite installation-specific app configuration unless the user explicitly asks.
```

---

## Step 8 — Create `CLAUDE.md`

Create `PARENT_DIR/WIKI_SLUG/CLAUDE.md`:

```markdown
---
type: Note
_organized: true
---

@AGENTS.md

This file is only a Claude Code compatibility shim. Keep shared agent instructions in `AGENTS.md`.
```

---

## Step 9 — Create `README.md`

Create `PARENT_DIR/WIKI_SLUG/README.md`:

```markdown
# <WIKI_TOPIC> Wiki

<WIKI_DESCRIPTION>

## Vault layout

- `content/synthesis/` — cross-book synthesis notes (start here once populated)
- `content/summaries/<book-id>/SUMMARY.md` — whole-book summary; chapter summaries live alongside
- `content/concepts/<book-id>/` — one note per concept
- `content/examples/<book-id>/` — one note per case study
- `content/concept-types/` — <list CONCEPT_TYPES> type definitions
- `content/org/` — one note per organization
- `sources/<book-id>/` — raw extracted chapters (skip unless reading deeply)

## Getting started

Drop ebook files into `sources/unprocessed/` and run the `ingest-ebook` skill to begin processing.
```

---

## Step 10 — Initialize git repository

```
cd PARENT_DIR/WIKI_SLUG
git init
git add .
git commit -m "Initial wiki scaffold"
```

---

## Step 11 — Report

Print a summary of what was created:

```
Created WIKI_SLUG at PARENT_DIR/WIKI_SLUG/

Directories:
  sources/unprocessed/
  content/concepts/
  content/examples/
  content/summaries/
  content/concept-types/
  content/org/
  content/synthesis/
  maps/

Files:
  AGENTS.md
  CLAUDE.md
  README.md
  .gitignore
  .obsidian/app.json
  .obsidian/core-plugins.json
  .obsidian/community-plugins.json
  .obsidian/graph.json
  .obsidian/appearance.json
  .obsidian/canvas.json
  .claude/settings.json
  content/concept-types/Framework.md
  content/concept-types/Practice.md

Next: drop ebook files into sources/unprocessed/ and run /ingest-ebook.
```
