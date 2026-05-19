---
name: build-concept-canvas
description: Build `maps/<book-id>/Concept Map.canvas` without scanning existing map files. Use when creating a new concept map canvas from concept notes.
---

Create a concept map canvas from concept files using a fixed schema and deterministic layout rules.

This skill is designed to avoid token waste from reverse-engineering older canvases.

---

## Inputs

- `BOOK_ID` (required, e.g. `ttw`, `hom`, `tps`)
- `CONCEPT_DIR` (default: `content/concepts/<book-id>/`)
- `MAP_DIR` (default: `maps/<book-id>/`)
- `CANVAS_FILE` (default: `maps/<book-id>/Concept Map.canvas`)
- `GROUPS` (optional ordered list of thematic groups with labels, if not exists infer from list of concepts)
- `STARRED_CONCEPTS` (optional list of concept filenames to highlight)

---

## Canonical canvas schema

Always produce this exact top-level shape:

```json
{
  "nodes": [
    {"id":"g-...","type":"group","x":0,"y":0,"width":560,"height":460,"label":"..."},
    {"id":"n-...","type":"file","file":"content/concepts/<book-id>/<Name>.md","x":30,"y":50,"width":220,"height":70,"color":"5"}
  ],
  "edges": [
    {"id":"e1","fromNode":"n-a","fromSide":"right","toNode":"n-b","toSide":"left"}
  ]
}
```

No extra top-level keys. No comments inside JSON.

---

## Node conventions

### 1) Group nodes

- `id`: `g-<slug>`
- `type`: `group`
- Required keys: `x`, `y`, `width`, `height`, `label`
- Recommended size:
  - Standard group: `width 560`, `height 460–520`
  - Larger group (denser section): widen to `1100–1160`

### 2) Concept file nodes

- `id`: `n-<slug>`
- `type`: `file`
- `file`: full relative path, e.g. `content/concepts/ttw/Long-Term Systems Thinking.md`
- Required keys: `x`, `y`, `width`, `height`, `color`
- Recommended size:
  - `width`: `200–280`
  - `height`: `50–100`

### 3) Colors (string values)

Use only these meanings:

- `"3"` = core concept / star concept
- `"5"` = concept with concept-type = "Framework"
- `"6"` = concept with concept-type = "Practice"

If `STARRED_CONCEPTS` is provided, map them to `"3"`.

---

## Edge conventions

- `id`: sequential `e1`, `e2`, ...
- Allowed sides: `top`, `right`, `bottom`, `left`
- Keep graph sparse and explanatory:
  - Prefer high-signal conceptual dependencies
  - Avoid fully connecting every related concept
  - Target ~1–4 outgoing edges per concept for readability

---

## Layout system (fixed grid)

Use a 3-column grid with consistent spacing:

- Column origins: `x = 0`, `600`, `1200`
- Row origins: `y = 0`, `560`, `1120` (only if needed)
- Inside each group:
  - left lane near `x + 30`
  - right lane near `x + 300`
  - optional center lane near `x + 150`
  - vertical rhythm: +90 to +110 per row

This preserves visual consistency with existing maps and avoids overlap.

---

## Build procedure

## Step 1 — Collect concept files

List markdown files in `CONCEPT_DIR`.
Use filename (without `.md`) as concept display identity.

## Step 2 — Draft groups first

Define `GROUPS` in reading order.
Add all group nodes before concept nodes.

## Step 3 — Place concept nodes

For each concept:
1. Assign group
2. Assign `n-<slug>` id
3. Assign color (`3/5/6`)
4. Place with fixed grid coordinates

## Step 4 — Add edges

Create only meaningful conceptual edges based on:
- direct dependencies
- feedback loops
- bridge concepts across groups

Then number edges sequentially.

## Step 5 — Write canvas file

Create `MAP_DIR` if missing.
Write JSON to `CANVAS_FILE`.

## Step 6 — Validate

Run both checks:

1. JSON parse:
   - `jq empty "maps/<book-id>/Concept Map.canvas"`
2. File references exist:
   - every `nodes[].file` path exists on disk

Do not consider the task done unless both checks pass.

---

## Output checklist

Before finishing, confirm:

- [ ] `maps/<book-id>/Concept Map.canvas` exists
- [ ] only canonical schema fields used (`nodes`, `edges`)
- [ ] all `file` nodes point to existing markdown files
- [ ] no duplicate node ids
- [ ] no duplicate edge ids
- [ ] edge ids are contiguous (`e1..eN`)
- [ ] JSON validates with `jq`
