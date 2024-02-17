import MainShortcuts.path as m_path
import codecs as _codecs
import os as _os
import shutil as _shutil
def read(path,encoding="utf-8"): # Прочитать текстовый файл
  if _os.path.isfile(path):
    with open(path,"rb") as f:
      text=f.read().decode(encoding)
  else:
    text=""
  return text
def write(path,text="",encoding="utf-8",force=False): # Записать текстовый файл
  if _os.path.isdir(path) and force:
    m_path.rm(path)
  with open(path,"wb") as f:
    f.write(str(text).encode(encoding))
  return True
def _open(path): # Открыть содержимое файла
  if _os.path.isfile(path):
    with open(path,"rb") as f:
      content=f.read()
  else:
    content=b""
  return content
load=open
def save(path,content,force=False): # Сохранить содержимое файла
  if _os.path.isdir(path) and force:
    m_path.rm(path)
  with open(path,"wb") as f:
    f.write(content)
  return True
def delete(path):
  type=m_path.info(path)["type"]
  if type=="file":
    m_path.rm(path)
  elif not _os.path.exists(path):
    pass
  else:
    raise Exception("Unknown type: "+type)
def copy(fr,to,force=False):
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _shutil.copy(fr,to)
  else:
    raise Exception("Unknown type: "+type)
def move(fr,to,force=False):
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _shutil.move(fr,to)
  else:
    raise Exception("Unknown type: "+type)
def rename(fr,to,force=False):
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _os.rename(fr,to)
  else:
    raise Exception("Unknown type: "+type)
open=_open
del _open