"""Replace later Palace masonry and correct the Level 3 acquisition book."""
from pathlib import Path
import hashlib,json,re
from PIL import Image

R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/palace_surfaces';G=R/'art/generated'
A.mkdir(exist_ok=True)
prior=json.loads((R/'evidence/0.31.0-pack-sha256.json').read_text())
text=(P/'hires.txt').read_text();assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==72
defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in lines if l.startswith('<condition>')}
rooms=['8816','888E','897E','8A6E','8AE6','8BD6','8C4E','8D3E','8E6A','8EE2']
styles={'001030':'silver','040F24':'violet','0B1B3B':'green'}
uv=json.loads((A/'native_uv.json').read_text());materials={}
for style in styles.values():
    # Register a whole two-by-two native tile unit, then slice it. The same
    # material is used by stairs, caps, wall faces and moving stone lifts.
    im=Image.open(G/f'palace_surface_{style}.png').convert('RGB').resize((32,32),Image.Resampling.LANCZOS).quantize(colors=64,dither=Image.Dither.NONE).convert('RGBA')
    im.save(A/f'{style}_unit.png');materials[style]=im
book=Image.open(G/'palace_surface_book.png').convert('RGBA');book=book.crop(book.getchannel('A').getbbox());book.thumbnail((30,30),Image.Resampling.LANCZOS)
whole=Image.new('RGBA',(32,32));whole.paste(book,((32-book.width)//2,(32-book.height)//2));whole.save(A/'overdrive_book.png')
atlas=Image.new('RGBA',(512,256));cache={};loaded={};changes=[]
def register(im):
    digest=hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cache:
        n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<256;cache[digest]=xy;atlas.paste(im,xy)
    return cache[digest]
def cell(f):
    name=images[int(f[0])]
    if name not in loaded:loaded[name]=Image.open(P/name).convert('RGBA')
    x,y=map(int,f[3:5]);return loaded[name].crop((x,y,x+16,y+16))
def room_for(head):
    ds=[defs.get(t.lstrip('!'),[])for t in head.split('&')]
    vals={d[1]:d[3]for d in ds if len(d)==4 and d[0]=='memoryCheckConstant'and d[2]=='=='}
    return vals.get('0079','')+vals.get('0078','')
for i,old in enumerate(lines):
    m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',old)
    if not m:continue
    head=m[1]or'';f=m[2].split(',');room=room_for(head);t=int(f[1],16);kind=None;style=None;source_xy=None
    if room in rooms and int(f[0])in [57,58,59,60,61]:
        if 0x1100<=t<0x1400 and f[2][:2]in ['0F','30','31']and f[2][2:]in styles:
            style=styles[f[2][2:]];key=f'{room}:{t%256:02X}:{f[2][2:]}'
            source_xy=uv.get(key,{}).get('xy',[(t%2)*16,(t//2%2)*16]);kind='masonry'
        elif 0x1501<=t<=0x150C and f[2]in ['0F001030','30001030','31001030','0F0F0020','0F0F0F10','0F0F0F00','0F021222','0F1B2B3B']:
            style='silver';n=t-0x1501;source_xy=[n%2*16,n//2%2*16];kind='boss masonry'
        elif 0x12F7<=t<=0x12FA and f[2]=='FF003008':
            style='silver';n=t-0x12f7;source_xy=[n%2*16,n//2*16];kind='moving lift'
        if kind:
            original=cell(f)
            if original.getchannel('A').getbbox()is None:continue
            x,y=source_xy;im=materials[style].crop((x,y,x+16,y+16));im.putalpha(original.getchannel('A'))
    elif room=='9F92'and int(f[0])==46 and 0x088b<=t<=0x088e and f[2]=='FF301116':
        n=t-0x088b;x,y=n%2*16,n//2*16;im=whole.crop((x,y,x+16,y+16));kind='Overdrive acquisition book';source_xy=[x,y]
    if kind:
        xy=register(im);f[0]=str(index);f[3:5]=map(str,xy)
        new=('['+head+']'if head else'')+'<tile>'+','.join(f);lines[i]=new
        changes.append(dict(line=i,room=room,kind=kind,style=style,source_xy=source_xy,old=old,new=new))
assert sum(e['kind']=='Overdrive acquisition book'for e in changes)==4
out='\n'.join(lines)+'\n';at=out.index('\n',out.rfind('<img>'))+1
out=out[:at]+'# BEGIN PALACE_SURFACES IMAGES\n<img>Palace_Surfaces_Book_2x.png\n# END PALACE_SURFACES IMAGES\n'+out[at:]
(P/'hires.txt').write_text(out);atlas.save(P/'Palace_Surfaces_Book_2x.png');atlas.save(A/'Palace_Surfaces_Book_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),rooms=rooms,substitutions=changes,source_hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in G.glob('palace_surface_*.png')}),indent=2)+'\n')
print('Palace surfaces and Overdrive book:',len(changes),'replacements;',len(cache),'cells')
