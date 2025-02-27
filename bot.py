import telebot # библиотека telebot
from config import token # импорт токена
import random

anecdotes = [ 
    'Мужик сидит на крыше дома, а под ним половина города затоплена. Проходит лодка, мужик кричит: — Эй, вы там, когда отплывать будете?',
    '— Доктор, у меня проблемы с памятью! — Какие именно? — Какие именно чего?',
    '— Доктор, у меня голова болит, когда я на ногах стою. — Ну, не стойте на ногах.',
    '– Сынок, не сиди за компьютером целый день! – Ладно, пап, буду сидеть за два.',
    'Женщина пришла в аптеку и спросила: "У вас есть что-нибудь от усталости мужа от моей усталости?"',
    'Встречаются два программиста. Один другому говорит: — Почему ты такой бледный? — Да вчера вечером цикл не закончил.',
    'Мужик купил говорящего попугая. Через неделю попугай сдох. Видимо, наговорился...'
]

    
bot = telebot.TeleBot(token) 
facts = [
    'Кошки могут прыгнуть в 7 раз выше своего роста',
    'Все панды в мире связаны между собой',
    'Во время второй мировой войны первая бомба, сброшенная на Берлин, убила единственного слона в Берлинском зоопарке.',
    'Ежедневная двадцатиминутная прогулка сжигает около трех килограмм жира в год.',
    'Игрушка йо-йо появилась в шеснадцатом веке на Филиппинах в качестве оружия.',
    'Человеческий волос толще мыльной пленки примерно в пять тысяч раз.',
    'Во время сна мозг работает быстрее, чем во время бодрствования.',
    'Все дети до трех лет могут быть признаны гениальными, так как их мозги развиваются быстрее, чем у взрослых.',
    ]
@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, f'''Приветсвую, {message.from_user.first_name}!👋
Добро пожаловать в чат!🙌 (/help для команд)''')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '''Привет!👋 Я бот для управления чатом.
Для списка команд пропишите - /help 📃''')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, '''Вот доступный список команд бота :
- /start - Начало работы с ботом
- /help - Выводит список команд
- /info - Информация об авторе бота
- /fact - Случайный факт
- /anecdote - Рандомный анекдот
**--------АДМИН КОМАНДЫ--------**
- /kick - Кикнуть пользователя
- /ban - Забанить пользователя
Пока что все...🤷‍♂️
''')
    
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        sender_id = message.from_user.id
        sender_status = bot.get_chat_member(chat_id, sender_id).status
        if sender_status == 'administrator' or sender_status == 'creator':
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно кикнуть администратора.")

            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был кикнут.")
        else:
            bot.reply_to(message, f'{message.from_user.first_name}, вы не являетесь администратором чата!')
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.") # НЕ ЗАБУДЬТЕ ДАТЬ ПРАВА АДМИНА БОТУ

@bot.message_handler(commands=['ban'])

def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.") # НЕ ЗАБУДЬТЕ ДАТЬ ПРАВА АДМИНА БОТУ

@bot.message_handler(commands=['info'])
def author_command(message):
    bot.send_message(message.chat.id, '''Данный бот был создан учеником Kodland Алиханом.
    author: @sirdezzan
    bot ver: 1.3''')

@bot.message_handler(commands=['anecdote'])
def text_message(message):
    anecdote=random.choice(anecdotes)
    bot.send_message(message.chat.id, f'Анекдот: {anecdote}')

    
@bot.message_handler(commands=['fact'])
def text_message(message):
    fact=random.choice(facts)
    bot.send_message(message.chat.id, f'Факт: {fact}')
@bot.message_handler(func=lambda message: True)
def linkban(message):
    if 'https://' in message.text:
        chat_id = message.chat.id
        user_id = message.from_user.id
        bot.ban_chat_member(chat_id, user_id)
    bot.reply_to(message, f'Пользователь @{message.from_user.username} был забанен за отправку ссылок.') 
    bot.delete_message(chat_id, message.message_id)
bot.infinity_polling(none_stop=True)
