from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import DeleteStudentResponse
from services.student_service import delete_student_service

router = APIRouter(prefix="/students", tags=["Students"])


@router.delete("/{student_id}", response_model=DeleteStudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = delete_student_service(db, student_id)
    return {
        "message": "Xóa học viên thành công",
        "data": deleted_student
    }