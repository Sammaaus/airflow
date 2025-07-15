from sqlalchemy import create_engine

def run_sql():
    # Connect to your PostgreSQL database
    engine = create_engine('postgresql+psycopg2://postgres@localhost/news_db')

    # Define your SQL
    sql_commands = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO test_table (name) VALUES ('Hello Airflow');
    """

    # Execute SQL
    with engine.connect() as conn:
        for cmd in sql_commands.strip().split(';'):
            if cmd.strip():
                conn.execute(cmd)
    print("✅ SQL commands executed successfully.")

# Run the function
if __name__ == '__main__':
    run_sql()
