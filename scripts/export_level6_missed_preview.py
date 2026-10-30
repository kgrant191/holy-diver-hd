"""Export the actual missed-room replay and its verified original audio."""
from pathlib import Path
import argparse,subprocess,json,hashlib
p=argparse.ArgumentParser()
for k in ['capture','output']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];capture=Path(a.capture);out=Path(a.output)
proof=json.loads((root/'evidence/level6_missed/replay.json').read_text());assert proof['native_exact']and proof['pcm_exact']and not proof['missing_backgrounds']
rate='719503/11972';fps=719503/11972;count=8997
command=['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',rate,'-start_number','2','-i',str(capture/'frames/%06d.png'),'-i',str(capture/'full.wav'),'-filter_complex',f'[1:a]atrim=start={1/fps}:duration={count/fps},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-r',rate,'-fps_mode','cfr','-frames:v',str(count),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart',str(out)]
subprocess.run(command,check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)],text=True));v=next(s for s in probe['streams']if s['codec_type']=='video');assert int(v['nb_frames'])==count and(v['width'],v['height'])==(512,480)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
report=dict(file=out.name,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size,frames=count,size=[512,480],fps=rate,duration_seconds=float(probe['format']['duration']),full_av_decode_passed=True,actual_capture_pngs_only=True,movie='Holy_Diver_HD(20261030-015933).mmo',first=2,last=8998,audio_source='Verified original Mesen PCM; AAC stereo 48 kHz with native one-frame capture offset.')
(root/'evidence/level6_missed/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
