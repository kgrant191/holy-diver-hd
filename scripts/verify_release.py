"""Verify every installed file against the reviewed expected build manifest."""
from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parents[1]
pack = root / 'build/Holy_Diver_(Tr)'
version = (root / 'VERSION').read_text().strip()
expected = json.loads((root / 'evidence/approved-pack-sha256.json').read_text())
actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in pack.iterdir() if p.is_file()}
missing = sorted(expected.keys() - actual.keys())
extra = sorted(actual.keys() - expected.keys())
changed = sorted(k for k in expected.keys() & actual.keys() if expected[k] != actual[k])
if missing or extra or changed:
    raise SystemExit(json.dumps({'missing': missing, 'extra': extra, 'changed': changed}, indent=2))
print(f'Expected {version}: all {len(expected)} pack files match SHA-256 exactly.')
