def path(v,path,sep="/"):
  for k in path.split(sep):
    if isinstance(v,dict):
      v=v[k]
    else:
      v=v[int(k)]
  return v
def swap(i):
  r={}
  for k,v in i.items():
    r[v]=k
  return r
