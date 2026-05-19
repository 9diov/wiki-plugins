# Wiki Build

A Claude Code plugin for building a structured knowledge wiki from books. It provides skills that take you from raw ebook files to a fully linked Obsidian vault with summaries, concept notes, example notes, org notes, and concept maps.

## Skills

| Skill | Trigger |
|---|---|
| `setup-wiki` | Bootstrap a new wiki vault (directories, config, AGENTS.md, git init) |
| `ingest-ebook` | Convert `.epub`/`.pdf` from `sources/unprocessed/` into clean Markdown chapters |
| `process-chapters` | Transform source chapters into summaries, concepts, and examples |
| `extract-orgs` | Generate org notes from a book's example files |
| `link-mentions` | Refresh Obsidian wiki links in summary notes after adding/renaming files |
| `build-concept-canvas` | Create `maps/<book-id>/Concept Map.canvas` from concept files |
| `generate-book-summary` | Write a full-book long-form summary article in HBR style |

## Typical workflow

```
setup-wiki          # once per vault
  └── ingest-ebook        # once per book
        └── process-chapters    # per chapter or batch
              ├── extract-orgs
              ├── link-mentions
              ├── build-concept-canvas
              └── generate-book-summary
```

## Usage

Skills are invoked via Claude Code's slash-command interface. Example:

```
/wiki-build:ingest-ebook
/wiki-build:process-chapters BOOK_ID=7pw chapters=1-3
/wiki-build:generate-book-summary BOOK_ID=7pw
```

Each skill reads its own `SKILL.md` for full input options and step-by-step logic.

## Vault layout

Skills expect (and produce) this directory structure inside the wiki vault:

```
sources/<book-id>/          raw Markdown chapters
sources/unprocessed/        drop new ebooks here
content/concepts/<book-id>/ one file per concept
content/examples/<book-id>/ one file per case study or example
content/summaries/<book-id>/one file per chapter + SUMMARY.md
content/concept-types/      Framework, Practice, etc.
content/org/                one file per organization
maps/<book-id>/             Obsidian canvas concept maps
```
