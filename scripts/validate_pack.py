"""Validate pack references, conditional ordering, tile bounds and unchanged scope."""
from pathlib import Path
from PIL import Image
import numpy as np
import sys,re,json,hashlib
pack=Path(sys.argv[1]);content=(pack/'hires.txt').read_text();lines=content.splitlines();imgs=[];sizes={};conditions={'hmirror','vmirror','bgpriority'};counts={'tile':0,'background':0,'condition':0}
sha='FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC'
if len(sys.argv)>2:assert hashlib.sha1(Path(sys.argv[2]).read_bytes()).hexdigest().upper()==sha
assert '<supportedRom>'+sha in lines
assert '<scale>2' in lines
for line in lines:
 m=re.match(r'(?:\[([^]]+)\])?<([^>]+)>(.*)',line)
 if not m:continue
 prefix,tag,value=m.groups()
 if prefix:assert all(n.lstrip('!') in conditions for n in prefix.split('&')),line
 assert tag not in {'bgm','sfx','album','bgmloop'},tag
 if tag=='patch':
  assert value=='Entrance_SFX_Priority.ips,'+sha
  patch=(pack/'Entrance_SFX_Priority.ips').read_bytes()
  manifest=json.loads((Path(__file__).resolve().parents[1]/'audio_priority_patch.json').read_text())
  expected=bytearray(b'PATCH')
  for e in manifest['edits']:
   data=bytes.fromhex(e['after_hex']);expected+=int(e['file_offset_hex'],16).to_bytes(3,'big')+len(data).to_bytes(2,'big')+data
  expected+=b'EOF';assert patch==expected
 if tag=='condition':
  name=value.split(',')[0];assert name not in conditions;conditions.add(name);counts[tag]+=1
 if tag=='img':
  assert value not in imgs;imgs.append(value);assert(pack/value).is_file();sizes[value]=Image.open(pack/value).size
 if tag=='background':assert(pack/value.split(',')[0]).is_file();counts[tag]+=1
 if tag=='tile':
  p=value.split(',');idx=int(p[0]);x=int(p[3]);y=int(p[4]);assert 0<=idx<len(imgs);w,h=sizes[imgs[idx]]
  assert x>=0 and y>=0 and x+16<=w and y+16<=h,line
  counts[tag]+=1
if '# BEGIN PALACE_ONE_UP MAPPINGS' in content:
 from verify_palace_one_up_rules import verify, legacy_projection
 root=Path(__file__).resolve().parents[1]
 report=verify(root,pack)
 legacy_projection(root,pack)
 print(json.dumps({'palace_one_up':report,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'all_historical_validators_passed':True}))
 raise SystemExit(0)
if '# BEGIN PALACE_FLASH CONDITIONS' in content:
 from verify_palace_flash_rules import verify, legacy_projection
 root=Path(__file__).resolve().parents[1]
 report=verify(root,pack)
 legacy_projection(root,pack)
 print(json.dumps({'palace_flash':report,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'all_historical_validators_passed':True}))
 raise SystemExit(0)
if '# BEGIN PALACE_NEXT IMAGES' in content:
 from verify_palace_next_rules import verify, legacy_projection
 root=Path(__file__).resolve().parents[1]
 report=verify(root,pack)
 legacy_projection(root,pack)
 print(json.dumps({'palace_next':report,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'all_historical_validators_passed':True}))
 raise SystemExit(0)
if '# BEGIN PALACE_REPAIR IMAGES' in content:
 from verify_palace_repair_rules import verify, legacy_projection
 root=Path(__file__).resolve().parents[1]
 report=verify(root,pack)
 legacy_projection(root,pack)
 print(json.dumps({'palace_repair':report,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'all_historical_validators_passed':True}))
 raise SystemExit(0)
if '# BEGIN DEMONIC_PALACE IMAGES' in content:
 from verify_level5_rules import verify, validate_legacy_projection
 root=Path(__file__).resolve().parents[1]
 report=verify(root,pack)
 validate_legacy_projection(root,pack)
 print(json.dumps({'level5':report,'atlas_count':len(imgs),**counts,'references_and_bounds_valid':True,'all_historical_validators_passed':True}))
 raise SystemExit(0)
assert len(imgs)==57
# Preserve approved assets outside the requested title/ledge, arm and crouch repairs.
root=Path(__file__).resolve().parents[1]
total_counts=counts.copy()
from verify_background_rules import verify as verify_background_rules, strip as strip_background_continuity
background_report=verify_background_rules(root,pack)
content=strip_background_continuity(content)
counts['condition']-=background_report['conditions'];counts['background']-=background_report['background_rules']
from verify_boss_entry_rules import verify as verify_boss_entry_rules, strip as strip_boss_entry
boss_entry_report=verify_boss_entry_rules(root,pack,content)
content=strip_boss_entry(content)
counts['tile']-=boss_entry_report['tile_rules']
from verify_cleanup_rules import verify as verify_cleanup_rules, strip as strip_cleanup, ADDED as cleanup_files
cleanup_report=verify_cleanup_rules(root,pack,content)
content=strip_cleanup(content)
counts['tile']-=cleanup_report['tile_rules'];counts['condition']-=cleanup_report['conditions']
cleanup_inventory={p.name for p in pack.iterdir()if p.is_file()}-cleanup_files
from verify_transition_rules import verify as verify_transition_rules, strip as strip_transition, ADDED as transition_files
transition_report=verify_transition_rules(root,pack,content,cleanup_inventory)
content=strip_transition(content)
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=transition_report[field]
transition_inventory=cleanup_inventory-transition_files
from verify_finish_rules import verify as verify_finish_rules
finish_report=verify_finish_rules(root,pack,content,transition_inventory)
for section in ['IMAGES','CONDITIONS','MAPPINGS','EARLY_STAIRS']:
 content,n=re.subn(r'^# BEGIN TEMPLE_FINISH '+section+r'\n.*?^# END TEMPLE_FINISH '+section+r'\n','',content,flags=re.M|re.S);assert n==1
counts['tile']-=finish_report['tile_rules'];counts['condition']-=finish_report['conditions']
legacy_inventory=transition_inventory-{'Golden_Temple_Finish_2x.png'}
finale=json.loads((root/'art/level4_finale/registration.json').read_text())
assert not finale['native_gameplay_modified'] and not finale['prior_artwork_modified']
from verify_finale_rules import verify as verify_finale_rules
assert verify_finale_rules(root)['unsafe_reads']==0
for m in finale['mappings']:assert m['rule']in lines
for m in finale['clones']:assert m['rule']in lines and m['source_rule']in lines
for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
 content,n=re.subn(r'^# BEGIN TEMPLE_FINALE '+section+r'\n.*?^# END TEMPLE_FINALE '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_finale=json.loads((root/'evidence/0.19.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_finale['hires.txt']
assert legacy_inventory-{'Golden_Temple_Finale_2x.png'}==set(previous_finale)
for name,digest in previous_finale.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=finale[field]
residue_rules=[f'[staffArenaMode&staffArenaLo&staffArenaHi]<tile>50,0DF8,{pal},0,0,1,N'for pal in ['0F073703','31073703']]
assert all(line in lines for line in residue_rules)
assert Image.open(pack/'Golden_Temple_Courtyard_2x.png').convert('RGBA').crop((0,0,16,16)).getchannel('A').getbbox()is None
content,n=re.subn(r'^# BEGIN TEMPLE_RESIDUE MAPPINGS\n.*?^# END TEMPLE_RESIDUE MAPPINGS\n','',content,flags=re.M|re.S);assert n==1
residue_prior=json.loads((root/'evidence/0.19.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==residue_prior['hires.txt']
assert legacy_inventory-{'Golden_Temple_Finale_2x.png'}==set(residue_prior)
for name,digest in residue_prior.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
counts['tile']-=len(residue_rules)
dragon=json.loads((root/'art/level4_dragon/registration.json').read_text())
assert not dragon['native_gameplay_modified'] and not dragon['prior_artwork_modified']
assert dragon['dragon_fit']['clipped_pixels']==0 and dragon['dragon_fit']['shared_native_cells_exact']
from verify_dragon_neighbor_rules import verify as verify_dragon_neighbors
assert verify_dragon_neighbors(root)['unsafe_reads']==0
dp=json.loads((root/'art/level4_dragon/native_patterns.json').read_text())
for source,targets in json.loads((root/'art/level4_dragon/native_aliases.json').read_text()).items():
 for target in targets:assert dp[source]==dp[target]
for m in dragon['mappings']:assert m['rule']in lines
for m in dragon['removed']:
 assert m['source_rule']in lines and lines.index(m['rule'])<lines.index(m['source_rule'])
 assert int(m['rule'].split('<tile>')[1].split(',')[1],16)&255 not in range(0x78,0x88)
for m in dragon['clones']:assert m['rule']in lines and m['source_rule']in lines
item=np.array(Image.open(root/'art/level4_dragon/staff.png'));menu=np.array(Image.open(root/'art/level4_dragon/staff_menu.png'))
assert np.array_equal(menu[:,8:24],item)
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 content,n=re.subn(r'^# BEGIN TEMPLE_DRAGON '+section+r'\n.*?^# END TEMPLE_DRAGON '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_dragon=json.loads((root/'evidence/0.18.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_dragon['hires.txt']
assert legacy_inventory-{'Golden_Temple_Dragon_2x.png','Golden_Temple_Finale_2x.png'}==set(previous_dragon)
for name,digest in previous_dragon.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=dragon[field]
staff=json.loads((root/'art/level4_staff/registration.json').read_text())
assert not staff['native_gameplay_modified'] and not staff['prior_artwork_modified']
legacy_files=legacy_inventory-{'Golden_Temple_Staff_2x.png','Golden_Temple_Dragon_2x.png','Golden_Temple_Finale_2x.png'}
staff_patterns=json.loads((root/'art/level4_staff/native_patterns.json').read_text())
for m in staff['mappings']:
 assert m['rule'] in lines
for m in staff['clones']:
 assert m['rule'] in lines and m['source_rule'] in lines
for m in staff['actor_aliases']:
 assert staff_patterns[m['source']]==staff_patterns[m['target']]
 before=m['source_rule'].split('<tile>')[1].split(',');after=m['rule'].split('<tile>')[1].split(',')
 assert before[:1]+before[2:]==after[:1]+after[2:]
assert staff_patterns['0CF8']==staff_patterns['0A94']
for t in range(256):assert staff_patterns[f'{0xb00+t:04X}']==staff_patterns[f'{0xd00+t:04X}']
for m in staff['clones']:
 if m['kind']!='outdoor scenery reuse':continue
 before=m['source_rule'].split('<tile>')[1].split(',');after=m['rule'].split('<tile>')[1].split(',')
 assert int(after[1],16)==int(before[1],16)+0x200
 assert before[:1]+before[2:]==after[:1]+after[2:]
for side in ['Left','Right']:
 expected=f'<condition>staffHallStatue{side},tileNearby,'+('-8'if side=='Left'else'8')+',0,'+('0BE3'if side=='Left'else'0BE4')+',0F172737'
 assert expected in lines
 for m in staff['clones']:
  if f'&staffHallStatue{side}]'in m['rule']:
   assert f'&courtyardStatue{side}Safe&staffHallStatue{side}]'in m['rule']
assert staff['sentinel_fit']['clipped_pixels']==0 and staff['sentinel_fit']['shared_native_cells_exact']
from verify_staff_neighbor_rules import verify as verify_staff_neighbors
assert verify_staff_neighbors(root)['unsafe_reads']==0
item=np.array(Image.open(root/'art/level4_staff/staff.png').convert('RGBA'))
menu=np.array(Image.open(root/'art/level4_staff/staff_menu.png').convert('RGBA'))
assert np.array_equal(menu[:,8:24],item)
for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
 content,n=re.subn(r'^# BEGIN TEMPLE_STAFF '+section+r'\n.*?^# END TEMPLE_STAFF '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_staff=json.loads((root/'evidence/0.17.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_staff['hires.txt'],'0.17.0 mappings changed'
assert legacy_files==set(previous_staff)
for name,digest in previous_staff.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior asset changed'
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=staff[field]
courtyard=json.loads((root/'art/level4_courtyard/registration.json').read_text())
source_scopes=json.loads((root/'art/level4/registration.json').read_text())['scopes']
assert not courtyard['native_gameplay_modified'] and not courtyard['prior_artwork_modified']
from verify_courtyard_neighbor_rules import verify as verify_courtyard_neighbors
assert verify_courtyard_neighbors(root)['unsafe_reads']==0
alias_patterns=json.loads((root/'art/level4_courtyard/native_patterns.json').read_text())
for source,targets in json.loads((root/'art/level4_courtyard/item_enemy_aliases.json').read_text()).items():
 for target in targets:assert alias_patterns[source]==alias_patterns[target]
for m in courtyard['mappings']:
 assert m['rule'] in lines
for m in courtyard['clones']:
 assert m['rule'] in lines and m['source_rule'] in lines
 source=m['source_rule'];oldscope=source_scopes[m['source_room']]
 expected=source.replace(oldscope,courtyard['scopes'][m['room']])
 head,tail=expected.split(']',1)
 renames=courtyard['rename_sets'][m['rename_key']]
 expected='['+'&'.join(('!'if term.startswith('!')else '')+renames.get(term.lstrip('!'),term.lstrip('!'))for term in head[1:].split('&'))+']'+tail
 assert expected==m['rule'],'Final repaired source rule was not preserved'
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 content,n=re.subn(r'^# BEGIN TEMPLE_COURTYARD '+section+r'\n.*?^# END TEMPLE_COURTYARD '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_courtyard=json.loads((root/'evidence/0.16.3-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_courtyard['hires.txt'],'Approved 0.16.3 mappings changed'
for name,digest in previous_courtyard.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved asset changed'
assert legacy_files-{'Golden_Temple_Courtyard_2x.png'}==set(previous_courtyard)
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=courtyard[field]
stairs=json.loads((root/'art/level4_stairs/registration.json').read_text())
assert not stairs['native_gameplay_modified'] and not stairs['prior_artwork_modified']
stair_image=Image.open(pack/'Golden_Temple_Stairs_2x.png').convert('RGBA')
assert stair_image.size==(32,32)
assert np.array_equal(np.array(stair_image.getchannel('A')),np.array(stairs['alpha'],dtype=np.uint8))
source=Image.open(root/stairs['source']).convert('RGBA')
assert np.array_equal(np.array(stair_image)[:,:,:3],np.array(source)[:,:,:3])
for m in stairs['mappings']:
 assert int(m['tile'],16)in range(0xb7c,0xb80) and m['rule'] in lines
 assert lines.index(m['rule'])<lines.index(m['overridden_rule'])
 assert m['scope'].startswith(('templeA865Mode&','templeAA09Mode&','templeAA81Mode&'))
for section in ['IMAGES','MAPPINGS']:
 content,n=re.subn(r'^# BEGIN TEMPLE_STAIRS '+section+r'\n.*?^# END TEMPLE_STAIRS '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_stairs=json.loads((root/'evidence/0.16.2-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_stairs['hires.txt'],'0.16.2 mappings changed'
for name,digest in previous_stairs.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior asset changed'
assert legacy_files-{'Golden_Temple_Courtyard_2x.png','Golden_Temple_Stairs_2x.png'}==set(previous_stairs)
counts['tile']-=stairs['tile_rules']
repairs=json.loads((root/'art/level4_repairs/registration.json').read_text())
from verify_temple_neighbor_rules import verify as verify_neighbor_rules
assert verify_neighbor_rules(root)['unsafe_evaluations']==0
pickup_patterns=json.loads((root/'art/level4_repairs/pickup_patterns.json').read_text())
for pickup in repairs['pickups']:
 assert pickup_patterns[pickup['tile']]==pickup['native_pattern']
 assert pickup['rule'] in lines
 source=pickup['source_rule'].split('<tile>')[1].split(',');target=pickup['rule'].split('<tile>')[1].split(',')
 assert source[:1]+source[2:]==target[:1]+target[2:]
 assert pickup_patterns[source[1]]==pickup_patterns[target[1]]
# Recover the entire previous candidate before applying its frozen checks.
assert not repairs['artwork_changed']
for change in repairs['neighbor_rewrites']:
 replacement='\n'.join(change['replacements'])+'\n'
 assert content.count(replacement)==1
 content=content.replace(replacement,change['original']+'\n')
for section in ['CONDITIONS','PICKUPS']:
 content,n=re.subn(r'^# BEGIN TEMPLE_REPAIRS '+section+r'\n.*?^# END TEMPLE_REPAIRS '+section+r'\n','',content,flags=re.M|re.S);assert n==1
previous_repairs=json.loads((root/'evidence/0.16.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_repairs['hires.txt'],'0.16.1 mapping recovery failed'
for name,digest in previous_repairs.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior art changed'
assert legacy_files-{'Golden_Temple_Courtyard_2x.png','Golden_Temple_Stairs_2x.png'}==set(previous_repairs)
counts['tile']-=repairs['extra_tile_rules'];counts['condition']-=repairs['extra_conditions']
masonry=json.loads((root/'art/level4_masonry/registration.json').read_text())
counts['tile']-=masonry['tile_rules'];counts['condition']-=masonry['conditions']
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN TEMPLE_MASONRY '+section+r'\n.*?^# END TEMPLE_MASONRY '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
previous_masonry=json.loads((root/'evidence/0.16.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_masonry['hires.txt'],'0.16.0 mappings changed'
for name,digest in previous_masonry.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior art changed'
current_files=legacy_files-{'Golden_Temple_Courtyard_2x.png','Golden_Temple_Masonry_2x.png','Golden_Temple_Stairs_2x.png'}
assert current_files==set(previous_masonry)
assert not masonry['backgrounds_modified'] and not masonry['outdoor_columns_modified']
for m in masonry['mappings']:
 t=int(m['tile'],16)
 assert 0xb3a<=t<=0xb49 or 0xb4e<=t<=0xb53 or 0xb78<=t<=0xb7b or 0xb80<=t<=0xb88 or 0xaf8<=t<=0xafb
 assert m['scope'].startswith(('templeA865Mode&templeA865Lo&templeA865Hi','templeAA09Mode&templeAA09Lo&templeAA09Hi','templeAA81Mode&templeAA81Lo&templeAA81Hi'))
temple=json.loads((root/'art/level4/registration.json').read_text())
temple_files={'Golden_Temple_Tiles_2x.png','Golden_Temple_Exterior.png','Golden_Temple_Interior.png'}
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=temple[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN GOLDEN_TEMPLE '+section+r'\n.*?^# END GOLDEN_TEMPLE '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
previous_temple=json.loads((root/'evidence/0.15.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_temple['hires.txt'],'Approved 0.15.0 mappings changed'
for name,digest in previous_temple.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved artwork changed'
assert current_files-set(previous_temple)==temple_files
for fit in temple['actor_fits'].values():assert fit['clipped_pixels']==0
temple_patterns=json.loads((root/'art/level4/native_patterns.json').read_text())
for key,aliases in json.loads((root/'art/level4/overdrive_aliases.json').read_text()).items():
 for alias in aliases:assert bytes.fromhex(temple_patterns[key])==bytes.fromhex(temple_patterns[alias])
for record in temple['mappings']:
 if record['kind'] in {'native collision masonry','outdoor gold column','nonsolid scenery reveal','temple entrance facade','dark entrance'}:
  assert record['scope'].startswith(('templeA865Mode&templeA865Lo&templeA865Hi','templeAA09Mode&templeAA09Lo&templeAA09Hi','templeAA81Mode&templeAA81Lo&templeAA81Hi'))
historical_files=current_files-temple_files
finale=json.loads((root/'art/level3_finale/registration.json').read_text())
finale_files={'Level3_Finale_Tiles_2x.png','Overdrive_Acquired.png'}
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=finale[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
 pattern=r'^# BEGIN LEVEL3_FINALE '+section+r'\n.*?^# END LEVEL3_FINALE '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
previous_finale=json.loads((root/'evidence/0.14.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_finale['hires.txt'],'Approved 0.14.0 mappings changed'
for name,digest in previous_finale.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved artwork changed'
assert historical_files-set(previous_finale)==finale_files
assert not finale['native_gameplay_modified']and not finale['previous_runtime_art_modified']
assert finale['boss_fit']['clipped_pixels']==0
shared_finale=json.loads((root/'art/level3_finale/shared_patterns.json').read_text())
for m in finale['actor_aliases']:assert m['source_tile']in shared_finale[m['tile']]
patterns_finale=json.loads((root/'art/level3_finale/native_patterns.json').read_text())
for t,m in finale['terrain_aliases'].items():assert patterns_finale[t]==patterns_finale[m['source_tile']]
moss=json.loads((root/'art/poison_moss/registration.json').read_text())
moss_files={'Poison_Moss_Tiles_2x.png','Poison_Moss_Forest_Background.png','Poison_Moss_Ruins_Background.png'}
counts['tile']-=moss['tile_rules']
for section in ['IMAGES','MAPPINGS']:
 pattern=r'^# BEGIN POISON_MOSS '+section+r'\n.*?^# END POISON_MOSS '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
for m in moss['background_replacements']:
 assert m['after']in content;content=content.replace(m['after'],m['before'],1)
previous_moss=json.loads((root/'evidence/0.13.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_moss['hires.txt'],'Rules changed beyond requested Level 3 scenery'
for name,digest in previous_moss.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' previous artwork changed'
assert historical_files-set(previous_moss)==moss_files|finale_files
moss_atlas=Image.open(pack/'Poison_Moss_Tiles_2x.png').convert('RGBA');moss_sources={}
for m in moss['mappings']:
 f=m['source_rule'].split('<tile>')[1].split(',');idx=int(f[0]);x,y=map(int,f[3:5]);xx,yy=m['xy']
 if idx not in moss_sources:moss_sources[idx]=Image.open(pack/imgs[idx]).convert('RGBA')
 alpha=moss_sources[idx].crop((x,y,x+16,y+16)).getchannel('A').tobytes()
 assert alpha==moss_atlas.crop((xx,yy,xx+16,yy+16)).getchannel('A').tobytes(),'Terrain contour changed'
 assert hashlib.sha256(alpha).hexdigest()==m['alpha_sha256']
 assert 0x700<=int(m['tile'],16)<0x800 and not 0x73e<=int(m['tile'],16)<=0x743
assert not moss['native_gameplay_modified']
for name in ['Forest','Ruins']:
 bg=np.array(Image.open(pack/f'Poison_Moss_{name}_Background.png').convert('RGB'))
 assert bg.shape==(480,10240,3)
 period=bg[:,:1024]
 assert np.array_equal(period[:,:512],period[:,512:][:,::-1]),'Background midpoint is not mirrored'
 assert np.array_equal(period[:,0],period[:,-1]),'512-native-pixel camera wrap has a seam'
 for x in range(0,10240,1024):assert np.array_equal(bg[:,x:x+1024],period),'Background camera period changed'
caves=json.loads((root/'art/level3_caves/registration.json').read_text())
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=caves[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN LEVEL3_CAVES '+section+r'\n.*?^# END LEVEL3_CAVES '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
assert not caves['native_gameplay_modified']
previous_caves=json.loads((root/'evidence/0.12.2-pack-sha256.json').read_text())
for name,digest in previous_caves.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest, name+' previous artwork changed'
assert historical_files-set(previous_caves)=={'Stage3_Caves_Tiles_2x.png'}|moss_files|finale_files
cave_atlas=np.array(Image.open(pack/'Stage3_Caves_Tiles_2x.png').convert('RGBA'))
for m in caves['mappings']:
 if 'xy'not in m:continue
 x,y=m['xy'];key=m['scope'][3:7]+'/'+m['tile']+'/'+m['palette']
 if key in caves['terrain_masks']:assert np.array_equal(cave_atlas[y:y+16,x:x+16,3],caves['terrain_masks'][key])
fish_stability=json.loads((root/'art/big_fish_motion/registration.json').read_text())
counts['tile']-=fish_stability['tile_rules'];counts['condition']-=fish_stability['conditions']
for section in ['CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN BIG_FISH_STABILITY '+section+r'\n.*?^# END BIG_FISH_STABILITY '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
prior_fish=json.loads((root/'evidence/0.12.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==prior_fish['hires.txt'],'Earlier mappings changed outside fish stabilization'
for name,digest in prior_fish.items():
 if name not in {'hires.txt','README.txt','Stage3_Lava_Tiles_2x.png'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
base_fish_atlas=np.array(Image.open(root/'art/level3_lava/Stage3_Lava_Tiles_2x.png').convert('RGBA'))
current_fish_atlas=np.array(Image.open(pack/'Stage3_Lava_Tiles_2x.png').convert('RGBA'))
assert np.array_equal(current_fish_atlas[:496],base_fish_atlas[:496])
assert np.array_equal(current_fish_atlas[496:,320:],base_fish_atlas[496:,320:])
assert not base_fish_atlas[496:,:,3].any()
assert not fish_stability['native_gameplay_modified']
level3_lava=json.loads((root/'art/level3_lava/registration.json').read_text())
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=level3_lava[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN LEVEL3_LAVA '+section+r'\n.*?^# END LEVEL3_LAVA '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
prior_lava=json.loads((root/'evidence/0.11.2-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==prior_lava['hires.txt'],'Approved Level 3 mappings changed'
for name,digest in prior_lava.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved Level 3 art changed'
lava_atlas=Image.open(pack/'Stage3_Lava_Tiles_2x.png').convert('RGBA');boot=Image.open(root/'art/level3_detail/boot.png').convert('RGBA')
menu_rows=[[0x974,0x973],[0x972,0x971]]
for m in level3_lava['mappings']:
 if m['kind']=='approved boot menu':
  t=int(m['tile'],16);y=next(i for i,row in enumerate(menu_rows)if t in row);x=menu_rows[y].index(t);xx,yy=m['xy']
  assert lava_atlas.crop((xx,yy,xx+16,yy+16)).tobytes()==boot.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()
assert len(level3_lava['lava_aliases'])==18
native_lava=json.loads((root/'art/level3_lava/native_patterns.json').read_text())
for alias in level3_lava['lava_aliases']:
 fields=alias['source_rule'].split('<tile>')[1].split(',');assert native_lava[alias['tile']]==native_lava[fields[1]]
assert not level3_lava['native_gameplay_modified']and not level3_lava['previous_runtime_art_modified']
level3_detail=json.loads((root/'art/level3_detail/registration.json').read_text())
counts['tile']-=level3_detail['tile_rules']
for section in ['IMAGES','MAPPINGS']:
 pattern=r'^# BEGIN LEVEL3_DETAIL '+section+r'\n.*?^# END LEVEL3_DETAIL '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
prior_detail=json.loads((root/'evidence/0.11.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==prior_detail['hires.txt'],'Previous review mappings changed'
for name,digest in prior_detail.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' previous review art changed'
detail_atlas=np.array(Image.open(pack/'Stage3_Detail_Tiles_2x.png').convert('RGBA'))
native_masks=json.loads((root/'art/level3_opening/registration.json').read_text())['terrain_masks']
assert {m['tile']for m in level3_detail['mappings']}=={'0694','068A','068B','068C','068D',*[f'{t:04X}'for t in range(0x768,0x771)]}
for m in level3_detail['mappings']:
 if m['kind']=='branch':
  x,y=m['xy'];assert np.array_equal(detail_atlas[y:y+16,x:x+16,3],np.array(native_masks[f"tree:{m['tile']}:0F091929"]))
level3_review=json.loads((root/'art/level3_review/registration.json').read_text())
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=level3_review[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS']:
 pattern=r'^# BEGIN LEVEL3_REVIEW '+section+r'\n.*?^# END LEVEL3_REVIEW '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
prior_review=json.loads((root/'evidence/0.11.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==prior_review['hires.txt'],'Earlier mappings changed'
for name,digest in prior_review.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' earlier art changed'
level3=json.loads((root/'art/level3_opening/registration.json').read_text())
for key,field in [('tile','tile_rules'),('condition','conditions'),('background','background_rules')]:counts[key]-=level3[field]
for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
 pattern=r'^# BEGIN LEVEL3_OPENING '+section+r'\n.*?^# END LEVEL3_OPENING '+section+r'\n'
 content,n=re.subn(pattern,'',content,flags=re.M|re.S);assert n==1
prior_level3=json.loads((root/'evidence/0.10.2-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==prior_level3['hires.txt'],'Existing mappings changed'
for name,digest in prior_level3.items():
 if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved art changed'
breaker_randy=json.loads((root/'art/breaker_randy/registration.json').read_text())
counts['tile']-=breaker_randy['tile_rules']
counts['condition']-=breaker_randy['conditions']
fade_block=re.search(r'^# BEGIN BREAKER_RANDY\n(.*?)^# END BREAKER_RANDY\n',content,flags=re.M|re.S)
assert fade_block and fade_block.end()<=content.index('# BEGIN BOSS2_REVIEW')
fade_lines=fade_block.group(1).splitlines()
assert sum('<tile>' in line for line in fade_lines)==942
assert sum('<condition>' in line for line in fade_lines)==breaker_randy['conditions']
for line in fade_lines:
 if '<tile>' in line:
  assert line.startswith('[b2Room&b2Lo&b2Hi')
  fields=line.split('<tile>')[1].split(',')
  assert fields[0] in {'18','19','22'} and fields[5] in {'.65','.30','.12'}
content=content[:fade_block.start()]+content[fade_block.end():]
previous_randy=json.loads((root/'evidence/0.10.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_randy['hires.txt']
for name,digest in previous_randy.items():
 if name not in {'README.txt','hires.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved artwork changed'
boss2_review=json.loads((root/'art/boss2_review/registration.json').read_text())
counts['tile']-=boss2_review['tile_rules']
review_block=re.search(r'^# BEGIN BOSS2_REVIEW\n(.*?)^# END BOSS2_REVIEW\n',content,flags=re.M|re.S)
assert review_block and len(review_block.group(1).splitlines())==boss2_review['tile_rules']
assert review_block.end()<=content.index('# BEGIN BOSS2 MAPPINGS')
content=content[:review_block.start()]+content[review_block.end():]
previous_boss=json.loads((root/'evidence/0.10.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==previous_boss['hires.txt']
for name,digest in previous_boss.items():
 if name not in {'README.txt','hires.txt','Boss2_Tiles_2x.png'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' previous boss asset changed'
boss_base=np.array(Image.open(root/'art/boss2/Boss2_Tiles_2x.png').convert('RGBA'))
boss_now=np.array(Image.open(pack/'Boss2_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(boss_base.shape[:2],dtype=bool)
for record in boss2_review['mappings']:
 x,y=record['xy'];allowed[y:y+16,x:x+16]=True
assert not boss_base[allowed].any()
assert np.array_equal(boss_base[~allowed],boss_now[~allowed])
assert not boss2_review['native_gameplay_modified']
boss2=json.loads((root/'art/boss2/registration.json').read_text())
for kind in ['tile','background','condition']:
 counts[kind]-=boss2[{'tile':'tile_rules','background':'background_rules','condition':'conditions'}[kind]]
content=re.sub(r'^# BEGIN BOSS2 (IMAGES|CONDITIONS|MAPPINGS|ALIASES)\n.*?^# END BOSS2 \1\n','',content,flags=re.M|re.S)
reviewed_090=json.loads((root/'evidence/0.9.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==reviewed_090['hires.txt']
for name,digest in reviewed_090.items():
 if name not in {'README.txt','hires.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved asset changed'
assert imgs[39]=='Boss2_Tiles_2x.png'
screen26=json.loads((root/'art/screen2_6/registration.json').read_text())
shared=json.loads((root/'art/shared_stage2/registration.json').read_text())
assert counts['tile']==6997+screen26['tile_rules']+shared['tile_rules']
assert counts['background']==229+screen26['background_rules']
assert counts['condition']==1689+screen26['conditions']
assert screen26['new_painted_assets']==['walking dragon'] and screen26['dragon_clipped_pixels']==[0,0]
assert screen26['shared_dragon_cells']==18
shared_block=re.search(r'^# BEGIN SCREEN2_SHARED\n(.*?)^# END SCREEN2_SHARED\n\Z',content,flags=re.M|re.S)
assert shared_block and shared_block.group(1).splitlines()==[r['rule']for r in shared['records']]
prior_content=content[:shared_block.start()]
for record in shared['records']:
 assert record['source_rule'] in prior_content.splitlines()
 source_fields=record['source_rule'].split('<tile>')[1].split(',')
 fields=record['rule'].split('<tile>')[1].split(',')
 assert fields[:2]+fields[3:]==source_fields[:2]+source_fields[3:]
 assert fields[2]==source_fields[2] or (source_fields[2],fields[2])==('0F071737','0F081737')
content=re.sub(r'^# BEGIN SCREEN2_6 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_6 \1\n','',prior_content,flags=re.M|re.S)
reviewed_083=json.loads((root/'evidence/0.8.3-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==reviewed_083['hires.txt']
for name,digest in reviewed_083.items():
 if name not in {'README.txt','hires.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior artwork changed'
assert imgs[38]=='Stage2_Dragon_2x.png'
# Restore the exact original brown cells, preserving the accepted stair/item art.
geometry=json.loads((root/'art/screen2_5_roof/previous_geometry.json').read_text())
roof_block=re.search(r'^# BEGIN SCREEN2_5_BROWN_ROOF\n(.*?)^# END SCREEN2_5_BROWN_ROOF\n',content,flags=re.M|re.S)
assert roof_block is not None and len(geometry)==46
expected_roof=[]
for identity,source in sorted(geometry.items()):
 x,y=source['xy'];index=imgs.index(source['image'])
 expected_roof.append(f'[s25Room&s25DataLo&s25DataHi]<tile>{index},{identity},0F071737,{x},{y},1,N')
assert roof_block.group(1).splitlines()==expected_roof
assert not any('<tile>' in line or '<background>' in line for line in content[:roof_block.start()].splitlines())
content=content[:roof_block.start()]+content[roof_block.end():]
reviewed_081=json.loads((root/'evidence/0.8.1-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==reviewed_081['hires.txt']
for name,digest in reviewed_081.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior runtime bytes changed'
assert 'Stage2_Crimson_Ceiling_2x.png' not in imgs
# Review overrides are additive; all 86 earlier runtime assets stay exact.
content=re.sub(r'^# BEGIN SCREEN2_5_REVIEW (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_5_REVIEW \1\n','',content,flags=re.M|re.S)
reviewed_080=json.loads((root/'evidence/0.8.0-pack-sha256.json').read_text())
assert hashlib.sha256(content.encode()).hexdigest()==reviewed_080['hires.txt']
for name,digest in reviewed_080.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior runtime bytes changed'
assert imgs[37]=='Stage2_Cave_Review_2x.png'
baseline=root/'rollback/approved_v15'
arm_atlases={'Randy_Entrance_2x.png','Randy_Equipped_2x.png'}
repaired_backgrounds={'Title_HD.png','Title_Intro_HD.png','EntranceScene.png'}
for p in baseline.glob('*.png'):
 if p.name in repaired_backgrounds:
  before=np.array(Image.open(p).convert('RGBA'));after=np.array(Image.open(pack/p.name).convert('RGBA'))
  assert before.shape==after.shape,p.name
  allowed=np.zeros(before.shape[:2],dtype=bool)
  if p.name.startswith('Title_'):allowed[390:452,100:412]=True
  else:
   allowed[192:236,0:128]=True
   allowed[544:588,0:160]=True
  assert np.any(before!=after),p.name+' repair missing'
  assert not np.any(np.any(before!=after,axis=2)&~allowed),p.name+' changed outside repair'
 elif p.name not in arm_atlases:assert p.read_bytes()==(pack/p.name).read_bytes(),p.name
 else:
  expected=Image.open(p).convert('RGBA')
  patch=Image.open(root/'art/randy_arm_patch.png').convert('RGBA')
  for pose,(x,y) in json.loads((root/'art/arm_repair.json').read_text())['pose_positions'].items():
   i=int(pose);expected.alpha_composite(patch,(i%4*64+x,i//4*64+y))
  mode=0 if p.name=='Randy_Entrance_2x.png' else 1
  for phase in range(2):
   sprite=Image.open(root/f'art/review_fixes/randy_{mode}_{phase}.png').convert('RGBA')
   expected.paste(sprite,((phase+2)*64,128))
  foot=json.loads((root/'art/randy_foot/registration.json').read_text())
  assert foot['target_pose']==0 and foot['target_rectangle']==[16,32,32,64]
  boot=Image.open(root/'art/randy_foot'/foot['patches'][p.name]).convert('RGBA')
  assert boot.size==(16,32)
  expected.paste(boot,(16,32))
  assert np.array_equal(np.array(expected),np.array(Image.open(pack/p.name).convert('RGBA'))),p.name
# Crimson-room additions must preserve the exact 0.7.1 pack.
pre_crimson=re.sub(r'^# BEGIN SCREEN2_5 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_5 \1\n','',content,flags=re.M|re.S)
reviewed_071=json.loads((root/'evidence/0.7.1-pack-sha256.json').read_text())
assert hashlib.sha256(pre_crimson.encode()).hexdigest()==reviewed_071['hires.txt']
for name,digest in reviewed_071.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' prior runtime bytes changed'
assert imgs[36]=='Stage2_Crimson_Cave_Tiles_2x.png'
crimson=json.loads((root/'art/screen2_5/registration.json').read_text())
assert crimson['shared_aliases']==359 and crimson['new_tile_rules']==32
assert crimson['background_rules']==58
# The stair review adds twelve rules and unused atlas cells only.
pre_stairs=re.sub(r'^# BEGIN SCREEN2_4_STAIRS\n.*?^# END SCREEN2_4_STAIRS\n','',pre_crimson,flags=re.M|re.S)
reviewed_070=json.loads((root/'evidence/0.7.0-pack-sha256.json').read_text())
assert hashlib.sha256(pre_stairs.encode()).hexdigest()==reviewed_070['hires.txt']
prior_stair_atlas=Image.open(root/'art/screen2_4/Stage2_Second_Cave_Tiles_2x_0.7.0.png').convert('RGBA')
current_stair_atlas=Image.open(pack/'Stage2_Second_Cave_Tiles_2x.png').convert('RGBA')
for box in [(0,0,128,16),(0,16,16,32)]:
 assert prior_stair_atlas.crop(box).tobytes()==current_stair_atlas.crop(box).tobytes()
# The second horizontal cave must preserve every approved 0.6.1 asset/rule.
pre_second_cave=re.sub(r'^# BEGIN SCREEN2_4 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_4 \1\n','',pre_crimson,flags=re.M|re.S)
approved_061=json.loads((root/'evidence/0.6.1-pack-sha256.json').read_text())
assert hashlib.sha256(pre_second_cave.encode()).hexdigest()==approved_061['hires.txt']
for name,digest in approved_061.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.6.1 bytes changed'
assert imgs[35]=='Stage2_Second_Cave_Tiles_2x.png'
second_cave=json.loads((root/'art/screen2_4/registration.json').read_text())
assert second_cave['shared_aliases']==304 and second_cave['new_tile_rules']==56
assert second_cave['background_rules']==47 and second_cave['new_painted_sources']==0
assert not second_cave['native_collision_modified'] and not second_cave['previous_artwork_modified']
second_cave_atlas=Image.open(pack/imgs[35]).convert('RGBA')
cleared=[]
for mapping in second_cave['mappings']:
 if mapping['kind']=='cave backdrop reveal':
  x,y=mapping['atlas'];assert not second_cave_atlas.crop((x,y,x+16,y+16)).getbbox()
  cleared.append(mapping['identity'])
assert cleared==['0300','036E','036F','039B','039C','039D','039E','039F','03A0']
# The vertical chamber must preserve every approved earlier cave asset/rule.
pre_vertical=re.sub(r'^# BEGIN SCREEN2_3 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_3 \1\n','',pre_second_cave,flags=re.M|re.S)
approved_051=json.loads((root/'evidence/0.5.1-pack-sha256.json').read_text())
assert hashlib.sha256(pre_vertical.encode()).hexdigest()==approved_051['hires.txt']
for name,digest in approved_051.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.5.1 bytes changed'
assert imgs[34]=='Stage2_Vertical_Cave_Tiles_2x.png'
vertical=json.loads((root/'art/screen2_3/registration.json').read_text())
assert vertical['shared_aliases']==98 and vertical['new_tile_rules']==12
assert vertical['background_rules']==18 and vertical['background_scroll']==[0,0]
assert not vertical['native_collision_modified'] and not vertical['previous_artwork_modified']
assert vertical['eye_size']==[32,32]
vertical_atlas=Image.open(pack/imgs[34]).convert('RGBA')
prior_vertical=np.array(Image.open(root/'evidence/screen2_3_review/baseline_0.6.0_atlas.png').convert('RGBA'))
tear_cells=np.zeros(prior_vertical.shape[:2],dtype=bool)
for mapping in vertical['mappings']:
 if mapping['identity'] in ['02DC','02DD']:
  x,y=mapping['atlas'];tear_cells[y:y+16,x:x+16]=True
assert not np.any(np.any(prior_vertical!=np.array(vertical_atlas),axis=2)&~tear_cells)
assert hashlib.sha256(pre_second_cave.encode()).hexdigest()==json.loads((root/'evidence/0.6.0-pack-sha256.json').read_text())['hires.txt']
for mapping in vertical['mappings']:
 if mapping['kind']=='cave backdrop reveal':
  x,y=mapping['atlas'];assert not vertical_atlas.crop((x,y,x+16,y+16)).getbbox()
# The earlier cave must preserve every approved exterior/earlier asset and rule.
pre_cave=re.sub(r'^# BEGIN SCREEN2_2 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_2 \1\n','',pre_vertical,flags=re.M|re.S)
approved_041=json.loads((root/'evidence/0.4.1-pack-sha256.json').read_text())
assert hashlib.sha256(pre_cave.encode()).hexdigest()==approved_041['hires.txt']
for name,digest in approved_041.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.4.1 bytes changed'
assert imgs[33]=='Stage2_Cave_Tiles_2x.png'
# Stage 2 additions must strip back to the exact approved 0.3.5 mapping.
pre_stage2=re.sub(r'^# BEGIN SCREEN2_1 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN2_1 \1\n','',pre_cave,flags=re.M|re.S)
approved_035=json.loads((root/'evidence/0.3.5-pack-sha256.json').read_text())
assert hashlib.sha256(pre_stage2.encode()).hexdigest()==approved_035['hires.txt']
for name,digest in approved_035.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.3.5 bytes changed'
assert imgs[32]=='Stage2_Exterior_Tiles_2x.png'
# Both additions own marked sections. Removing these must recover the exact
# approved mapping file, including ordering and whitespace.
approved_rules=re.sub(r'^# BEGIN RECOVERY_ITEMS (IMAGES|MAPPINGS)\n.*?^# END RECOVERY_ITEMS \1\n','',pre_stage2,flags=re.M|re.S)
approved_rules=re.sub(r'^# BEGIN BOSS1 (IMAGES|CONDITIONS|MAPPINGS|ALIASES|OPTIONS)\n.*?^# END BOSS1 \1\n','',approved_rules,flags=re.M|re.S)
approved_rules=re.sub(r'^# BEGIN STANDING_LEG CONDITIONS\n.*?^# END STANDING_LEG CONDITIONS\n','',approved_rules,flags=re.M|re.S)
approved_rules=approved_rules.replace('[standingLegNormal]<tile>18,07,','[randySig8]<tile>18,07,').replace('[standingLegTwin]<tile>19,07,','[randyEquippedSig8]<tile>19,07,')
approved_021=json.loads((root/'evidence/0.2.1-pack-sha256.json').read_text())
assert hashlib.sha256(approved_rules.encode()).hexdigest()==approved_021['hires.txt']
for name,digest in approved_021.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.2.1 bytes changed'
boss=json.loads((root/'art/boss1/registration.json').read_text())
assert boss['tile_rules']==2433 and boss['conditions']==1083 and boss['background_rules']==4
assert boss['shared_bank_aliases']==758 and not boss['collision_modified'] and not boss['existing_rules_modified']
assert boss['global_sprite_limit_changed']
assert [line for line in lines if line.startswith('<options>')]==['<options>disableSpriteLimit']
assert '<addition>' not in content
assert boss['menu_glyphs']=={'0964':'R','0965':'D'}
assert boss['pre_announcement_fade']=={'FF202020':255,'FF101010':173,'FF000000':102}
wall=np.array(Image.open(pack/'Nave_Background.png').convert('RGB'))
ascent=np.array(Image.open(pack/'Blizzard_Ascent_Background.png').convert('RGB'))
assert ascent.shape==(wall.shape[0]*3,wall.shape[1],3)
assert all(np.array_equal(ascent[i*wall.shape[0]:(i+1)*wall.shape[0]],wall) for i in range(3))
for identity in boss['menu_glyphs']:
 assert sum(f'[pauseScreen&pauseMagicRow&pausedPalette]<tile>30,{identity},0F072830,' in line for line in lines)==1
assert imgs[30]=='Boss_Tiles_2x.png'
assert imgs[31]=='Recovery_Items_2x.png'
prior=json.loads((root/'evidence/0.3.4-pack-sha256.json').read_text())
for name,digest in prior.items():
 if name not in {'README.txt','hires.txt'}:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' confirmed 0.3.4 art changed'
without_items=re.sub(r'^# BEGIN RECOVERY_ITEMS (IMAGES|MAPPINGS)\n.*?^# END RECOVERY_ITEMS \1\n','',pre_stage2,flags=re.M|re.S)
assert hashlib.sha256(without_items.encode()).hexdigest()==prior['hires.txt']
items=json.loads((root/'art/pickups/registration.json').read_text())
assert items['tile_rules']==64 and not items['native_geometry_changed'] and not items['existing_rules_modified']
item_atlas=Image.open(pack/'Recovery_Items_2x.png').convert('RGBA')
assert item_atlas.size==(32,32)
assert not np.any(np.array(item_atlas)[:8,:,3])
for i,name in enumerate(['hp','magic']):
 assert np.array_equal(np.array(item_atlas)[:,i*16:(i+1)*16],np.array(Image.open(root/f'art/pickups/{name}_flask.png').convert('RGBA')))
previous_rules=re.sub(r'^# BEGIN SCREEN1_4 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN1_4 \1\n','',approved_rules,flags=re.M|re.S)
approved_011=json.loads((root/'evidence/0.1.1-pack-sha256.json').read_text())
assert hashlib.sha256(previous_rules.encode()).hexdigest()==approved_011['hires.txt']
for name,digest in approved_011.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.1.1 bytes changed'
tree=json.loads((root/'art/screen1_4/registration.json').read_text())
assert tree['tile_rules']==198 and tree['new_atlas_cells']==150 and tree['shared_enemy_rules']==48
assert tree['conditions']==4 and tree['background_rules']==1
assert not tree['collision_modified'] and not tree['existing_rules_modified']
assert content.count('['+tree['scope']+']<tile>29,')==150
original_rules=re.sub(r'^# BEGIN REVIEW_FIXES (CONDITIONS|MAPPINGS)\n.*?^# END REVIEW_FIXES \1\n','',previous_rules,flags=re.M|re.S)
original_rules=re.sub(r'^# BEGIN SCREEN1_3 (IMAGES|CONDITIONS|MAPPINGS)\n.*?^# END SCREEN1_3 \1\n','',original_rules,flags=re.M|re.S)
assert original_rules.encode()==(baseline/'hires.txt').read_bytes()
approved_002=json.loads((root/'evidence/0.0.2-pack-sha256.json').read_text())
for name,digest in approved_002.items():
 if name not in {'README.txt','hires.txt'}|arm_atlases:
  assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name+' approved 0.0.2 bytes changed'
assert imgs[28]=='Nave_Tiles_2x.png' and imgs[29]=='Tree_Court_Tiles_2x.png'
nave=json.loads((root/'art/screen1_3/registration.json').read_text())
assert nave['tile_rules']==87 and nave['conditions']==3 and nave['background_rules']==1
assert not nave['collision_modified'] and not nave['existing_rules_modified']
assert content.count('['+nave['scope']+']<tile>28,')==87
# The old 87 atlas cells (including every rolling frame) remain byte-identical
# at the pixel level; only twelve previously empty standing cells are added.
before=np.array(Image.open(root/'art/screen1_3/Nave_Tiles_2x.png').convert('RGBA'))
after=np.array(Image.open(pack/'Nave_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(before.shape[:2],dtype=bool)
for slot in range(87,99):
 x,y=slot%16*16,slot//16*16;allowed[y:y+16,x:x+16]=True
assert not np.any(np.any(before!=after,axis=2)&~allowed)
repairs=json.loads((root/'art/review_fixes/registration.json').read_text())
assert repairs['tile_rules']==50 and repairs['conditions']==66
assert repairs['rolling_pixels_changed']==0 and repairs['existing_pose_pixels_changed']==0
assert (baseline/'Entrance_SFX_Priority.ips').read_bytes()==(pack/'Entrance_SFX_Priority.ips').read_bytes()
# Conditional pose rules must precede any corresponding ordinary mappings.
first_unconditional={}
for index,line in enumerate(lines):
 m=re.match(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 prefix,v=m.groups();p=v.split(',');key=(p[1],p[2])
 if prefix:assert key not in first_unconditional,line
 else:first_unconditional[key]=index
assert len(re.findall(r'^<tile>27,[0-9A-F]{2}(?:6[4-9A-F]|7[0-3]),FF301116,',content,re.M))==256
assert not re.search(r'<tile>25,(?:6[C-F]|7[0-3]),FF301116,',content)
assert content.count('<patch>')==1
assert len(re.findall(r'\[pauseScreen&pauseMagicRow&pausedPalette\]<tile>26,097[5-8],0F172737,',content))==4
for asset in (Path(__file__).resolve().parents[1]/'rollback/bracelet_v14').glob('*.png'):
 if asset.name not in arm_atlases|repaired_backgrounds:assert asset.read_bytes()==(pack/asset.name).read_bytes(),asset.name
assert 'cryptBatPhase' not in content
assert len(re.findall(r'<tile>26,7[4-7],FF160636,',content))==4
assert len(re.findall(r'\[randyDefeated\]<tile>',approved_rules))==64
assert len(re.findall(r'\[randyDefeated\]<tile>',content))==192
assert '<condition>randyDefeated,memoryCheckConstant,0440,==,00' in content
assert not re.search(r'<tile>25,7[4-7],FF160636,',content)
result={'supported_rom_sha1':sha.lower(),'scale':2,'atlas_count':len(imgs),**total_counts,'references_and_bounds_valid':True,'conditional_priority_valid':True,'rom_patch_bytes':56,'patch_scope':'entrance priorities and conditional thunder masking','replacement_audio':False}
print(json.dumps(result,indent=2))
