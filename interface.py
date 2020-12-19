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
            print(i)
            lessons_count += int(i[-2])
    return f"{name} {lessons_count % 24}/24 [{lessons_count // 24}]"
    

def get_lessons_info(_id):
    markup = RKM()
    markup.add(get_button_text(students[0]), get_button_text(students[1]))
    markup.add(get_button_text(students[2]), get_button_text(students[3]))
    markup.add(get_button_text(students[4]), get_button_text(students[5]))

    if _id in owners or _id in admins:
        markup.add("Расписание", "cash")
        if _id in admins:
            markup.add("Add today", "Add custom")
    else:
        markup.add("Расписание")
    return markup

def get_add_lessons_board():
    markup = RKM()
    markup.add(get_button_text(students[0]).split()[0], get_button_text(students[1]).split()[0])
    markup.add(get_button_text(students[2]).split()[0], get_button_text(students[3]).split()[0])
    markup.add("return")
    return markup

def get_lessons_count_buttons():
    markup = RKM()
    markup.add("1", "2")
    markup.add("return")
    return markup