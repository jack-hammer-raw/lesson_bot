from config import *
from interface import *
from database import SQLighter
import telebot

bot = telebot.TeleBot(TOKEN)
db = SQLighter("base.db")

say = bot.send_message

add_lesson = False

add_lesson_name = ''


def non_user_answer(_id):
    say(_id, "Отправлена заявка на добавление", reply_markup=get_start())


def new_user(_id, name):
    say(admins[0], str(_id) + ' ' + name + " Добавил(а) заявку на добавление")


@bot.message_handler(commands=["start"])
def main(msg):
    _id = msg.chat.id
    if _id not in users:
        non_user_answer(_id)
        new_user(_id, msg.chat.first_name)
    else:
        say(msg.chat.id, "Top Expert Lessons", reply_markup=get_lessons_info(msg.chat.id))
    print(msg.chat.first_name, msg.chat.id, msg.text)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(msg):
    global add_lesson
    global add_lesson_name
    _id = msg.chat.id
    if _id in users:
        if msg.text.split()[0] in students:
            text = msg.text.split()[0]
        else:
            text = msg.text

        if text == "cash":
            say(_id, db.get_cash(), reply_markup=get_lessons_info(_id))
        elif text == "Расписание":
            say(_id, schedule, reply_markup=get_lessons_info(_id))
        elif text in students:
            if add_lesson:
                say(_id, "how much?", reply_markup=get_lessons_count_buttons())
                add_lesson_name = text
                add_lesson = False
            else:
                say(_id, db.get_full_list_lessons(text), reply_markup=get_lessons_info(_id))
        elif text in ['1', '2']:
            say(_id, "lesson added", reply_markup=get_lessons_info(_id))
            db.add_lesson(add_lesson_name, text)
        elif text == "Add custom":
            say(_id, "choose the student", reply_markup=get_add_lessons_board())
            add_lesson = True


        else:
            say(msg.chat.id, "Top Expert Lessons", reply_markup=get_lessons_info(_id))
            add_lesson = False

        print(msg.chat.first_name, msg.chat.id, text)

    else:
        non_user_answer(_id)
        new_user(_id, msg.chat.first_name)


if __name__ == "__main__":
    print("started")
    bot.polling(none_stop=True)
