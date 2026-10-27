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
leaf = ('<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 4 C23 10 25 12 31 11 C29 16 30 19 36 22 C29 24 26 25 25 29 '
        'L21 27 L21 37 L19 37 L19 27 L15 29 C14 25 11 24 4 22 C10 19 11 16 9 11 C15 12 17 10 20 4Z" fill="#C44125" '
        'stroke="#FBF4E3" stroke-width="1.6" stroke-linejoin="round"/><path d="M20 27 L20 9 M20 25 L11 15 M20 25 L29 15" '
        'stroke="#FBF4E3" stroke-width="1.1" fill="none" opacity=".75"/></svg>')
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
