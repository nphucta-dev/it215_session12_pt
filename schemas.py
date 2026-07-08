from pydantic import BaseModel


class StudentOut(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True


class DeleteStudentResponse(BaseModel):
    message: str
    data: StudentOut