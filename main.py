import datetime
import random
import telebot
import time
import threading


FIRST_REM = '07:30'
SECOND_REM = '21:00'
TRY_QUANTITY = 3
TASK_FILE = 'tasks.txt'
ANSWERS_FILE = 'answers.txt'
puzzles = []
answers_list = []


bot = telebot.TeleBot('7215415683:AAFOaAfAPJ7iTRyMUkBOAXrWvUz7kHhC0I8')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, text='Привет! Меня зовут Ларс, я '
                               'буду отправлять тебе различные'
                               ' головоломки и загадки. Набери /puzzle')
    # Напоминатель
    reminder_thread = threading.Thread(target=send_reminders,
                                       args=(message.chat.id,))
    reminder_thread.daemon = True
    reminder_thread.start()


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, text=f'Этот бот предназначен для тренировки мозга,'
                               f'путем разгадывания математических '
                               f'головоломок. В настоящий момент Ларс знает'
                               f' {task_quantity} головоломок. Напоминания о '
                               f'необходимости размять мозги приходят '
                               f'пользователю в {FIRST_REM} и {SECOND_REM}. '
                               f'Всего дается {TRY_QUANTITY} попытки. Если '
                               f'головолмка не разгадана, то ее разгадка '
                               f'переносится на следущий раз. Для того чтобы '
                               f'испытать себя прямо сейчас наберите команду /puzzle')


def load_values_from_file(file_path):
    '''Загрузка информации из файлов'''
    values_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            values_list.append(line.strip())
    return values_list


@bot.message_handler(commands=['puzzle'])
def send_puzzle(message):
    index = random.randint(0, len(puzzles)-1)
    bot.send_message(message.chat.id, puzzles[index])
    bot.register_next_step_handler(message, check_answer, answers_list[index])



def check_answer(message, correct_answer):
    '''Проверка ответа - 1я попытка'''
    if message.text.lower() == correct_answer.lower():
        bot.send_message(message.chat.id, "Правильный ответ! Поздравляю!")
    else:
        bot.send_message(message.chat.id, "Неправильный ответ. Попробуйте еще раз.")
        bot.register_next_step_handler(message, check_answer_again, correct_answer)


def check_answer_again(message, correct_answer):
    '''Проверка ответа 2-я попытка'''
    if message.text.lower() == correct_answer.lower():
        bot.send_message(message.chat.id, "Правильный ответ! Поздравляю!")
    else:
        bot.send_message(message.chat.id, "Неправильный ответ. Попробуйте еще раз.")
        bot.register_next_step_handler(message, check_answer_last, correct_answer)


def check_answer_last(message, correct_answer):
    '''Проверка ответа последняя попытка'''
    if message.text.lower() == correct_answer.lower():
        bot.send_message(message.chat.id, "Правильный ответ! Поздравляю!")
    else:
        bot.send_message(message.chat.id, "Неправильный ответ. Попытки закончились. В следующий раз старайтесь лучше")


def send_reminders(chat_id):
   '''Напоминатель'''
   while True:
       now = datetime.datetime.now().strftime('%H:%M')
       if now == FIRST_REM or now == SECOND_REM:
           bot.send_message(chat_id, text='Пора размять мозги! Введите комманду /puzzle')
           time.sleep(61)


# Загружаем вопросы и ответы
puzzles = load_values_from_file(TASK_FILE)
answers_list = load_values_from_file(ANSWERS_FILE)
task_quantity = len(puzzles)

bot.polling(none_stop=True)