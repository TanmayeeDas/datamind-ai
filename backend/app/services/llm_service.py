from openai import OpenAI
import json
import pandas as pd

from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_sql(prompt: str):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Remove Markdown code fences if the LLM adds them
    if sql.startswith("```"):
        sql = sql.replace("```sql", "", 1)
        sql = sql.replace("```", "", 1)
        sql = sql.strip()

    return sql



def generate_analysis_plan(
    question: str,
    dataframe: pd.DataFrame
):
    columns_info = [
        {
            "name": str(col),
            "dtype": str(dataframe[col].dtype)
        }
        for col in dataframe.columns
    ]

    prompt = f"""
You are an expert data analyst.

Understand the user's question and return a JSON
analysis plan for execution using Pandas.

Available columns and data types:
{json.dumps(columns_info)}

User question:
{question}

Return a JSON object with these fields:

{{
  "operation": "count_rows | list_columns | head |
                aggregate | groupby_aggregate |
                filter | top_n",
  "column": null,
  "group_by": null,
  "aggregation": null,
  "filter": null,
  "limit": 5
}}

Rules:
- Use only columns listed in the schema.
- count_rows: count rows.
- list_columns: list column names.
- head: show first N rows.
- aggregate: sum, mean, min, max, or count.
- groupby_aggregate: group by a column and aggregate
  another column.
- filter: filter using a column, operator, and value.
- top_n: rank rows or grouped results by a column.
- Use null for fields not required.
- For filter, use:
  {{"column": "column_name",
    "operator": "equals | greater_than |
                 less_than | contains",
    "value": "value"}}
- Never invent column names.
- Return JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return json.loads(
        response.choices[0].message.content
    )