"""Measure the controller-only left stop, full traverse and native walk-off."""
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();c=Path(a.capture)
rows=[]
for n in range(1048,1230):
 b=(c/'ram'/f'{n:06}.bin').read_bytes();rows.append([n,int.from_bytes(b[0x60:0x62],'little')+b[0x340],b[0x350]])
stop=[x for x in rows if 1060<=x[0]<=1080];grounded=[x for x in rows if x[0]>1080 and x[2]==160];fall=[x for x in rows if x[0]>1080 and x[2]>160]
assert all(x[1:]==[499,160]for x in stop)
assert grounded[-1]==[1187,553,160] and fall[0]==[1188,554,161]
assert {x[1]for x in grounded}==set(range(499,554))
report=dict(route='Original prefix 1048, left8, wait24, then right2/wait2 x90',fields=['frame','world_player_x','player_y'],left_stop_samples=stop,last_grounded_samples=grounded[-12:],first_falling_samples=fall[:12],every_supported_anchor_traversed=True,notes='Camera X plus player X gives the world anchor. Feet reach Y184 while grounded. Actual paired pictures show the supported left stop, complete top-surface traverse and right walk-off; Randy art and native collision remain unchanged.')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
