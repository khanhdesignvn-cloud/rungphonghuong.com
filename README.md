# Mùa Phong Khe Sanh · rungphonghuong.com
Sa bàn 3D rừng phong hương hồ Rào Quán (Khe Sanh, Quảng Trị) cho người trẻ khám phá: địa hình SRTM, đường và hồ từ OpenStreetMap, điểm đến đối chiếu Google Maps, trình chiếu, lưu ý an toàn và các nút dịch vụ (đặt tour, thuê thuyền, HDV, chụp hình, đặt xe, lưu trú, liên hệ).

- `index.html` – trang hoàn chỉnh, tĩnh, không cần máy chủ (GitHub Pages).
- `tools/sa-ban-template.html` – giao diện và logic; `tools/data/` – dữ liệu; `python3 tools/build.py` dựng lại `index.html`.
- Sửa liên hệ nhận yêu cầu: hằng `CONTACT` trong phần `DỊCH VỤ` của template.

Dữ liệu: SRTM qua AWS Terrain Tiles; © OpenStreetMap contributors (ODbL). Chữ: SVN Branding. Thư viện: three.js, d3-contour (CDN jsdelivr).
