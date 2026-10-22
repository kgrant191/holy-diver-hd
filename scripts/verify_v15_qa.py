from pathlib import Path
from PIL import Image,ImageChops
import argparse,json,wave,hashlib
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args();result={}
for case,end in [('title',1800),('normal',720),('twin',720),('enemy',360),('menu',180)]:
 b=Path(a.before)/case;c=Path(a.after)/case;r={}
 assert(b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(end)
 for ext in ['ram','ppu','oam']:
  files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==end//2
  assert all(f.read_bytes()==(c/'dumps'/f.name).read_bytes()for f in files),case+' '+ext
  r[ext+'_identical_frames']=len(files)
 for name in ['apu.tsv','commands.tsv']:
  data=(b/name).read_bytes();assert data==(c/name).read_bytes(),case+' '+name;r[name]={'identical':True,'sha256':hashlib.sha256(data).hexdigest()}
 with wave.open(str(b/'full.wav'),'rb')as w:audio1=w.readframes(w.getnframes());rate=w.getframerate()
 with wave.open(str(c/'full.wav'),'rb')as w:audio2=w.readframes(w.getnframes())
 size=min(len(audio1),len(audio2));assert audio1[:size]==audio2[:size],case+' PCM'
 r['audio']={'matching_common_pcm_bytes':size,'before_bytes':len(audio1),'after_bytes':len(audio2),'sample_rate':rate}
 changed=[];same=[]
 for f in sorted((b/'frames').glob('*.png')):
  if f.read_bytes()==(c/'frames'/f.name).read_bytes():same.append(int(f.stem))
  else:changed.append(int(f.stem))
 r['identical_render_frames']=len(same);r['changed_render_frames']=len(changed);r['changed_frames']=changed
 if case=='title':
  assert all(548<=f<=746 or 1448<=f<=1646 for f in changed),changed
  assert (c/'frames/0580.png').read_bytes()==(c/'frames/1480.png').read_bytes(),'reset stage card differs'
 if case=='menu':assert all(f>=140 for f in changed),'approved pause-menu changed before death after resume'
 if case=='menu':r['approved_pause_frames_identical']=True
 result[case]=r
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:{kk:vv for kk,vv in v.items()if kk!='changed_frames'}for k,v in result.items()},indent=2))
