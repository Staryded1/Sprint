import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv('FSTR_DB_NAME'),
            user=os.getenv('FSTR_DB_USER'),
            password=os.getenv('FSTR_DB_PASSWORD'),
            host=os.getenv('FSTR_DB_HOST'),
            port=os.getenv('FSTR_DB_PORT')
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def add_pass(self, data):
        query = """
        INSERT INTO passes (column1, column2, status) 
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (data['column1'], data['column2'], 'new'))
        self.connection.commit()

    def get_pass(self, pass_id):
        query = "SELECT * FROM passes WHERE id = %s"
        self.cursor.execute(query, (pass_id,))
        return self.cursor.fetchone()

    def update_pass(self, pass_id, data):
        set_clause = ", ".join(f"{key} = %s" for key in data.keys())
        query = f"UPDATE passes SET {set_clause} WHERE id = %s AND status = 'new'"
        self.cursor.execute(query, (*data.values(), pass_id))
        self.connection.commit()
        return self.cursor.rowcount

    def get_passes_by_email(self, email):
        query = """
        SELECT * FROM passes 
        WHERE user_email = %s
        """
        self.cursor.execute(query, (email,))
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()