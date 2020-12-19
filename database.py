from operator import itemgetter
import sqlite3
from config import students
from datetime import datetime


def get_record(x):
    return f"{x[0]}.{x[1]}.{x[2]}   ({x[3]})"


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_all_from_name(self, name):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM students WHERE name = '{name}'").fetchall()

    def close(self):
        self.connection.close()

    def get_full_list_lessons(self, name):
        all_records = self.select_all_from_name(name)
        res = []
        for row in all_records:
            res.append((row[-2].split('.') + [str(row[-1])]))
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
                res.append(f"{str(i[-1]).zfill(4)}  {i[-2]}")
                all_payments += i[-1]
            if res:
                return res, all_payments
            return "empty", all_payments

    def get_cash(self):
        with self.connection:
            all_records = []
            for name in students:
                temp = self.cursor.execute(f"SELECT lessons_count FROM students WHERE name = '{name}'").fetchall()
                if temp:
                    all_records.extend(i[0] for i in temp)
            payments_list, payments_sum = self.get_payments_list()
            res = '\n'.join(payments_list) + '\n\n' + str(sum(map(int, all_records)) * 150 - payments_sum)
            return res

    def add_lesson(self, name, count):
        date = datetime.now().date().strftime("%d.%m.%Y")
        number = self._get_next_number()
        with self.connection:
            self.cursor.execute(f"INSERT INTO students VALUES({number}, '{name}', '{date}', {count})")

    def _get_next_number(self):
        res = len(self.cursor.execute(f"SELECT * FROM students").fetchall()) + 1
        return res




















