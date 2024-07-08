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
            # Вставка данных пользователя
            user_data = data['user']
            user_query = """
            INSERT INTO users (email, fam, name, otc, phone)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE 
            SET fam = EXCLUDED.fam, name = EXCLUDED.name, otc = EXCLUDED.otc, phone = EXCLUDED.phone
            RETURNING id
            """
            self.cursor.execute(user_query, (
                user_data['email'], 
                user_data['fam'], 
                user_data['name'], 
                user_data['otc'], 
                user_data['phone']
            ))
            user_id = self.cursor.fetchone()[0]

            # Вставка координат
            coords_data = data['coords']
            coords_query = """
            INSERT INTO coords (latitude, longitude, height)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            self.cursor.execute(coords_query, (
                coords_data['latitude'], 
                coords_data['longitude'], 
                coords_data['height']
            ))
            coords_id = self.cursor.fetchone()[0]

            # Вставка перевала
            pass_query = """
            INSERT INTO pereval_added (beauty_title, title, other_titles, connect, add_time, user_id, coords_id, level_winter, level_summer, level_autumn, level_spring, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(pass_query, (
                data['beauty_title'],
                data['title'],
                data.get('other_titles', None),
                data.get('connect', None),
                data['add_time'],
                user_id,
                coords_id,
                data.get('level_winter', None),
                data['level_summer'],
                data['level_autumn'],
                data.get('level_spring', None),
                data['status']
            ))

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            if self.conn:
                self.conn.rollback()
            return False
