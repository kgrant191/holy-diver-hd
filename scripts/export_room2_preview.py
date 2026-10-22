from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont
base=Path.cwd();work=base/'work/v13';out=base/'deliverables';tmp=work/'video';tmp.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
board=Image.new('RGB',(1024,1016),'#0b101b');dr=ImageDraw.Draw(board)
for row,(st,fr)in enumerate([(2,6),(3,6)]):
 for col,version in enumerate(['before','after']):
  im=Image.open(work/version/f'state{st}/frames/{fr:04}.png').convert('RGB');board.paste(im,(col*512,row*508+28));dr.text((col*512+12,row*508+5),('Approved v12'if col==0 else'v13 — screen 2'),font=font,fill='#e5dbc5')
board.save(out/'Holy_Diver_v13_Comparison.png')
# Native emulator captures at one image for every two emulated NTSC frames.
for st in range(1,5):
 folder=tmp/f'state{st}';folder.mkdir(exist_ok=True)
 for j,p in enumerate(sorted((work/'after'/f'state{st}/frames').glob('*.png'))):
  dest=folder/f'{j:04}.png'
  if not dest.exists():dest.symlink_to(p)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','30.0494','-i',str(folder/'%04d.png'),'-i',str(work/'after'/f'state{st}/full.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(tmp/f'state{st}.mp4')],check=True)
(tmp/'concat.txt').write_text(''.join(f"file '{tmp/f'state{st}.mp4'}'\n" for st in range(1,5)))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(tmp/'concat.txt'),'-c','copy','-movflags','+faststart',str(out/'Holy_Diver_v13_Screen_2.mp4')],check=True)
print('Exported live comparison and gameplay',flush=True)
