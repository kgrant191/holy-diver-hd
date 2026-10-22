from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--images-only',action='store_true');p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();capture=Path(a.capture).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
regular=ImageFont.truetype(font,18);small=ImageFont.truetype(font,14);title=ImageFont.truetype(font,26)
canvas=Image.new('RGB',(1088,1170),'#111b29');d=ImageDraw.Draw(canvas)
d.text((24,18),'Holy Diver HD v14',font=title,fill='#f4dfb8')
d.text((24,58),'Bracelet pickup and shared HD Randy death mappings',font=regular,fill='white')
for x,version,label in [(24,'before','Previous pickup'),(552,'after','Gold bracelet with ruby')]:
 im=Image.open(capture/version/'bracelet/frames/0005.png').convert('RGB');canvas.paste(im,(x,119));d.text((x,91),label,font=regular,fill='white')
 crop=im.crop((408,286,456,330)).resize((192,176),Image.Resampling.NEAREST);canvas.paste(crop,(x,615));d.text((x+206,620),'Pickup detail',font=small,fill='#b6c9dd')
for x,case,label,f in [(24,'normal','Normal Randy — death frame',77),(552,'twin','Twin Fire Randy — death frame',74)]:
 im=Image.open(capture/'after'/case/'frames'/f'{f:04}.png').convert('RGB')
 # This crop includes the whole player with surrounding game pixels.
 crop=im.crop((185,326,305,424)).resize((240,196),Image.Resampling.NEAREST)
 # Death crops shown in a separate evidence image to retain ample pixel size.
 row=Image.new('RGB',(512,236),'#111b29');row.paste(crop,(136,40));ImageDraw.Draw(row).text((5,8),label,font=regular,fill='white')
 row.save(out/(case+'_death_detail.png'));canvas.paste(row,(x,815))
d.text((24,1092),'Actual Mesen captures. Details enlarged with nearest-neighbor scaling.',font=regular,fill='#b6c9dd')
d.text((24,1123),'Native movement, item behavior, title sequence and audio are retained.',font=regular,fill='#b6c9dd')
canvas.save(out/'Holy_Diver_v14_Comparison.png')
if a.images_only:sys.exit(0)
clips=[]
for case,label in [('bracelet','Gold bracelet pickup'),('normal','Normal Randy - death'),('twin','Twin Fire Randy - death')]:
 dest=out/(case+'.mp4');clips.append(dest)
 vf=f"scale=1024:960:flags=neighbor,pad=1024:1016:0:56:black,drawtext=fontfile={font}:text='{label}':x=24:y=15:fontsize=26:fontcolor=white"
 subprocess.run(['ffmpeg','-y','-v','error','-framerate','60','-start_number','2','-i',str(capture/'after'/case/'frames/%04d.png'),'-ss','0.016667','-i',str(capture/'after'/case/'full.wav'),'-frames:v','359','-vf',vf,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',str(dest)],check=True)
concat=out/'clips.txt';concat.write_text(''.join("file '"+str(f)+"'\n"for f in clips))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out/'Holy_Diver_v14_Gameplay.mp4')],check=True)
print('Exported',out)
