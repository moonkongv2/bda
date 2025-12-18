from app.db.session import engine
from app.models.user import Base
# 모델들을 import 해줘야 Base가 "아, 이런 테이블을 만들어야 하는구나" 하고 알 수 있음!
from app.models.user import User
from app.models.document import Document

def init_db():
    Base.metadata.create_all(bind=engine)
