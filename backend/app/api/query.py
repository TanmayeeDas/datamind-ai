from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.database.schema_cache import DATABASE_SCHEMA
from app.database.connection import create_connection
from app.database.query_executor import execute_query

from app.services.prompt_builder import build_prompt
from app.services.llm_service import generate_sql

from app.utils.sql_validator import validate_sql


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post("/generate", response_model=QueryResponse)
def generate_query(request: QueryRequest):

    prompt = build_prompt(
        DATABASE_SCHEMA,
        request.question
    )

    sql = generate_sql(prompt)

    if not validate_sql(sql):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT queries are allowed."
        )

    connection = create_connection(
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
    )

    try:

        result = execute_query(
            connection,
            sql
        )

    finally:

        connection.close()

    return QueryResponse(
        sql=sql,
        columns=result["columns"],
        rows=result["rows"]
    )