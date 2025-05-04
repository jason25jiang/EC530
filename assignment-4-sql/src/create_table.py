import pandas as pd
import sqlite3
import os

def create_table_from_csv(csv_file, db_name):
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Dynamically generate column definitions based on DataFrame column types
        columns = ', '.join([f"{col} {get_sqlite_type(df[col])}" for col in df.columns])
        
        create_table_query = f"CREATE TABLE IF NOT EXISTS {csv_file.split('.')[0]} ({columns});"
        
        cursor.execute(create_table_query)
        
        # Insert data into the table
        df.to_sql(name=csv_file.split('.')[0], con=conn, if_exists='replace', index=False)
        conn.commit()
        
        print(f"Table created and data loaded for {csv_file}.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def get_sqlite_type(series):
    if series.dtype == 'int64':
        return 'INTEGER'
    elif series.dtype == 'float64':
        return 'REAL'
    else:
        return 'TEXT'

if __name__ == "__main__":
    csv_file = input("Enter CSV file path: ")
    db_name = input("Enter SQLite database name: ")
    create_table_from_csv(csv_file, db_name)
