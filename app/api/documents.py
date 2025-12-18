from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("", response_model=DocumentResponse)
def create_document(
    doc_in: DocumentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 인증된 유저만 가능!
):
    db_doc = Document(
        **doc_in.model_dump(),
        owner_id=current_user.id # 현재 로그인한 유저 ID를 자동으로 넣음
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("", response_model=List[DocumentResponse])
def read_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 내가 올린 문서만 조회하기
    return db.query(Document).filter(Document.owner_id == current_user.id).all()