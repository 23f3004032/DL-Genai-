# Script to remove metadata.widgets from a Jupyter notebook file
# Usage: python3 scripts/fix_notebook_widgets.py "Week 3/CNN_Fundamentals.ipynb"

import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python fix_notebook_widgets.py <notebook-path>")
    sys.exit(1)

nb_path = Path(sys.argv[1])
if not nb_path.exists():
    print(f"Notebook not found: {nb_path}")
    sys.exit(2)

backup = nb_path.with_suffix(nb_path.suffix + '.bak')
print(f"Creating backup: {backup}")
backup.write_bytes(nb_path.read_bytes())

nb = json.loads(nb_path.read_text(encoding='utf-8'))
changed = False

# Remove metadata.widgets from cells
for cell in nb.get('cells', []):
    meta = cell.get('metadata')
    if isinstance(meta, dict) and 'widgets' in meta:
        print(f"Removing widgets metadata from cell")
        del meta['widgets']
        changed = True

# Also remove top-level nb metadata.widgets if present
meta = nb.get('metadata')
if isinstance(meta, dict) and 'widgets' in meta:
    print("Removing widgets from notebook metadata")
    del meta['widgets']
    changed = True

if changed:
    nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f"Updated notebook written to {nb_path}")
else:
    print("No widgets metadata found; no changes made.")
