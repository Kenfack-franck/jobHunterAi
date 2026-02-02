from pydantic import BaseModel, EmailStr

class ContactMessageRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str = ""
    message: str

class ContactMessageResponse(BaseModel):
    success: bool
    message: str
