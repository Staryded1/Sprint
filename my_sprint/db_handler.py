import psycopg2

class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='sprint', 
                user='postgres', 
                password='killer*10', 
                host='localhost', 
                port='5432'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error while connecting to the database: {e}")
            self.conn = None
            self.cursor = None

    def add_pass(self, data):
        if self.conn is None or self.cursor is None:
            print("Database connection is not established.")
            return False

        try:
            print("Data to insert:", data)  # Отладочный принт
            query = """
            INSERT INTO passes (name, latitude, longitude, user_email, additional_info, status)
            VALUES (%s, %s, %s, %s, %s, 'new')
            """
            self.cursor.execute(query, (
                data['name'], 
                data['latitude'], 
                data['longitude'], 
                data['user_email'], 
                data['additional_info']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            if self.conn:
                self.conn.rollback()
            return False