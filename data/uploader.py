import os
import pandas as pd
import psycopg2
from psycopg2 import sql
import time


time.sleep(6.0)

# PostgreSQL database configuration
db_config = {
    "dbname": "my_database",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": "5432",
}

# Function to drop table if it exists
def drop_table(table_name, conn):
    with conn.cursor() as cursor:
        drop_table_query = sql.SQL("DROP TABLE IF EXISTS {}").format(
            sql.Identifier(table_name)
        )
        cursor.execute(drop_table_query)
        conn.commit()

# Function to upload CSV files to PostgreSQL
def upload_csv_to_postgres(csv_file, table_name, conn):
    df = pd.read_csv(csv_file, dtype=str)
    columns = list(df.columns)

    # Create table if not exists
    with conn.cursor() as cursor:
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(
                sql.Identifier(col) + sql.SQL(" VARCHAR") for col in columns
            ),
        )
        cursor.execute(create_table_query)
        conn.commit()

    # Insert data into the table
    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(map(sql.Placeholder, columns)),
            )
            data = {col: row[col] for col in columns}
            cursor.execute(insert_query, data)
        conn.commit()


# Main function to upload all CSV files in the local folder
def main():
    conn = None  # Initialize the connection variable
    try:
        # Establish database connection
        conn = psycopg2.connect(**db_config)

        # Get list of CSV files in the current directory
        csv_files = [file for file in os.listdir() if file.endswith(".csv")]

        # Drop existing tables and upload new data
        for csv_file in csv_files:
            table_name = os.path.splitext(csv_file)[0]  # Use CSV filename as table name
            drop_table(table_name, conn)  # Drop table if it exists
            upload_csv_to_postgres(csv_file, table_name, conn)  # Upload new data
            print(f"Uploaded data from {csv_file} to table {table_name}.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close database connection
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
