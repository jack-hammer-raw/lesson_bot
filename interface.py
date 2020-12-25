import matplotlib.pyplot as plt
from telebot.types import ReplyKeyboardMarkup as RKM
from config import *
from database import SQLighter


def get_start():
    markup = RKM(True)
    markup.add(r"/start")
    return markup


def get_button_text(name):
    db = SQLighter("base.db")
    lessons = db.get_full_list_lessons(name)
    lessons = lessons.split('\n')
    lessons_count = 0
    if lessons != "empty":
        for i in lessons:
            lessons_count += int(i[-2])
    return f"{name} {lessons_count % 24}/24 [{lessons_count // 24}]"


def get_lessons_info(_id):
    markup = RKM()  # row_width=2
    markup.add(get_button_text(students[0]), get_button_text(students[1]))
    markup.add(get_button_text(students[2]), get_button_text(students[3]))
    markup.add(get_button_text(students[4]), get_button_text(students[5]))

    if _id in owners:
        markup.add("Расписание", "cash")
        if _id in admins:
            markup.add("Add lessons", "new payment")
    else:
        markup.add("Расписание")

    return markup


def get_add_lessons_board():
    markup = RKM()
    markup.add(get_button_text(students[0]).split()[0], get_button_text(students[1]).split()[0])
    markup.add(get_button_text(students[2]).split()[0], get_button_text(students[3]).split()[0])
    markup.add(get_button_text(students[4]).split()[0], get_button_text(students[5]).split()[0])
    markup.add("return")
    return markup


def get_lessons_count_buttons():
    markup = RKM(one_time_keyboard=True)
    markup.add("1", "2")
    markup.add("return")
    return markup


def return_button():
    markup = RKM()
    markup.add("return")
    return markup


def draw_plots(name):
    db = SQLighter("base.db")
    all_records = db.select_all_from_name(name)
    y_speed = []
    y_accuracy = []
    x = []
    for i in all_records:
        if i[-2]:
            y_speed.append(i[-3])
            y_accuracy.append(i[-2])
            x.append('.'.join(i[1].split('.')[:2]))
    fig, ax = plt.subplots(facecolor="lightgreen")
    ax.plot(x, y_speed, label="Скорость печати")
    ax.plot(x, y_accuracy, label="Аккуратность")

    typing_speed = str(y_speed[-1]) if y_speed else 0
    typing_accuracy = str(y_accuracy[-1]) if y_accuracy else 0

    plt.title(f"Скорость перчати [{typing_speed}]   Аккуратность [{typing_accuracy}]")
    plt.xlabel("Дата")
    plt.ylabel("Кол-во символов в минуту")
    ax.set_xticklabels(x)
    plt.legend()
    plt.savefig(f"imgs/{name}_plot")
    plt.clf()

def rander_plots():
    [draw_plots(name) for name in students]

def get_plot(name):
    result = ''
    with open(f"imgs/{name}_plot.png", "rb") as img:
        result = img
    return result

class States:
    def __init__(self):
        self._states = ["listening",
                        "add_lessons",
                        "add_lessons_count",
                        "add_typing_speed",
                        "add_typing_accuracy",
                        "new_payment",
                        "payment_comment",
                        ]
        self.state = "listening"

    def set_state(self, state):
        self.state = state

    def next_state(self):
        pass




if __name__ == "__main__":
    pass