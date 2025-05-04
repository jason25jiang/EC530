# cli.py
import sqlite3
import os

def start_cli_interaction(db_name):
    """Start an interactive CLI for interacting with SQLite."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        print("Welcome to the SQLite CLI!")
        
        while True:
            user_input = input("Enter a command (load CSV, run SQL, list tables, exit): ").lower()
            
            if user_input == 'load csv':
                file_name = input("Enter CSV file path: ")
                load_csv_to_sqlite(file_name, db_name)
            elif user_input == 'run sql':
                sql_query = input("Enter the SQL query to execute: ")
                cursor.execute(sql_query)
                results = cursor.fetchall()
                for row in results:
                    print(row)
            elif user_input == 'list tables':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print("Tables in the database:")
                for table in tables:
                    print(table[0])
            elif user_input == 'exit':
                print("Exiting the program.")
                break
            else:
                print("Invalid command.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def load_csv_to_sqlite(csv_file, db_name):
    """Load CSV file into SQLite."""
    import pandas as pd
    
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    df.to_sql(name='data_table', con=conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    db_name = input("Enter SQLite database name: ")
    start_cli_interaction(db_name)
