from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.database.schema_cache import DATABASE_SCHEMA
from app.services.prompt_builder import build_prompt
from app.services.llm_service import generate_sql
from app.utils.sql_validator import validate_question, validate_sql


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post("/generate", response_model=QueryResponse)
def generate_query(request: QueryRequest):

    # Validate user's request before calling the LLM
    if not validate_question(request.question):
        raise HTTPException(
            status_code=400,
            detail="Only read-only SELECT questions are allowed."
        )

    prompt = build_prompt(
        DATABASE_SCHEMA,
        request.question
    )

    sql = generate_sql(prompt)

    # Validate generated SQL
    if not validate_sql(sql):
        raise HTTPException(
            status_code=400,
            detail="Generated SQL is not a valid SELECT query."
        )

    return QueryResponse(sql=sql)