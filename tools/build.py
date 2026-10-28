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
leaf = '<svg viewBox="0 0 40 40" aria-hidden="true"><path fill-rule="evenodd" d="M20 2 C 18.4 7.6 16.6 10.4 12.6 12 C 9.4 13.3 5.6 12.4 2 14.6 C 6.2 16.8 9 19.4 10 22.8 C 10.8 25.4 10 28.2 7.6 31 C 11.6 29.4 15.4 28.6 18.6 29.4 L 18.6 36.5 L 20 36.5 L 21.4 36.5 L 21.4 29.4 C 24.6 28.6 28.4 29.4 32.4 31 C 30 28.2 29.2 25.4 30 22.8 C 31 19.4 33.8 16.8 38 14.6 C 34.4 12.4 30.6 13.3 27.4 12 C 23.4 10.4 21.6 7.6 20 2 Z M20 7 L20.75 10 L20.95 28.2 L19.05 28.2 L19.25 10 Z" fill="#C44125"/></svg>'
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
