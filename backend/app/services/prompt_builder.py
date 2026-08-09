def build_prompt(schema: dict, question: str) -> str:

    prompt = f"""
You are an expert PostgreSQL SQL generator.

Database Schema:
{schema}

Rules:
1. Generate ONLY PostgreSQL SQL.
2. Return ONLY SQL.
3. Do not explain anything.
4. Use only tables and columns from the schema.
5. Generate only SELECT queries.

User Question:
{question}
"""

    return prompt