"""Compare a complete stock-core movie and inspect the actual finale render."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches,variants

def main():
 p=argparse.ArgumentParser()
 for k in ['before','after','out']:p.add_argument('--'+k,required=True)
 p.add_argument('--regression',action='store_true');p.add_argument('--repair',required=True);a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
 infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
 for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
 assert all(i['movie_completed']for i in infos)and infos[1]['stride']==1
 assert json.loads((b/'installed_pack.json').read_text())==json.loads((root/'evidence/0.29.1-pack-sha256.json').read_text())
 assert json.loads((c/'installed_pack.json').read_text())==json.loads((root/'evidence/level6_finale/pre_blackout_fix-pack-sha256.json').read_text())
 repair=Path(a.repair);proof=json.loads((root/'evidence/level6_finale/blackout_repair.json').read_text());assert proof['exact_rule_delta_verified']and proof['all_other_scope_images_exact']
 assert json.loads((repair/'installed_pack.json').read_text())==json.loads((root/'evidence/0.30.0-pack-sha256.json').read_text())
 count=infos[1]['movie_frames'];assert count==(4761 if a.regression else 19215)
 apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
 with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 report=dict(movie=infos[1],native_samples_per_type=count,native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),final_manifest_verified=True,final_scope_replay=proof['final_scope_movie'],full_capture_manifest='pre_blackout_fix-pack-sha256.json',final_scope_proof='blackout_repair.json')
 stats=Counter();rooms=Counter();hits={};badbg=[];ending_bad=[];art=root/'art/level6_finale';reg=json.loads((art/'registration.json').read_text());atlas=Image.open(art/'Final_Citadel_Finale_2x.png').convert('RGBA')
 sources={n:[source(art/(n+'.png'),m)for m in [False,True]]for n in ['joint0','joint1','joint2','joint3','connector','arc0','arc1','arc2','shot','ending_dragon0','ending_dragon1']}
 body={};spec=json.loads((art/'boss_background_variants.json').read_text())
 for name in ['boss1','boss2']:
  bx,by,ex,ey=spec[name]['box'];table={}
  for e in reg['mappings']:
   if e['kind']==name+' body'and e['palette']=='0F063026':
    x,y=e['xy'];table[int(e['tile'],16)&255]=atlas.crop((x,y,x+16,y+16))
  fills={}
  for fill in reg['fill_sources']:
   if fill['form']!=name:continue
   e=next(e for e in reg['mappings']if e['kind']==name+' static interior fill'and e['palette']=='0F063026'and fill['terms'][-1]in e['scope'].split('&'))
   x,y=e['xy'];fills[fill['x'],fill['y']]=atlas.crop((x,y,x+16,y+16))
  body[name]=(table,fills)
 pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';backgrounds={}
 for room,stem in [('A49F','Ascent'),('A553','Chamber'),('A58F','Void')]:
  entries=[]
  stems=['Chamber','Void']if room=='A58F'else[stem]
  for st in stems:
   for suffix in ['', '_fade1','_fade2','_fade3']:
    f=pack/('Final_Citadel_Last_'+st+suffix+'.png')
    if f.exists():entries.extend(variants(np.array(Image.open(f).convert('RGB'))[::8,::8]))
   f=pack/('Final_Citadel_Last_'+st+'.png');rgb=np.array(Image.open(f).convert('RGB'))[::8,::8]
   for color in [[255,254,255],[194,223,255]]:entries.extend(variants((rgb.astype(np.uint32)*176//255+np.array(color)*80//256).astype(np.uint8)))
  backgrounds[room]=entries
 menu_corner=np.array(Image.open(b/'frames/000010.png').convert('RGB'))[32:48,2:24]
 source_ids={name:{t&255 for t,x,y in layout}for name,layout in reg['components'].items()}
 source_ids.update({f'ending_dragon{i}':{t for t,x,y in layout}for i,layout in enumerate(reg['ending_layouts'])})
 previous=None
 for n in range(1,count+1):
  if n%3000==0:print('Verified through frame',n-1,flush=True)
  data={}
  for kind in ['ram','ppu','oam','view']:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/name).read_bytes();assert raw==(b/kind/name).read_bytes(),(n,kind);data[kind]=json.loads(raw)if kind=='view'else raw
  fs=[b/'frames'/f'{n:06}.png',(repair if not a.regression and 7400<=n<=9200 else c)/'frames'/f'{n:06}.png']
  if not all(f.stat().st_size for f in fs):assert fs[0].stat().st_size==fs[1].stat().st_size;stats['empty_initial']+=1;previous=data;continue
  old,im=[np.array(Image.open(f).convert('RGB'))for f in fs];diff=np.any(old!=im,2);stats['changed'if diff.any()else'identical']+=1
  if a.regression:
   assert not diff.any(),n;assert int.from_bytes(data['ram'][0x78:0x7a],'little')not in [0xa58f,0xb01c];previous=data;continue
  room=f'{int.from_bytes(data["ram"][0x78:0x7a],"little"):04X}';prevroom=f'{int.from_bytes((previous or data)["ram"][0x78:0x7a],"little"):04X}';rooms[room]+=1
  if not old.any():assert not im.any(),(n,'blackout');stats['blackouts_exact']+=1;previous=data;continue
  # Fixed menu frame ornaments identify visible menus even during their redraw.
  if np.array_equal(old[32:48,2:24],im[32:48,2:24])and np.array_equal(old[32:48,2:24],menu_corner):
   assert not diff.any(),(n,'menu');stats['menus_exact']+=1;previous=data;continue
  if room in backgrounds and room==prevroom:
   sampled=im[::8,::8];best=0
   for bg in backgrounds[room]:
    best=max(best,int(np.all(sampled==bg,2).sum()))
    if best>=40:break
   if best>=40:stats['backdrop_visible_'+room]+=1
   else:badbg.append(dict(frame=n,room=room,matching_sample_points=best))
  if room=='B01C'and prevroom=='B01C':
   mask=np.zeros((480,512),bool)
   for d in [previous or data,data]:
    for j in range(0,256,4):
     y,t,attr,x=d['oam'][j:j+4]
     if y<239 and 0xcd<=t<=0xeb:mask[(y+1)*2:min(480,(y+9)*2),x*2:min(512,x*2+16)]=True
   outside=diff&~mask
   if outside.any():ending_bad.append(dict(frame=n,pixels=int(outside.sum())))
   stats['ending_frames_with_only_dragon_changes']+=1
  if n<10050:
   active_ids={d['oam'][j+1]for d in [previous or data,data]for j in range(0,256,4)if d['oam'][j]<239}
   for name,ss in sources.items():
    if name in hits:continue
    if name.startswith('ending')!=(room=='B01C'):continue
    if not name.startswith('ending')and room not in ['A553','A58F']:continue
    if not source_ids[name]<=active_ids:continue
    for mirror,item in enumerate(ss):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirror),positions=found);break
  name='boss1'if room=='A553'else'boss2'if room=='A58F'else None
  if name and name not in hits:
   bx,by,ex,ey=spec[name]['box'];table,fills=body[name]
   # Native moving joints, attacks, player and HUD legitimately obscure the
   # body. Verify every remaining painted body pixel, using only native OAM
   # cell bounds from the current/preceding submitted frame as occlusions.
   occluded=np.zeros((480,512),bool)
   for d in [previous or data,data]:
    for j in range(0,256,4):
     y,t,attr,x=d['oam'][j:j+4]
     if y<239:occluded[(y+1)*2:min(480,(y+9)*2),x*2:min(512,x*2+16)]=True
   for d in [previous or data,data]:
    pp=d['ppu'];v=d['view'];vv=v['vram'];sx=(vv&31)*8+v['xscroll'];sy=((vv>>5)&31)*8+((vv>>12)&7);intro=name=='boss2'and pp[0x202d]==0xc5
    expected=Image.new('RGBA',(512,480))
    for y in range(by,ey,16):
     for x in range(bx,ex,16):
      ny=y//2-(64 if intro else 0);t=pp[0x2000+ny//8*32+x//16];cell=table.get(t)
      if cell is None and t==0:cell=fills.get((x,y))
      if cell is not None:expected.paste(cell,(((x//2-sx)%256)*2,((ny-sy)%240)*2))
    arr=np.array(expected);mask=(arr[:,:,3]==255)&~occluded
    if mask.sum()>15000 and np.array_equal(im[mask],arr[:,:,:3][mask]):
     hits[name]=dict(frame=n,unoccluded_opaque_pixels=int(mask.sum()),complete_native_layout=True,native_OAM_occlusion_only=True);break
  previous=data
 report['ending_second_pose_whole_visible']='ending_dragon1'in hits
 report['ending_second_pose_note']='Both pose mappings and shared tail are statically verified. The second pose has native behind-background priority during scrolling text; do not force it forward to manufacture a whole-source match.'
 report.update(images=dict(stats),rooms=dict(rooms),live_whole_source_matches=hits,source_names_not_observed=sorted((set(sources)|{'boss1','boss2'})-set(hits)),backdrop_exceptions=badbg,ending_changes_outside_native_dragon_bounds=ending_bad,earlier_images_exact=a.regression)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 assert not ending_bad,ending_bad[:10]
 if not a.regression:assert {'boss1','boss2','ending_dragon0'}<=set(hits)

if __name__=='__main__':main()
