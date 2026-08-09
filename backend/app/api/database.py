from fastapi import APIRouter

from app.database.connection import create_connection
from app.schemas.database import (
    DatabaseConnectionRequest,
    DatabaseConnectionResponse,
)

from app.database.schema_reader import read_database_schema
from app.database.schema_cache import DATABASE_SCHEMA

router = APIRouter(prefix="/database", tags=["Database"])


@router.post("/connect", response_model=DatabaseConnectionResponse)
def connect_database(request: DatabaseConnectionRequest):

    connection = create_connection(
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
    )

    schema = read_database_schema(connection)

    DATABASE_SCHEMA.clear()
    DATABASE_SCHEMA.update(schema)

    connection.close()

    return DatabaseConnectionResponse(
        success=True,
        message="Database connected successfully."
    )
@router.post("/tables")
def get_database_tables(request: DatabaseConnectionRequest):

    connection = create_connection(
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
    )

    schema = read_database_schema(connection)

    connection.close()

    return schema


@router.get("/schema")
def get_schema():
    return DATABASE_SCHEMA