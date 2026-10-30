"""Check the complete violet ledge, right wall stop and slow left walk-off."""
from pathlib import Path
import argparse,json,hashlib,wave,tempfile
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
from verify_level6_opening_replay import source,matches
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][key]==infos[1][key]
assert all(i['movie_completed']and i['movie_frames']==1930 and i['captured_frames']==331 for i in infos)
for d,version in [(b,'0.30.1'),(c,'0.31.0')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
data={k:{}for k in ['ram','ppu','oam','view']};frames=list(range(1600,1931))
for n in frames:
    for kind in data:
        name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/name).read_bytes();assert raw==(b/kind/name).read_bytes(),(n,kind);data[kind][n]=raw
assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
pos={n:[int.from_bytes(data['ram'][n][o:o+2],'little')for o in [0x74,0x76]]for n in frames};states={n:data['ram'][n][0x300]for n in frames}
assert all(pos[n]==[489,96]and states[n]==0 for n in range(1692,1721))
assert all(pos[n][1]==96 and pos[n+1][0]-pos[n][0]in [0,-1]for n in range(1721,1827))
assert pos[1827]==[409,96]and pos[1828]==[408,96]and states[1828]==2
assert next(n for n in range(1828,1840)if pos[n][1]>96)==1832
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';reg=json.loads((root/'art/level6_missed/registration.json').read_text());images=[l[5:]for l in(pack/'hires.txt').read_text().splitlines()if l.startswith('<img>')]
entries={}
for e in reg['mappings']+reg['clones']:
    if e['room']=='9D5B':
        f=e['rule'].split('<tile>')[1].split(',');entries.setdefault((int(f[1],16),f[2]),f)
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_missed/native_patterns.json').read_text()).items()}
ppu=data['ppu'][1700];whole=Image.new('RGBA',(192,256));mask=Image.new('L',whole.size);layout=[];cache={}
for y in range(16):
    row=[]
    for x in range(12):
        tx,ty=20+x,14+y;nt=0x2400;t=0x1700+ppu[nt+ty*32+tx];at=ppu[nt+960+ty//4*8+tx//4];pi=(at>>((ty%4)//2*4+(tx%4)//2*2))&3
        pal=(bytes([ppu[0x3f00]])+ppu[0x3f01+4*pi:0x3f04+4*pi]).hex().upper();row.append([f'{t:04X}',pal]);f=entries[t,pal];idx,cx,cy=int(f[0]),int(f[3]),int(f[4])
        if idx not in cache:cache[idx]=Image.open(pack/images[idx]).convert('RGBA')
        whole.paste(cache[idx].crop((cx,cy,cx+16,cy+16)),(x*16,y*16));assert pal in ['0F051433','0F011121']
        if pal=='0F051433':mask.paste(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255),(x*16,y*16))
    layout.append(row)
assert np.array_equal(np.array(whole.getchannel('A')),np.array(mask))
hits=[]
with tempfile.TemporaryDirectory()as temp:
    path=Path(temp)/'ledge.png';whole.save(path);item=source(path)
    for n in range(1692,1833):
        im=np.array(Image.open(c/f'frames/{n:06}.png').convert('RGB'));found=matches(im,item)
        if found:hits.append(dict(frame=n,positions=found))
assert len(hits)>80,len(hits)
report=dict(movie=infos[1],native_samples_per_type=331,native_exact=True,apu_exact=True,pcm_exact=True,pcm_sha256=hashlib.sha256(pcm).hexdigest(),controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True,right_stop=dict(frames=[1692,1720],world_position=[489,96]),slow_left=[1721,1827],platform_native_world_bounds=dict(left=416,right_exclusive=496,top=112),native_fall_start=dict(frame=1828,world_position=pos[1828]),native_first_descent=dict(frame=1832,world_position=pos[1832]),complete_platform_dimensions=[192,256],native_platform_layout=layout,whole_platform_native_alpha_exact=True,complete_platform_source_matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['native_platform_layout','complete_platform_source_matches']},indent=2));print('Complete ledge matches:',len(hits))
