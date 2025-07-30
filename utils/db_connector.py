import os
import pyodbc
from config.config import Config

def get_db_connection():
    conn = pyodbc.connect(Config.DB_CONNECTION_STRING)
    return conn

def fetch_data_from_table(table_name: str, start_date: str = None, end_date: str = None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        if start_date and end_date:
            query += f" WHERE Date >= '{start_date}' AND Date <= '{end_date}'"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            processed_row = []
            for item in row:
                if item is None:
                    # Determine default based on column type or context, for now, use 0 for numbers and '' for strings
                    # This is a generic approach, more specific handling might be needed based on schema
                    processed_row.append(0) if isinstance(item, (int, float)) else processed_row.append('')
                else:
                    processed_row.append(item)
            data.append(dict(zip(columns, processed_row)))
        return data
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate}")
        return None
    finally:
        if conn:
            conn.close()

def execute_custom_query(query: str):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            processed_row = []
            for item in row:
                if item is None:
                    # Assuming numeric columns should default to 0 if None
                    processed_row.append(0)
                else:
                    processed_row.append(item)
            data.append(dict(zip(columns, processed_row)))

        return data
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
