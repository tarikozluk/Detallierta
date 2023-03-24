import pyodbc
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("../.env")

sql_server_conn = pyodbc.connect(os.getenv("SQL_SERVER_CONN"))
sql_server_conn_cursor = sql_server_conn.cursor()

def sql_error_logs(command):
    try:
        sql_server_conn_cursor.execute(
            "INSERT INTO ErrorLogs_Mobile (LogType, LogMessage, LogDate) VALUES (?,?,?)",
            ('Error', command, datetime.now()))

        sql_server_conn_cursor.commit()
    except:
        print("SQL Error Logs cannot be fetched")