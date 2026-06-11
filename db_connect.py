import sqlite3
def get_db_connection():
    # check_same_thread=False zaroori hai Streamlit ke liye 
    conn = sqlite3.connect("project_data.db", check_same_thread=False)
    return conn