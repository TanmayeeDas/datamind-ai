from psycopg2.extensions import connection


def read_database_schema(conn: connection):

    cursor = conn.cursor()

    schema = {}

    # Get all tables
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)

    tables = cursor.fetchall()

    for table in tables:

        table_name = table[0]

        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema='public'
            AND table_name=%s
            ORDER BY ordinal_position;
        """, (table_name,))

        columns = cursor.fetchall()

        schema[table_name] = {
            "columns": [column[0] for column in columns],
            "relationships": []
        }

    # Read foreign key relationships
    cursor.execute("""
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """)

    relationships = cursor.fetchall()

    for table, column, foreign_table, foreign_column in relationships:

        if table in schema:
            schema[table]["relationships"].append({
                "column": column,
                "references_table": foreign_table,
                "references_column": foreign_column
            })

    cursor.close()

    return schema