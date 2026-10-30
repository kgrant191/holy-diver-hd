"""Actual face-room excerpt followed by the complete finale, with captured audio."""
from pathlib import Path
import argparse,subprocess,json,hashlib

p=argparse.ArgumentParser()
for name in ['face','finale','output']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];face,finale,out=Path(a.face),Path(a.finale),Path(a.output)
for name in ['replay','face_replay']:
    report=json.loads((root/f'evidence/level6_finale_repair/{name}.json').read_text());assert report['native_exact']and report['pcm_exact']and report['all_image_changes_within_requested_scope']
fps=719503/11972;rate='719503/11972';first,last=550,1150;count0=last-first+1;count1=19214
filters=(f'[0:v]trim=end_frame={count0},setpts=PTS-STARTPTS[v0];'
         f'[1:a]atrim=start={(first-1)/fps}:duration={count0/fps},asetpts=PTS-STARTPTS[a0];'
         f'[2:v]setpts=PTS-STARTPTS[v1];'
         f'[3:a]atrim=start={1/fps}:duration={count1/fps},asetpts=PTS-STARTPTS[a1];'
         '[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]')
command=['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',rate,'-start_number',str(first),'-t',str(count0/fps),'-i',str(face/'frames/%06d.png'),'-i',str(face/'full.wav'),'-framerate',rate,'-start_number','2','-i',str(finale/'frames/%06d.png'),'-i',str(finale/'full.wav'),'-filter_complex',filters,'-map','[v]','-map','[a]','-r',rate,'-fps_mode','cfr','-frames:v',str(count0+count1),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart',str(out)]
subprocess.run(command,check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)],text=True));video=next(s for s in probe['streams']if s['codec_type']=='video');assert int(video['nb_frames'])==count0+count1;assert (video['width'],video['height'])==(512,480)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
report=dict(file=out.name,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size,frames=count0+count1,size=[512,480],fps=rate,duration_seconds=float(probe['format']['duration']),full_av_decode_passed=True,actual_capture_pngs_only=True,segments=[dict(movie='20261029-215619',first=first,last=last),dict(movie='20261029-225605',first=2,last=19215)],audio_source='Verified original Mesen PCM, AAC stereo 48 kHz; native one-frame capture offset retained.')
(root/'evidence/level6_finale_repair/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
