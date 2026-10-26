"""Reproduce the controller-only lowest-branch probe from the supplied movie."""
from pathlib import Path
import argparse,zipfile
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');p.add_argument('--span',action='store_true');a=p.parse_args()
with zipfile.ZipFile(a.movie)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def line(buttons):return '|..|'+''.join(c if c in buttons else '.'for c in 'UDLRSsBA')+'|........'
inputs=rows[:1624]+[line('R')]*24+[line('')]*8+[line(('L'if n%4<3 else '')+('B'if n%16<6 else ''))for n in range(100)]+[line('')]*36
if a.span:inputs=rows[:1628]+[line('L')]*36+[line('')]*12+[line('R'if n%4<3 else '')for n in range(100)]+[line('')]*20
with zipfile.ZipFile(a.out,'w',zipfile.ZIP_DEFLATED)as z:
 for key,value in entries.items():z.writestr(key,('\n'.join(inputs)+'\n').encode()if key=='Input.txt'else value)
print('Wrote',len(inputs),'input frames; original state and settings retained.')
