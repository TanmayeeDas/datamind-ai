from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.database.schema_cache import DATABASE_SCHEMA
from app.services.prompt_builder import build_prompt
from app.services.llm_service import generate_sql

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

    return QueryResponse(sql=sql)