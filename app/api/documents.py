from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate

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

@router.get("/{doc_id}", response_model=DocumentResponse)
def read_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    # 404 error if doc is not found
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 403 error if the doc is not owned by user(user_id)
    if doc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return doc

@router.put("/{doc_id}", response_model=DocumentResponse)
def update_document(
    doc_id: int,
    doc_in: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = doc_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doc, key, value)

    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(doc)
    db.commit()
    return {"status": "deleted", "id": doc_id}
