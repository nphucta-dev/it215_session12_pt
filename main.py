"""
1. Input / Output
Input: student_id (int) từ URL path.
Output thành công (200):
json{
  "message": "Xóa học viên thành công",
  "data": {
    "id": 1,
    "full_name": "Nguyen Van A",
    "email": "vana@gmail.com"
  }
}
Output thất bại (404):
json{
  "detail": "Học viên không tồn tại trong hệ thống"
}
2. Hai giải pháp
Giải pháp 1 — Query trước rồi xóa (Query-then-Delete):
Dùng db.query(Student).filter(Student.id == student_id).first() để lấy object thật từ DB, kiểm tra None, nếu có thì db.delete(obj) + db.commit().
Giải pháp 2 — Xóa trực tiếp bằng bulk delete (Query.delete()):
Dùng db.query(Student).filter(Student.id == student_id).delete(), hàm này trả về số dòng bị ảnh hưởng (rowcount). Nếu rowcount = 0 thì báo lỗi 404. Không cần lấy object trước.
Phần 2: So sánh & Lựa chọn
Tiêu chíGiải pháp 1 (Query-then-Delete)Giải pháp 2 (Bulk delete)Độ dễ hiểuCao, rõ ràng từng bướcTrung bình, dễ nhầm vì không thấy objectSố lượng code cần viếtNhiều hơn một chútÍt hơnKhả năng kiểm soát lỗiTốt, dễ log/trả về data đã xóaHạn chế, chỉ biết rowcountCó kiểm tra học viên tồn tại không?Có, kiểm tra None trước khi xóaCó, nhưng phải kiểm tra sau khi xóa (rowcount)Mức độ phù hợp với SQLAlchemy ORMRất phù hợp, đúng ORM pattern (tracked object)Ít phù hợp, bỏ qua ORM identity map, không trigger cascade/relationship eventsKhả năng tách logic vào ServiceDễ, trả về đầy đủ thông tin học viên đã xóaKhó, không có data để trả về cho response
Lựa chọn: Giải pháp 1
Lý do:

Cần trả về data (id, full_name, email) của học viên đã xóa trong response — bulk delete không cung cấp object nên không lấy được thông tin này sau khi xóa.
Đúng với bẫy đề bài: "không xóa trực tiếp object không lấy từ database" — Giải pháp 1 buộc phải query lấy object thật rồi mới delete, tránh được bẫy 2.
Phù hợp ORM: db.delete(obj) hoạt động với object đã được SQLAlchemy track (identity map), đảm bảo cascade/relationship (nếu có) hoạt động đúng.
"""

from fastapi import FastAPI
from database import Base, engine
from routers import student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(student_router.router)