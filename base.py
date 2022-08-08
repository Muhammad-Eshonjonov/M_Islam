import sqlite3

class DBController:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def add_user(self, id, city, user_name):
        self.cursor.execute(
            f"INSERT INTO users VALUES('{id}', '{city}', 'today', '{user_name}');"
        )
        self.connection.commit()

    def update_city(self, id, city):
        self.cursor.execute(
            f"UPDATE users SET city = '{city}' WHERE id = '{id}'"
        )
        self.connection.commit()

    def update_day(self, id, day):
        self.cursor.execute(
            f"UPDATE users SET day = '{day}' WHERE id = '{id}'"
        )
        self.connection.commit()

    def delete_user(self, id):
        self.cursor.execute(
            f"DELETE FROM users WHERE id = '{id}'"
        )
        self.connection.commit()

    def get_user(self, id):
        self.cursor.execute(
            f"SELECT * FROM users WHERE id = '{id}'"
        )

        return self.cursor.fetchone()