from config import *
from interface import *
from database import SQLighter
import telebot

bot = telebot.TeleBot(TOKEN)
db = SQLighter("base.db")
say = bot.send_message
state = States()

record = []
payment_record = []


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


@bot.message_handler(func=lambda x: state.state == "add_lessons")
def bot_add_lesson(msg):
    _id = msg.chat.id
    if msg.text == "return":
        state.set_state("listening")
        return
    record.append(msg.text)  # name
    say(_id, "How much?", reply_markup=get_lessons_count_buttons())
    state.set_state("add_lessons_count")


@bot.message_handler(func=lambda x: state.state == "add_lessons_count")
def bot_add_lesson(msg):
    _id = msg.chat.id
    if msg.text == "return":
        state.set_state("listening")
        return
    record.append(int(msg.text))  # lessons_count
    say(_id, "Enter typing speed")
    state.set_state("add_typing_speed")


@bot.message_handler(func=lambda x: state.state == "add_typing_speed")
def bot_add_lesson(msg):
    _id = msg.chat.id
    if msg.text == "return":
        state.set_state("listening")
        return
    record.append(int(msg.text))  # typing_speed
    say(_id, "done", reply_markup=get_lessons_info(_id))
    db.add_row_in_archive(*record)
    record.clear()
    rander_plots()
    state.set_state("listening")


@bot.message_handler(func=lambda x: state.state == "new_payment")
def add_new_payment(msg):
    _id = msg.chat.id
    if msg.text == "return":
        state.set_state("listening")
        return
    payment_record.append(int(msg.text))
    say(_id, "comment?", reply_markup=return_button())
    state.state = "payment_comment"


@bot.message_handler(func=lambda x: state.state == "payment_comment")
def add_new_payment(msg):
    _id = msg.chat.id
    text = msg.text
    if not text == "return":
        payment_record.append(text)
    db.add_new_payment(*payment_record)
    payment_record.clear()
    state.set_state("listening")
    say(_id, "done", reply_markup=get_lessons_info(_id))


@bot.message_handler(content_types=["text"], func=lambda x: state.state == "listening")
def repeat_all_messages(msg):
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
            say(_id, db.get_full_list_lessons(text), reply_markup=get_lessons_info(_id))
            with open(f"imgs/{text}_plot.png", "rb") as img:
                bot.send_photo(_id, img)

        elif text == "Add lessons":
            say(_id, "choose the student", reply_markup=get_add_lessons_board())
            state.set_state("add_lessons")

        elif text == "new payment":
            say(_id, "how much?")
            state.set_state("new_payment")

        elif text == "return":
            say(msg.chat.id, "Top Expert Lessons", reply_markup=get_lessons_info(_id))
            state.set_state("listening")

    else:
        non_user_answer(_id)
        new_user(_id, msg.chat.first_name)


if __name__ == "__main__":
    rander_plots()
    print("started")
    bot.polling(none_stop=True)
#