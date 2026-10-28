"""Ghép sa bàn 3D Mùa Phong Khe Sanh: python3 tools/build.py
  -> index.html        (trang đầy đủ, đưa lên hosting)
  -> artifact.html     (bản xem trước trên Claude)
Sửa giao diện/logic trong tools/sa-ban-template.html, dữ liệu trong tools/data/."""
import json, os, re
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
t = open(f'{T}/sa-ban-template.html', encoding='utf-8').read()
d = json.load(open(f'{T}/data/dem.json')); g = json.load(open(f'{T}/data/geo.json'))
dem = {k: d[k] for k in ['W', 'H', 'lon0', 'lon1', 'lat0', 'lat1', 'b64']}
pts = json.load(open(f'{T}/data/points.json'))
geo = {k: g.get(k, []) for k in ['lake', 'lakeLevel', 'roads', 'rivers', 'waters', 'wind', 'places']}
geo.update({k: pts[k] for k in ['boat', 'phong', 'ben', 'dam']})
placeholder = d.get('source') == 'placeholder' or g.get('placeholder')
leaf = '<svg viewBox="0 0 40 47" aria-hidden="true"><path d="M6 46 V20 C6 10 13 3 20 1 C27 3 34 10 34 20 V46 Z" fill="none" stroke="#F6E7C9" stroke-width="2.2" stroke-linejoin="round"/><rect x="18.9" y="28" width="2.2" height="12" fill="#F6E7C9"/><path d="M9 40.5 Q14.5 38.6 20 40.5 T31 40.5" fill="none" stroke="#F6E7C9" stroke-width="1.6" stroke-linecap="round"/><path d="M20 18 C24.55 24.6 30.4 28.2 33 30 Q20 27.8 7 30 C9.6 28.2 15.45 24.6 20 18 Z" fill="#C44125"/><path d="M20 12 C23.675 18.05 28.4 21.35 30.5 23 Q20 20.8 9.5 23 C11.6 21.35 16.325 18.05 20 12 Z" fill="#E07A2C"/><path d="M20 6.5 C22.8 12.0 26.4 15.0 28 16.5 Q20 14.3 12 16.5 C13.6 15.0 17.2 12.0 20 6.5 Z" fill="#E2B93B"/><path d="M20 2.0 C21.925 6.675 24.4 9.225 25.5 10.5 Q20 8.3 14.5 10.5 C15.6 9.225 18.075 6.675 20 2.0 Z" fill="#C44125"/></svg>'
t = (t.replace('__FONTS__', open(f'{T}/data/fonts.css').read())
      .replace('__DEM__', json.dumps(dem, separators=(',', ':')))
      .replace('__GEO__', json.dumps(geo, separators=(',', ':')))
      .replace('__LEAF__', leaf)
      .replace('__BADGE__', '<span class="badge">Bản xem trước · địa hình tạm</span>' if placeholder else '')
      .replace('__DATANOTE__', 'Địa hình, bờ hồ và tuyến đường hiện là bản dựng tạm, đang chờ thay bằng dữ liệu SRTM và OpenStreetMap.' if placeholder
               else 'Địa hình từ dữ liệu độ cao SRTM (AWS Terrain Tiles), bờ hồ và tuyến đường từ OpenStreetMap.'))
open(f'{ROOT}/index.html', 'w', encoding='utf-8').write(t)
# bản artifact: bỏ khung tài liệu, giữ nguyên nội dung head/body
a = re.sub(r'<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', t, count=1)
a = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', a, count=1)
a = a.replace('</head>\n<body>\n', '\n', 1).replace('</body>\n</html>\n', '')
open(f'{ROOT}/artifact.html', 'w', encoding='utf-8').write(a)
print('index.html', len(t), '| artifact.html', len(a), '| placeholder' if placeholder else '| real data')
