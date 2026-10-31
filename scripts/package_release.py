"""Package the verified Actions artifact with one extraction to install."""
from pathlib import Path
import argparse,hashlib,json,zipfile
p=argparse.ArgumentParser()
p.add_argument('--pack',required=True)
p.add_argument('--out',required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];pack=Path(a.pack)
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
actual={f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in pack.iterdir()if f.is_file()}
assert actual==expected,'Downloaded artifact must match every expected installation byte'
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
    for name in sorted(expected):z.writestr(name,(pack/name).read_bytes())
with zipfile.ZipFile(out)as z:
    assert z.testzip()is None
    assert set(z.namelist())==set(expected)and len(z.namelist())==len(expected)
    assert all('/'not in n and '\\'not in n for n in z.namelist())
    assert {n:hashlib.sha256(z.read(n)).hexdigest()for n in z.namelist()}==expected
print('Release ZIP verified:',out,hashlib.sha256(out.read_bytes()).hexdigest())
