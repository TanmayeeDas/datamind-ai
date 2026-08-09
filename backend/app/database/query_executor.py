from psycopg2.extensions import connection
from psycopg2 import Error


def execute_query(conn: connection, sql: str):

    cursor = conn.cursor()

    try:
        cursor.execute(sql)

        columns = [description[0] for description in cursor.description]

        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }

    except Error as e:
        raise Exception(f"Query execution failed: {e}")

    finally:
        cursor.close()