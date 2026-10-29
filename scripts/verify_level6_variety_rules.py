"""Check reversible room art, complete hit frames, and exact native silhouettes."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
NEW={'Final_Citadel_Variety_2x.png'}|{f'Final_Citadel_{style}{flash}.png'for style in ['Amber_Ossuary','Crimson_Shaft','Verdant_Crypt']for flash in ['','_Flash']}
def strip(text):
 for part in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_VARIETY '+part+r'\n.*?^# END LEVEL6_VARIETY '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text.replace('<background>Final_Citadel_Amber_Ossuary','<background>Final_Citadel_Interior').replace('<background>Final_Citadel_Crimson_Shaft','<background>Final_Citadel_Interior')
def verify(root,pack):
 previous=json.loads((root/'evidence/0.26.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|NEW
 for name,digest in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_variety';reg=json.loads((art/'registration.json').read_text());nxt=json.loads((root/'art/level6_next/registration.json').read_text())
 patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
 lines=set(text.splitlines());oldlines=set(old.splitlines());defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in text.splitlines()if l.startswith('<condition>')}
 assert all('tileNearby'not in c for c in reg['conditions'])
 assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
 for room,mode in [('9A8B','04'),('9BB7','10'),('9CA7','0C'),('9F3B','10'),('A02B','04'),('A0DF','14')]:
  assert [defs[k]for k in reg['scopes'][room].split('&')]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
 atlas=Image.open(pack/'Final_Citadel_Variety_2x.png').convert('RGBA');assert atlas.size==(512,512)
 assert (pack/'Final_Citadel_Variety_2x.png').read_bytes()==(art/'Final_Citadel_Variety_2x.png').read_bytes()
 images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[65]=='Final_Citadel_Variety_2x.png'
 mapped={};hulls=0
 for e in reg['mappings']:
  assert e['rule']in lines;t=int(e['tile'],16);x,y=e['xy'];cell=atlas.crop((x,y,x+16,y+16));mapped[t,e['palette'],e['scope']]=cell
  if e['kind'].endswith('structural stone'):
   assert np.array_equal(np.array(cell.getchannel('A'))>0,native_hull(patterns[t]));hulls+=1
  else:assert not cell.getchannel('A').getbbox()
 hit=0
 for e in reg['clones']:
  assert e['source_rule']in oldlines and e['rule']in lines
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',')
  assert a[0]==b[0]and a[3:]==b[3:];assert patterns[int(a[1],16)]==patterns[int(b[1],16)]
  if e['kind']=='sentinel hit':hit+=1;assert a[2]==b[2]and b[2]in ['FF102030','FF122232']
 assert hit==3*2*53
 # Whole native terrain units stay exactly assembled from their registered sources.
 checked=0
 for room,color in [('9F3B','amber'),('A02B','red'),('A0DF','green')]:
  scope=reg['scopes'][room];pal={'amber':'0F162738','red':'0F061636','green':'0F0B1B3B'}[color]
  for name,layout in reg['groups'].items():
   im=Image.open(art/f'{color}_{name}.png').convert('RGBA')
   for y,row in enumerate(layout):
    for x,t in enumerate(row):
     if t is None or(t,pal,scope)not in mapped:continue
     assert mapped[t,pal,scope].tobytes()==im.crop((x*16,y*16,x*16+16,y*16+16)).tobytes(),(room,name,hex(t));checked+=1
 for before,after in reg['substitutions']:
  assert before in oldlines and after in lines and before not in lines
  assert ('citadelNext9F3B' in before and 'Amber_Ossuary' in after)or('citadelNextA02B'in before and 'Crimson_Shaft'in after)
 assert len(reg['substitutions'])==len(nxt['backgrounds'])
 expected={(t,phase+suffix)for base in [0x1700,0x1900]for t in range(base,base+256)for phase in ['0F','30','31']for suffix in reg['guard_palettes']}
 for line in reg['backgrounds']:
  head,fields=line[1:].split(']<background>');terms=head.split('&');d=defs[terms[-1]]
  assert '&'.join(terms[:3])==reg['scopes']['A0DF'];assert d[:3]==['tileAtPosition','128','16'];t,pal=int(d[3],16),d[4];expected.remove((t,pal))
  assert fields=='Final_Citadel_Verdant_Crypt'+('_Flash'if pal[:2]!='0F'else'')+'.png,1,0,0,1,0,0'
 assert not expected
 for style in ['Amber_Ossuary','Crimson_Shaft','Verdant_Crypt']:
  im=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGBA'));flash=np.array(Image.open(pack/f'Final_Citadel_{style}_Flash.png').convert('RGBA'))
  assert im.shape==(480,512,4)and np.all(im[:,:,3]==255);assert np.array_equal(im[:,:,:3],flash[:,:,:3])and np.all(flash[:,:,3]==176)
 return dict(prior_assets_exact=len(previous)-2,exact_0260_mapping_recovery=True,native_structural_masks=hulls,
  whole_terrain_cells_checked=checked,complete_sentinel_hit_rules=hit,hit_palettes=['FF102030','FF122232'],
  background_substitutions=len(reg['substitutions']),new_background_guards=len(reg['backgrounds']),
  background_bank_copies=['1700','1900'],new_neighbor_probes=0,original_red_amber_green_room_colors=True)
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.26.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0260-')as directory:
  target=Path(directory)
  for name,digest in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_variety/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
