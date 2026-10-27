import json,re,sys,base64,zlib
LOG=sys.argv[1]; tag=sys.argv[2]
best=None
for line in open(LOG,encoding='utf-8'):
    if tag+'_BEGIN' not in line: continue
    try: obj=json.loads(line)
    except: continue
    s=json.dumps(obj,ensure_ascii=False)
    def walk(o):
        global best
        if isinstance(o,str):
            if tag+'_BEGIN' in o and tag+'_END' in o:
                best=o[o.index(tag+'_BEGIN'):o.index(tag+'_END')]
        elif isinstance(o,dict): [walk(v) for v in o.values()]
        elif isinstance(o,list): [walk(v) for v in o]
    walk(obj)
open(sys.argv[3],'w').write(best or '')
print(len(best or ''))
