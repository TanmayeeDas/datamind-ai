from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    host: str
    port: int
    database: str
    username: str
    password: str


class QueryResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list