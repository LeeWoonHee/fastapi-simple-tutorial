from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQL 연결 URL
DATABASE_URL = "postgresql+psycopg2://postgres:6399@localhost:5432/fastapi-eric"

# PostgreSQL에서는 connect_args={"check_same_thread": False}가 필요하지 않음 (SQLite 전용)
engine = create_engine(DATABASE_URL)

# 오타 수정: SesstionLocal -> SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()  # 수정된 이름 사용
    try:
        yield db
    finally:
        db.close()
