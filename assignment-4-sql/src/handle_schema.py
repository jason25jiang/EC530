# handle_schema.py
import pandas as pd
import sqlite3
import os

def handle_schema_conflict(csv_file, db_name):
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        table_name = csv_file.split('.')[0]
        
        # Check if the table already exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_schema = cursor.fetchall()
        
        if existing_schema:
            print(f"Table {table_name} already exists.")
            action = input("Do you want to (O)verwrite, (R)ename, or (S)kip? ").lower()
            
            if action == 'o':
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                create_table_from_csv(csv_file, db_name)
            elif action == 'r':
                new_name = input("Enter new table name: ")
                df.to_sql(new_name, conn, if_exists='replace', index=False)
            else:
                print("Skipping table creation.")
        else:
            print(f"Creating table {table_name}.")
            create_table_from_csv(csv_file, db_name)
        
        conn.commit()
    except Exception as e:
        print(f"Error handling schema conflict: {e}")
    finally:
        conn.close()

def create_table_from_csv(csv_file, db_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    columns = ', '.join([f"{col} {get_sqlite_type(df[col])}" for col in df.columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {csv_file.split('.')[0]} ({columns})"
    
    cursor.execute(create_table_query)
    df.to_sql(name=csv_file.split('.')[0], con=conn, if_exists='replace', index=False)
    conn.commit()

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
    handle_schema_conflict(csv_file, db_name)
