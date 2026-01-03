from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass # 생성할 때 입력받을 데이터

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
