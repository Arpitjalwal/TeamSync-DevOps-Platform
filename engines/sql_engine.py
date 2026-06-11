import pandas as pd
import sqlite3
from backend.db_connect import get_db_connection

def run_sql_query(query):
    """
    Ek versatile function jo SELECT aur DML/DDL (INSERT/UPDATE/DELETE/CREATE) 
    dono queries ko handle karta hai.
    """
    try:
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

# Baki purane functions waise hi rahenge
def initialize_db():
    conn = get_db_connection()
    conn.close()

def drop_table(table_name):
    conn = get_db_connection()
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.close()

def reset_entire_db():
    # Saari tables delete karne ka logic
    pass
