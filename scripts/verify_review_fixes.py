"""Compare native-input replays, audio and the retained rolling animation."""
from pathlib import Path
import argparse, hashlib, json, struct
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
p.add_argument('--root',required=True)
p.add_argument('--out',required=True)
a=p.parse_args();work=Path(a.root)
result={'emulator':'MesenCE 2.2.1','ram_writes':False,'cases':{},'visual_scope':'crouch attacks and standing ghoul only'}

def pcm(path):
 data=path.read_bytes()
 assert data[:4]==b'RIFF' and data[8:16]==b'WAVEfmt ' and data[36:40]==b'data'
 assert struct.unpack('<IHHIIHH',data[16:36])==(16,1,2,48000,192000,4,16)
 return data[44:]

for case in ['normal','twin','state1','state2','state3']:
 enemy=case.startswith('state')
 before=work/('ghoul_before' if enemy else 'before')/case
 after=work/('ghoul_after' if enemy else 'after')/case
 frames=720 if enemy else 240
 assert (before/'completed.txt').read_text()==(after/'completed.txt').read_text()==str(frames)
 assert (before/'input.json').read_bytes()==(after/'input.json').read_bytes()
 report={'frames':frames,**json.loads((after/'input.json').read_text())}
 for ext in ['ram','ppu','oam']:
  paths=sorted((before/'dumps').glob('*.'+ext))
  assert len(paths)==(360 if enemy else 240)
  assert all(path.read_bytes()==(after/'dumps'/path.name).read_bytes() for path in paths),(case,ext)
  report[ext+'_identical_samples']=len(paths)
 apu=(before/'apu.tsv').read_bytes()
 assert apu==(after/'apu.tsv').read_bytes()
 report['apu_sha256']=hashlib.sha256(apu).hexdigest()
 bp,ap=pcm(before/'full.wav'),pcm(after/'full.wav');common=min(len(bp),len(ap))
 assert common>0 and bp[:common]==ap[:common]
 assert abs(len(bp)-len(ap))<=3200,(case,'audio capture truncated; rerun this case')
 report.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(ap))
 identical,changed,rolling=0,0,0
 observed=set()
 for path in sorted((after/'frames').glob('*.png')):
  bpath=before/'frames'/path.name
  assert bpath.exists()
  if not path.stat().st_size or not bpath.stat().st_size:
   assert int(path.stem)==1 and path.read_bytes()==bpath.read_bytes()
   continue  # Mesen's first screenshot immediately after load is empty.
  b=np.array(Image.open(bpath).convert('RGBA'));n=np.array(Image.open(path).convert('RGBA'))
  delta=np.any(b!=n,axis=2)
  if not delta.any():identical+=1
  else:changed+=1
  frame=int(path.stem);allowed=np.zeros(delta.shape,dtype=bool);rolling_seen=False;standing_seen=False
  for sample in [frame-(2 if enemy else 1),frame]:
   op=after/'dumps'/f'{sample:04}.oam'
   if not op.exists():continue
   data=op.read_bytes();sprites=[tuple(data[k:k+4]) for k in range(0,256,4)]
   if enemy:
    group=[(y,t,attr,x)for y,t,attr,x in sprites if y<239 and attr&3==1 and 0x94<=t<=0xab]
    standing=any(0x96<=t<=0x9d for y,t,attr,x in group)
    standing_seen|=standing
    rolling_seen|=bool(group) and not standing
    affected=group if standing else []
   else:
    affected=[(y,t,attr,x)for y,t,attr,x in sprites if y<239 and attr&3==3 and t<0x40]
    tiles={t for y,t,attr,x in affected}
    phase='windup' if 0x33 in tiles else ('release' if {0x2c,0x2f}<=tiles else None)
    if phase:
     ppu=(after/'dumps'/f'{sample:04}.ppu').read_bytes()
     palette='FF'+ppu[0x3f1d:0x3f20].hex().upper()
     observed.add((phase,'left' if any(attr&0x40 for y,t,attr,x in affected) else 'right',palette))
    else:affected=[]
   for y,t,attr,x in affected:
    # Native screenshot may reflect the preceding sampled OAM, hence union.
    allowed[max(0,y*2):min(480,(y+10)*2),max(0,x*2-2):min(512,(x+9)*2)]=True
  assert not np.any(delta & ~allowed),(case,frame,'changed outside requested sprites')
  if enemy and rolling_seen and not standing_seen:
   assert not delta.any(),(case,frame,'rolling image changed')
   rolling+=1
 if not enemy:
  palette='FF300036' if case=='normal' else 'FF221136'
  assert observed=={(phase,direction,palette)for phase in ['windup','release']for direction in ['left','right']},observed
 report.update(identical_screenshots=identical,changed_screenshots=changed,rolling_screenshots_identical=rolling)
 if observed:report['observed_crouch_attacks']=[list(v)for v in sorted(observed)]
 result['cases'][case]=report
result['emulated_frames_per_build']=2640
result['paired_samples_per_memory_type']=1560
out=Path(a.out);out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
