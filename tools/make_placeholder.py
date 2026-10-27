"""Dữ liệu TẠM cho sa bàn Khe Sanh (chạy: python3 tools/make_placeholder.py).
Vị trí điểm đã kiểm tra với Google Maps (27/10/2026). Địa hình, bờ hồ và đường là PHỎNG ĐOÁN,
sẽ thay bằng SRTM (AWS Terrain Tiles) + OpenStreetMap khi lấy được qua trình duyệt.
"""
import json, math, base64, io, os
from PIL import Image, ImageDraw, ImageFilter
T = os.path.dirname(os.path.abspath(__file__))
LON0, LON1, LAT0, LAT1 = 106.565, 106.805, 16.580, 16.745
W, H = 240, 170
LAKE_LEVEL = 460

LAKE = [[16.716,106.666],[16.7215,106.673],[16.7185,106.681],[16.7235,106.690],[16.7205,106.699],[16.7245,106.706],
        [16.7190,106.714],[16.7220,106.725],[16.7170,106.735],[16.7160,106.746],[16.7090,106.749],[16.7065,106.741],
        [16.7090,106.732],[16.7020,106.726],[16.7045,106.716],[16.6975,106.709],[16.6935,106.700],[16.6985,106.693],
        [16.7010,106.686],[16.7040,106.678],[16.7080,106.671]]
ISLE = [[16.7108,106.6825],[16.7122,106.6852],[16.7112,106.6880],[16.7094,106.6872],[16.7090,106.6842]]

def to_px(lat, lon, w, h):
    return ((lon-LON0)/(LON1-LON0)*w, (LAT1-lat)/(LAT1-LAT0)*h)

# ---- lake mask ----
LW, LH = 960, 680
img = Image.new('L', (LW, LH), 0); d = ImageDraw.Draw(img)
d.polygon([to_px(a, b, LW, LH) for a, b in LAKE], fill=255)
d.polygon([to_px(a, b, LW, LH) for a, b in ISLE], fill=0)
img = img.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 127 else 0)
buf = io.BytesIO(); img.save(buf, 'PNG', optimize=True)
lake_b64 = base64.b64encode(buf.getvalue()).decode()
mask = img.load()

# ---- DEM (phỏng đoán) ----
HILLS = [  # lat, lon, cao (m), bán kính km
    (16.6897, 106.6618, 881, 1.6),   # Cu Vơ – Đồi 881 Nam
    (16.733, 106.700, 760, 2.2), (16.736, 106.728, 720, 2.0), (16.742, 106.676, 820, 2.4),
    (16.688, 106.632, 700, 2.5), (16.660, 106.600, 560, 3.0), (16.700, 106.780, 640, 2.5),
    (16.596, 106.775, 600, 2.6), (16.585, 106.700, 520, 3.0), (16.675, 106.760, 560, 2.0),
]
def elev(lat, lon):
    kx = 111.32*math.cos(math.radians(16.66)); ky = 110.57
    h = 420
    for la, lo, hh, r in HILLS:
        dx = (lon-lo)*kx; dy = (lat-la)*ky
        h = max(h, h + (hh-420)*math.exp(-(dx*dx+dy*dy)/(r*r)))
    # thung lũng Sê Pôn phía tây (Lao Bảo thấp)
    h -= max(0, (106.63-lon))*2600
    # thung lũng sông Rào Quán đổ về Khe Sanh
    h -= 60*math.exp(-((lon-106.745)*kx)**2/1.2)
    return max(160, h)
grid = []
for j in range(H):
    lat = LAT1-(j/(H-1))*(LAT1-LAT0)
    for i in range(W):
        lon = LON0+(i/(W-1))*(LON1-LON0)
        h = elev(lat, lon)
        x, y = to_px(lat, lon, LW, LH)
        if mask[min(LW-1, int(x)), min(LH-1, int(y))]: h = LAKE_LEVEL-10
        grid.append(int(round(h)))
raw = b''.join(int(v).to_bytes(2, 'little') for v in grid)
json.dump({'W': W, 'H': H, 'lon0': LON0, 'lon1': LON1, 'lat0': LAT0, 'lat1': LAT1, 'b64': base64.b64encode(raw).decode(),
           'source': 'placeholder'}, open(f'{T}/data/dem.json', 'w'))

ql9= [[16.6125,106.565],[16.6106,106.588],[16.6060,106.620],[16.6004,106.668],[16.6090,106.698],[16.6230,106.722],[16.6351,106.7415],[16.6320,106.770],[16.6255,106.805]]
hcm=[[16.580,106.752],[16.6050,106.7470],[16.6351,106.7415],[16.6537,106.7262],[16.6700,106.7090],[16.6840,106.6880],[16.6990,106.6770],[16.7128,106.6745],[16.7300,106.6700],[16.745,106.6650]]
boat=[[16.7130,106.6762],[16.7118,106.6790],[16.7110,106.6820],[16.7080,106.6850],[16.7055,106.6820],[16.7060,106.6790],[16.7090,106.6770],[16.7122,106.6762]]
geo = {'placeholder': True, 'lakeLevel': LAKE_LEVEL, 'lake': lake_b64,
       'roads': [{'hw':'trunk','ref':'QL9','name':'Quốc lộ 9','pts':ql9},{'hw':'trunk','ref':'','name':'Đường Hồ Chí Minh','pts':hcm}]}
json.dump(geo, open(f'{T}/data/geo.json', 'w'))
# điểm biên tập tay (giữ nguyên khi thay dữ liệu thật)
if not os.path.exists(f'{T}/data/points.json'):
    json.dump({'boat': boat, 'phong': {'lat': 16.7085, 'lon': 106.6810, 'r_km': 1.1}}, open(f'{T}/data/points.json','w'), indent=1)
print('dem', W, H, 'min/max', min(grid), max(grid), '| lake png', len(lake_b64))
