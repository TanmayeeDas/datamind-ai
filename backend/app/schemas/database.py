from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str


class DatabaseConnectionResponse(BaseModel):
    success: bool
    message: str