"""Dựng geo.json từ dữ liệu thật: tools/data/osm.json (OpenStreetMap) + dem.json (SRTM)."""
import json, base64, io, struct, statistics, os
from PIL import Image, ImageDraw
T=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(f'{T}/data/dem.json')); osm=json.load(open(f'{T}/data/osm.json'))
# gộp thêm các lớp OSM mở rộng (osm_*.json) nếu có, bỏ trùng
import glob
for extra in sorted(glob.glob(f'{T}/data/osm_*.json')):
    e=json.load(open(extra))
    for k,v in e.items():
        seen={json.dumps(x,sort_keys=True,ensure_ascii=False) for x in osm.get(k,[])}
        osm.setdefault(k,[]).extend(x for x in v if json.dumps(x,sort_keys=True,ensure_ascii=False) not in seen)
W,H=d['W'],d['H']; LON0,LON1,LAT0,LAT1=d['lon0'],d['lon1'],d['lat0'],d['lat1']
hm=struct.unpack(f'<{W*H}H',base64.b64decode(d['b64']))
def h(lat,lon):
    fi=(lon-LON0)/(LON1-LON0)*(W-1); fj=(LAT1-lat)/(LAT1-LAT0)*(H-1)
    i=min(W-2,max(0,int(fi))); j=min(H-2,max(0,int(fj))); a=fi-i; b=fj-j
    return (hm[j*W+i]*(1-a)+hm[j*W+i+1]*a)*(1-b)+(hm[(j+1)*W+i]*(1-a)+hm[(j+1)*W+i+1]*a)*b
LW=1100; LH=round(LW*(LAT1-LAT0)/(LON1-LON0)*1.04)
P=lambda la,lo:((lo-LON0)/(LON1-LON0)*LW,(LAT1-la)/(LAT1-LAT0)*LH)
lake=[w for w in osm['water'] if w['name']=='Hồ Rào Quán'][0]
img=Image.new('L',(LW,LH),0); dr=ImageDraw.Draw(img)
for role,ring in lake['rings']:
    if role=='outer': dr.polygon([P(*p) for p in ring],fill=255)
for role,ring in lake['rings']:
    if role=='inner': dr.polygon([P(*p) for p in ring],fill=0)
buf=io.BytesIO(); img.save(buf,'PNG',optimize=True)
# mực nước = trung vị cao độ SRTM dọc đường bờ (SRTM đo năm 2000, trước khi tích nước)
edge=[h(*p) for role,ring in lake['rings'] for p in ring]
level=round(statistics.median(edge))
others=[{'name':w['name'],'kind':w['water'],'rings':[r for role,r in w['rings'] if role=='outer']} for w in osm['water'] if w['name']!='Hồ Rào Quán']
roads=[r for r in osm['roads']]
wind=[[a,b] for a,b,s in osm['wind'] if s=='wind']
rivers=[r for r in osm['rivers'] if len(r['pts'])>3]
places=[p for p in osm['places'] if p['name'] and not any('຀'<=c<='໿' for c in p['name']) and p['name']!='Davasan']
geo={'source':'OpenStreetMap contributors (ODbL), Overpass 2026-10-27','lake':base64.b64encode(buf.getvalue()).decode(),'lakeLevel':level,
     'roads':roads,'rivers':rivers,'waters':others,'wind':wind,'places':places}
json.dump(geo,open(f'{T}/data/geo.json','w'),ensure_ascii=False,separators=(',',':'))
print('lake level',level,'edge min/max',round(min(edge)),round(max(edge)),'| roads',len(roads),'rivers',len(rivers),'waters',len(others),'wind',len(wind),'places',len(places))
img.save('/tmp/claude-0/-home-claude/7ef2a531-4f32-5fdf-8118-f3b29d704b09/scratchpad/lake.png')
