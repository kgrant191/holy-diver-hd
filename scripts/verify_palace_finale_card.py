"""Prove the final card repair changes only its last visible native fallback."""
from pathlib import Path
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['full','consecutive','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];full,con,after=map(Path,[a.full,a.consecutive,a.after]);info=json.loads((after/'result.json').read_text());assert info['movie_completed']
assert json.loads((after/'installed_pack.json').read_text())==json.loads((r/'evidence/0.24.0-pack-sha256.json').read_text())
old=json.loads((full/'installed_pack.json').read_text());new=json.loads((after/'installed_pack.json').read_text());assert set(old)==set(new) and [k for k in old if old[k]!=new[k]]==['hires.txt']
# The only final delta is the explicitly recorded card clone family and guard.
oldtext=(full/'mesen_home/HdPacks/Holy_Diver_(Tr)/hires.txt').read_text();newtext=(after/'mesen_home/HdPacks/Holy_Diver_(Tr)/hires.txt').read_text()
reg=json.loads((r/'art/level5_finale/registration.json').read_text());delta=[e['rule']for e in reg['card_clones']]+['<condition>palaceFinaleStage6Rendered,tileAtPosition,96,80,1F34,0F213029']
for line in delta:assert newtext.count(line+'\n')==1;newtext=newtext.replace(line+'\n','',1)
assert newtext==oldtext
assert (after/'apu.tsv').read_bytes()==(full/'apu.tsv').read_bytes()
with wave.open(str(full/'full.wav'),'rb')as w:params=w.getparams();pcm=w.readframes(w.getnframes())
with wave.open(str(after/'full.wav'),'rb')as w:assert w.getparams()==params and w.readframes(w.getnframes())==pcm
changed=[];paired=0;ref=np.array(Image.open(full/'frames/015372.png').convert('RGB'))
for path in sorted((after/'frames').glob('*.png')):
 n=int(path.stem);prior=con if(con/'frames'/path.name).exists()else full
 if not(prior/'frames'/path.name).exists():continue
 for kind,ext in [('ram','bin'),('ppu','bin'),('oam','bin'),('view','json')]:assert(after/kind/f'{n:06}.{ext}').read_bytes()==(prior/kind/f'{n:06}.{ext}').read_bytes(),(n,kind)
 oldim=np.array(Image.open(prior/'frames'/path.name).convert('RGB'));im=np.array(Image.open(path).convert('RGB'));paired+=1
 if not np.array_equal(im,oldim):
  assert np.array_equal(im,ref),(n,'changed beyond completed HD card');changed.append(n)
assert changed==[15374],changed
report=dict(movie=info,only_changed_image_frames=changed,paired_native_and_picture_samples=paired,unchanged_asset_files=len(old)-1,only_mapping_delta='61 existing card clones plus one rendered-stage-six guard',full_apu_exact=True,full_pcm_exact=True,pcm_sha256=hashlib.sha256(pcm).hexdigest(),stage6_card_equals_prior_complete_hd_card=True)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
