"""Hide the baked-in title prompt during the intro; native ready state reveals it."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json
root=Path(__file__).resolve().parents[1];art=root/'art';pack=root/'build/Holy_Diver_(Tr)'
base=Image.open(art/'Title_HD.png').convert('RGBA')
clean=Image.open(art/'generated/title_without_prompt_generated.png').convert('RGBA').resize(base.size,Image.Resampling.LANCZOS)
# Only the banner footprint is replaced from the generated edit. The entire
# character, logo, sky, moon, flame, footer and surrounding approved art remain.
mask=Image.new('L',base.size);d=ImageDraw.Draw(mask)
d.rectangle((127,406,386,448),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1.2))
intro=Image.composite(clean,base,mask)
intro.save(art/'Title_Intro_HD.png');intro.save(pack/'Title_Intro_HD.png')
p=pack/'hires.txt';s=p.read_text()
s=s.replace('<condition>titleLogoB,ppuMemoryCheckConstant,20A4,==,43',
 '<condition>titleLogoB,ppuMemoryCheckConstant,20A4,==,43\n<condition>titleReady,memoryCheckConstant,04AF,==,01')
s=s.replace('[titleScreen&titleLogoB]<background>Title_HD.png,1,0,0,30,0,0',
 '[titleScreen&titleLogoB&!titleReady]<background>Title_Intro_HD.png,1,0,0,30,0,0\n[titleScreen&titleLogoB&titleReady]<background>Title_HD.png,1,0,0,30,0,0')
p.write_text(s)
(art/'title_prompt_registration.json').write_text(json.dumps({'intro':'Title_Intro_HD.png','ready':'Title_HD.png',
 'ready_condition':'RAM $04AF == $01; native first Start press',
 'generated_patch_rectangle':[127,406,386,448],'feather_radius':1.2,
 'inputs_or_game_state_modified':False},indent=2)+'\n')
