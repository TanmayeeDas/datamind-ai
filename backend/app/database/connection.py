import psycopg2
from psycopg2 import OperationalError


def create_connection(
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
):
    """
    Creates a PostgreSQL connection.
    """

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
        )

        return connection

    except OperationalError as e:
        raise Exception(f"Database Connection Failed: {e}")