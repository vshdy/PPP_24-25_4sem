from pydantic import BaseModel
from typing import Dict
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr 
    password: str

class UserLogin(UserCreate):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    token: str

class EncodeRequest(BaseModel):
    text: str
    key: str

class DecodeRequest(BaseModel):
    encoded_data: str
    key: str
    huffman_codes: Dict[str, str]
    padding: int

class EncodeResponse(BaseModel):
    task_id: str

class DecodeResponse(BaseModel):
    task_id: str
