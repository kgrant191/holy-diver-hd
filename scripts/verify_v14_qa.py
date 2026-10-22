from pathlib import Path
import argparse,json,wave,hashlib
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args();result={}
for case in ['bracelet','normal','twin']:
 before=Path(a.before)/case;after=Path(a.after)/case;r={}
 assert(before/'completed.txt').read_text()==(after/'completed.txt').read_text()=='360'
 for kind in ['ram','ppu','oam']:
  files=sorted((before/'dumps').glob('*.'+kind));assert len(files)==360
  assert all(f.read_bytes()==(after/'dumps'/f.name).read_bytes()for f in files),case+' '+kind
  r[kind+'_identical_frames']=len(files)
 for name in ['apu.tsv','commands.tsv']:
  b=(before/name).read_bytes();assert b==(after/name).read_bytes(),case+' '+name;r[name]={'identical':True,'sha256':hashlib.sha256(b).hexdigest()}
 with wave.open(str(before/'full.wav'),'rb')as w:b=w.readframes(w.getnframes());bp=w.getparams()
 with wave.open(str(after/'full.wav'),'rb')as w:c=w.readframes(w.getnframes());cp=w.getparams()
 n=min(len(b),len(c));assert b[:n]==c[:n],case+' PCM';r['audio']={'matching_common_pcm_bytes':n,'before_bytes':len(b),'after_bytes':len(c),'sample_rate':bp.framerate,'channels':bp.nchannels}
 images=[f for f in sorted((before/'frames').glob('*.png'))if f.stat().st_size];r['identical_render_frames']=sum(f.read_bytes()==(after/'frames'/f.name).read_bytes()for f in images);r['render_frames']=len(images)
 zero=[int(f.stem)for f in(after/'dumps').glob('*.ram')if f.read_bytes()[0x440]==0];r['native_health_zero_range']=[min(zero),max(zero)]if zero else None
 result[case]=r
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
