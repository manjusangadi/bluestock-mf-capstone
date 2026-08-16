import sqlite3
import os

DB_PATH = "bluestock_mf.db"

def get_connection(db_path=DB_PATH):
    """
    Establish a connection to the SQLite database and enable foreign keys.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

if __name__ == "__main__":
    print(f"Connecting to database at: {os.path.abspath(DB_PATH)}")
    try:
        conn = get_connection()
        print("Database Connected successfully.")
        
        cursor = conn.cursor()
        
        # Print SQLite version
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        print(f"SQLite Version: {version}")
        
        # Fetch and list tables
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print("\nExisting Tables in Database:")
        if tables:
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"  - {table} ({count} rows)")
        else:
            print("  (No tables found. Please run db_loading.py to apply schema and load data.)")
            
        conn.close()
    except Exception as e:
        print(f"Database Connection failed: {e}")