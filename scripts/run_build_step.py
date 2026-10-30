"""Run one builder with complete, atomic PNG and Path output writes.

Pillow's direct file-descriptor encoder can leave short PNGs on mounted
filesystems. Encoding to memory first preserves the exact PNG bytes, and an
atomic rename prevents the next build step from seeing a partial output.
This wrapper affects build I/O only, never artwork or emulator execution.
"""
from pathlib import Path
import io,os,runpy,sys,tempfile
from PIL import Image

original_save=Image.Image.save
original_write_bytes=Path.write_bytes
original_write_text=Path.write_text

def atomic(path,writer):
 path=Path(path)
 fd,name=tempfile.mkstemp(prefix='.build-output-',suffix='.tmp',dir=path.parent)
 os.close(fd);temporary=Path(name)
 try:
  result=writer(temporary)
  with temporary.open('rb')as stream:os.fsync(stream.fileno())
  os.replace(temporary,path)
  return result
 finally:
  if temporary.exists():temporary.unlink()

def write_bytes(path,data):
 def writer(temporary):
  count=original_write_bytes(temporary,data);assert count==len(data)
  assert temporary.read_bytes()==data
  return count
 return atomic(path,writer)

def write_text(path,data,*args,**kwargs):
 return atomic(path,lambda temporary:original_write_text(temporary,data,*args,**kwargs))

def save(self,fp,format=None,**params):
 if isinstance(fp,(str,bytes,os.PathLike))and (format or Path(fp).suffix[1:]).upper()=='PNG':
  buffer=io.BytesIO();original_save(self,buffer,format='PNG',**params)
  write_bytes(Path(fp),buffer.getvalue())
 else:original_save(self,fp,format=format,**params)

Image.Image.save=save
Path.write_bytes=write_bytes
Path.write_text=write_text
script=Path(sys.argv[1]).resolve();sys.argv=sys.argv[1:]
runpy.run_path(str(script),run_name='__main__')
