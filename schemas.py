from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int

    class Config:
        from_attributes = True  # SQLAlchemy 객체에서 데이터 읽기
        validate_assignment = True  # 값 할당 시 검증
        str_strip_whitespace = True  # 문자열 앞뒤 공백 제거
        