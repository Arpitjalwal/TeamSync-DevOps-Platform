import pandas as pd
import sqlite3
from backend.db_connect import get_db_connection

def run_sql_query(query):
    """
    Ek versatile function jo SELECT aur DML/DDL (INSERT/UPDATE/DELETE/CREATE) 
    dono queries ko handle karta hai.
    """
    try:
        # --- Naya Logic: User friendly commands ke liye ---
        clean_query = query.strip().upper()
        if clean_query == "SHOW TABLES;":
            query = "SELECT name FROM sqlite_master WHERE type='table';"
        # --------------------------------------------------

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query execute karo
        cursor.execute(query)
        
        # Check karo agar ye SELECT query hai
        if cursor.description:
            # Result ko DataFrame mein lao
            data = pd.read_sql_query(query, conn)
            conn.close()
            return {"data": data, "error": None}
        else:
            # Ye CRUD ya DDL query hai (INSERT/UPDATE/DROP etc.)
            conn.commit()
            conn.close()
            return {"data": None, "error": None} # Success
            
    except Exception as e:
        return {"data": None, "error": str(e)}

def initialize_db():
    """Database connection initialize karne ke liye."""
    conn = get_db_connection()
    conn.close()

def drop_table(table_name):
    """Specific table delete karne ke liye."""
    conn = get_db_connection()
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()

def reset_entire_db():
    """Saari tables delete karke database ko reset karne ke liye."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Saari tables ki list nikalo
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE {table[0]}")
    conn.commit()
    conn.close()
