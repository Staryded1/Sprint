import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
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
        self.cursor = self.connection.cursor()

    def add_pass(self, data):
        query = """
        INSERT INTO passes (column1, column2, status) 
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (data['column1'], data['column2'], 'new'))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()