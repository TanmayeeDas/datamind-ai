import sqlglot
from sqlglot import expressions


FORBIDDEN_OPERATIONS = [
    "delete",
    "update",
    "insert",
    "drop",
    "alter",
    "truncate",
]


def validate_question(question: str) -> bool:
    """
    Checks whether the user's question is asking
    for a database modification operation.
    """

    question_lower = question.lower()

    for operation in FORBIDDEN_OPERATIONS:
        if operation in question_lower:
            return False

    return True


def validate_sql(sql: str) -> bool:
    """
    Allows only SELECT SQL statements.
    """

    try:
        parsed = sqlglot.parse_one(sql)

        return isinstance(parsed, expressions.Select)

    except Exception:
        return False