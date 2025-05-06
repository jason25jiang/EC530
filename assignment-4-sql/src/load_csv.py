import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_file, db_name):
    try:
        db_name = db_name + ".db"
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_name)
        df.to_sql(name='data_table', con=conn, if_exists='replace', index=False)
        
        print(f"Data from {csv_file} has been successfully loaded into {db_name}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    csv_file = input("Enter CSV file path: ")
    db_name = input("Enter SQLite database name: ")
    load_csv_to_sqlite(csv_file, db_name)
