from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models import Student


def delete_student_service(db: Session, student_id: int):
    # Quy tắc 1: kiểm tra học viên tồn tại - lấy object thật từ DB (tránh Bẫy 2)
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại trong hệ thống"
        )

    # Lưu lại thông tin trước khi xóa để trả về cho client
    deleted_info = {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }

    try:
        # Quy tắc 2: chỉ delete khi đã tìm thấy student trong DB
        db.delete(student)
        # Quy tắc 3: bắt buộc commit để xác nhận xóa xuống MySQL (tránh Bẫy 3)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi hệ thống khi xóa học viên"
        )

    return deleted_info