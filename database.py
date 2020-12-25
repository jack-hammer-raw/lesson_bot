from operator import itemgetter
import sqlite3
from config import students, ONE_LESSON_COST
from datetime import datetime


def get_record(x):
    return f"{x[0]}.{x[1]}.{x[2]}   ({x[3]})"


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_all_from_name(self, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM archive WHERE name = '{name}'").fetchall()

    def close(self):
        self.connection.close()

    def get_full_list_lessons(self, name):
        all_records = self.select_all_from_name(name)
        res = []
        for row in all_records:
            res.append((row[1].split('.') + [str(row[2])]))
        if res:
            res = sorted(res, key=itemgetter(2, 1, 0))
            res = map(get_record, res)
            return '\n'.join(res)
        return 'empty'

    def get_payments_list(self):
        with self.connection:
            res = []
            all_results = self.cursor.execute(f"SELECT * FROM payments").fetchall()
            all_payments = 0
            for i in all_results:
                comment = f"({i[-1]})" if i[-1] else ''
                res.append(f"{i[0]}     {i[1]} {comment}")
                all_payments += i[1]
            if res:
                return res, all_payments
            return "empty", all_payments

    def add_new_payment(self, value, comment=''):
        date = datetime.now().date().strftime("%d.%m.%Y")
        with self.connection:
            self.cursor.execute(f"INSERT INTO payments VALUES('{date}', {value}, '{comment}')")

    def get_cash(self):
        full_cash = 0
        for name in students:
            with self.connection:
                command = f"SELECT lessons_count, lesson_cost FROM archive WHERE name = '{name}'"
                all_records = self.cursor.execute(command).fetchall()
                for i in all_records:
                    full_cash += i[0] * i[1]
        payments_list, payments_sum = self.get_payments_list()
        res = '\n'.join(payments_list) + '\n\n' + f"Текущий баланс - {full_cash - payments_sum}"
        return res

    def add_row_in_archive(self, name, lessons_count, typing_speed, date='', lesson_cost=ONE_LESSON_COST):
        if not date:
            date = datetime.now().date().strftime("%d.%m.%Y")
        with self.connection:
            self.cursor.execute(f"INSERT INTO archive VALUES('{name}', '{date}', {lessons_count}," +
                                f"{typing_speed}, {lesson_cost})")




if __name__ == "__main__":
    db = SQLighter("base.db")
    db.get_cash()
#





