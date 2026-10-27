"""Actual branch replay comparison followed by a clearly labeled artwork panel."""
from pathlib import Path
import argparse,subprocess,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--work',required=True);p.add_argument('--out',required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];work=Path(a.work);work.mkdir(exist_ok=True,parents=True);frames=work/'frames';frames.mkdir(exist_ok=True);font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),16)
for j,n in enumerate(range(2,602)):
 im=Image.new('RGB',(1024,512),'#10131a');d=ImageDraw.Draw(im)
 for col,(root,title)in enumerate([(a.before,'Approved0.20.2'),(a.after,'Cleanup0.20.3')]):
  im.paste(Image.open(Path(root)/'frames'/f'{n:06}.png').convert('RGB'),(col*512,32));d.text((col*512+12,8),title+' — actual tree replay',font=font,fill='#ead7ac')
 im.save(frames/f'{j:06}.png',compress_level=1)
clip=work/'tree.mp4';fps=60.0988138974405
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate',str(fps),'-i',str(frames/'%06d.png'),'-ss',str(1/fps),'-i',str(Path(a.after)/'full.wav'),'-t',str(600/fps),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-r','60','-threads','2','-c:a','aac','-ar','48000','-b:a','128k',str(clip)],check=True)
panel=Image.new('RGB',(1024,512),'#200912');d=ImageDraw.Draw(panel);d.text((32,20),'Potion artwork comparison — enlarged pixels, not a gameplay capture',font=font,fill='#f4e8d0')
for col,(path,title)in enumerate([(r/'art/screen2_5_review/health_jug.png','Before'),(r/'art/tree_potion_cleanup/health_jug.png','After')]):
 sprite=Image.open(path).convert('RGBA').resize((256,256),Image.Resampling.NEAREST);panel.paste(sprite,(col*512+128,128),sprite);d.text((col*512+218,85),title,font=font,fill='#ead7ac')
panel.save(work/'potion_art.png');artclip=work/'potion.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-loop','1','-i',str(work/'potion_art.png'),'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','3','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-r','60','-threads','2','-c:a','aac','-ar','48000','-b:a','128k',str(artclip)],check=True)
listing=work/'concat.txt';listing.write_text("file '"+str(clip)+"'\nfile '"+str(artclip)+"'\n")
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',a.out],check=True)
print(json.dumps(dict(preview=a.out,tree_actual_replay=True,potion_panel_artwork_only=True)))
