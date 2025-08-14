# Laocai API (Django REST + JWT)
Triển khai nhanh **Phương án B**: Backend với đăng nhập (JWT), RBAC sơ bộ, CRUD cho **roads**, **assets**, **projects**.

## 1) Chạy nhanh với Docker (Postgres + PostGIS)
```bash
docker compose up -d --build
# Lần đầu: chạy migrate & tạo tài khoản mẫu
docker compose exec web python manage.py migrate
docker compose exec web python manage.py create_default_admin
# Kiểm tra API
curl http://localhost:8000/api/health
```

## 2) Đăng nhập (JWT)
```bash
curl -X POST http://localhost:8000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'
# Nhận access/refresh token
```

## 3) CRUD
- `GET /api/roads?kind=&owner_unit=&search=&ordering=length_km` (lọc + tìm kiếm + sắp xếp)
- `POST /api/roads` (cần quyền admin hoặc staff)
- `POST /api/import/roads` nạp JSON mảng roads (overwrite toàn bộ)
- Tương tự `/api/assets`, `/api/projects`
- `GET /api/reports/summary` KPI tổng hợp

## 4) Kết nối Frontend (Netlify)
Cấu hình domain của API (Render/Railway/Dokcer riêng) và sửa **app.js** bên frontend để gọi vào `https://<api-domain>/api/...`.

## 5) Triển khai miễn phí
### Tuỳ chọn A: Render
- New Web Service → Python → kết nối repo này.
- Build: `pip install -r requirements.txt`  
- Start: `gunicorn laocai_api.wsgi:application`
- Env:
  - `SECRET_KEY` = tạo chuỗi ngẫu nhiên
  - `DJANGO_DEBUG` = `false`
  - `ALLOWED_HOSTS` = `<render-service>.onrender.com,<domain-bạn>`
  - `DATABASE_URL` = URL Postgres (Neon/Supabase)
  - `CORS_ALLOWED_ORIGINS` = `https://quanly-giao-thong-lao-cai.netlify.app`
- "Shell" → chạy `python manage.py migrate && python manage.py create_default_admin`

### Tuỳ chọn B: Railway
- Tạo Postgres → lấy `DATABASE_URL`
- Deploy dịch vụ Python với thông số tương tự

> Ghi chú: PostGIS là *tuỳ chọn*; local Docker compose ở trên đã dùng PostGIS. Với Neon/Supabase, bật extension PostGIS nếu cần.

## 6) RBAC sơ bộ
- Mặc định **đọc công khai** (GET) và **ghi chỉ dành cho admin/staff**.
- Có thể mở rộng rule: lọc theo `unit` của người dùng (Owner/Commune).

## 7) Import dữ liệu mẫu
- `POST /api/import/roads` với payload là **mảng JSON**.
- Bạn có thể dùng file `roads.json` đã chuẩn hoá từ mình trước đó.
