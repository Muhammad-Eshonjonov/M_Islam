import sqlite3
import datetime

class DBController:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def add_user(self, id, city, user_name):
        self.cursor.execute(
            f"INSERT INTO users VALUES('{id}', '{city}', 'today', '{user_name}', '{str(datetime.datetime.now())}');"
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

    def update_last_use(self, id):
        self.cursor.execute(
            f"UPDATE users SET last_use = '{str(datetime.datetime.now())}' WHERE id = '{id}'"
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


    #Команды для Админов внизу :)

    def get_info_users(self):
        self.cursor.execute(
            "SELECT * FROM users"
        )
        k = 0
        answer = f"{'№'.ljust(5)} {'id'.ljust(10)} {'Город'.ljust(15)} {'день'.ljust(10)} {'username'.ljust(20)} {'Последное использование'}\n"
        for to in self.cursor.fetchall():
            k += 1
            answer += f"{str(k).ljust(5)} {to[0].ljust(10)} {to[1].ljust(15)} {to[2].ljust(10)} {to[3].ljust(20)} {to[4]}\n"

        end_answer = f"\n{k} - пользователей"
        return "<pre>\n" + answer + "</pre>" + end_answer

    def get_users(self):
        self.cursor.execute(
            "SELECT username FROM users"
        )
        answer = ""
        k = 0
        for to in self.cursor.fetchall():
            k += 1
            answer += f'{(str(k)+".").ljust(5)} <a href = "t.me/{to[0]}/">{to[0]}</a>\n'

        answer += "\n"
        answer += f"{k} - пользователей"

        return answer