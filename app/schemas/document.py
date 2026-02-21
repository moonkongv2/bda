from pydantic import BaseModel, Field
from typing import Optional, List

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
    file_path: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    contexts: List[str] = Field(default_factory=list)
