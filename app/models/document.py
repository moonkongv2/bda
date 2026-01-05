from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import Base # 기존 Base 가져오기

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=True) # 문서 내용 (나중에 RAG용)
    file_path = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id")) # 누구 꺼니?

    # 유저 모델과의 관계 설정 (선택사항이지만 편리함)
    owner = relationship("User", back_populates="documents")
