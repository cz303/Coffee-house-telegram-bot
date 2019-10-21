import telebot
from telebot import types
from gh_menu import gh_menu
import db_users
from config import create_menu, Goods
import config
from datetime import datetime
from random import randint

bot = telebot.TeleBot(config.TOKEN)

print(bot.get_me())

text_messages = {
    'start':
        u'Приветствую тебя, {name}!\n'
        u'Я помогу тебе сделать онлайн заказ (это быстро и без очереди).\n\n'
        u'1. Выбери интересующий напиток/сэндвич/десерт (Ты можешь выбрать несколько)\n'
        u'2. Выбери время, когда захочешь забрать заказ\n'
        u'3. Оплати заказ (это безопасно)\n'
        u'4. Обязательно забери заказ вовремя',
    
    'help':
        u'Пока что я не знаю, чем тебе помочь, поэтому просто выпей кофе!'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    db_users.check_and_add_user(message)
    bot.send_message(message.from_user.id, text_messages['start'].format(name=message.from_user.first_name))

#@bot.message_handler(commands=['start'])
#def make_order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Сделать заказ')
    bot.send_message(message.from_user.id, 'Начните взаимодействие путем нажатия кнопки', reply_markup=markup)
    db_users.set_state(message.from_user.id, config.S_MAKE_ORDER)
    new_order(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Назад')
    msg = bot.send_message(message.from_user.id, text_messages['help'], reply_markup=markup)
    bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_MAKE_ORDER)
def new_order(message):
    if message.text == 'Сделать заказ':
        global dt
        dt = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        db_users.new_list(message, dt)
        db_users.set_state(message.from_user.id, config.S_GET_CAT)
        get_categories(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_CAT)
def get_categories(message):
    user_id = message.from_user.id
    mass = list(gh_menu.keys())
    markup = create_menu(mass, back=False)
    bot.send_message(user_id, 'Что вас интересует?', reply_markup=markup)
    db_users.set_state(user_id, config.S_CHOOSE_CAT)
    choose_categories(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_CHOOSE_CAT)
def choose_categories(message):
    
    user_id = message.from_user.id
    
    if message.text == 'Особые напитки':
        db_users.set_state(user_id, config.S_SPECIAL_DRINKS)
        get_special_drinks(message)
        db_users.set_category(dt, user_id, message)
    elif message.text == 'Кофе':
        db_users.set_state(user_id, config.S_COFFEE)
        get_coffee(message)
        db_users.set_category(dt, user_id, message)
    elif message.text == 'Горячие напитки':
        db_users.set_state(user_id, config.S_HOT_DRINKS)
        get_hot_drinks(message)
        db_users.set_category(dt, user_id, message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_SPECIAL_DRINKS)
def get_special_drinks(message):
    special_drinks = Goods(bot, message, config.S_ITEM_SELECTION)
    special_drinks.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_COFFEE)
def get_coffee(message):
    coffee = Goods(bot, message, config.S_ITEM_SELECTION)
    coffee.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_HOT_DRINKS)
def get_hot_drinks(message):
    hot_drinks = Goods(bot, message, config.S_ITEM_SELECTION)
    hot_drinks.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_ITEM_SELECTION)
def item_selection(message):

    user_id = message.from_user.id

    if message.text == "Назад":
        db_users.set_state(user_id, config.S_GET_CAT)
        get_categories(message)
        db_users.delete_category(dt, user_id)
    if message.text == 'Латте Лаванда Шалфей':
        db_users.set_state(user_id, config.S_LATTE_LAVANDA_SHALFEI)
        get_latte_lavanda_shalfei(message)
        db_users.set_item(dt, user_id, message)     
    elif message.text == 'Раф Лимонный Пай':
        db_users.set_state(user_id, config.S_RAF_LEMON_PIE)
        get_raf_lemon_pie(message)
        db_users.set_item(dt, user_id, message)
    elif message.text == 'Капучино':
        db_users.set_state(user_id, config.S_KAPUCHINO)
        get_kapuchino(message)
        db_users.set_item(dt, user_id, message)
    elif message.text == 'Латте Макиато':
        db_users.set_state(user_id, config.S_LATTE_MAKIATO)
        get_latte_makiato(message)
        db_users.set_item(dt, user_id, message)
    elif message.text == 'Какао':
        db_users.set_state(user_id, config.S_KAKAO)
        get_kakao(message)
        db_users.set_item(dt, user_id, message)
    elif message.text == 'Чай':
        db_users.set_state(user_id, config.S_TEA) #S_HOT_DRINKS_TEA_TYPE
        get_tea(message)
        db_users.set_item(dt, user_id, message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_LATTE_LAVANDA_SHALFEI)
def get_latte_lavanda_shalfei(message):
    latte_lavanda_shalfei = Goods(bot, message, config.S_SPECIAL_DRINKS_SELECTION)
    latte_lavanda_shalfei.get_current_good(config.S_SPECIAL_DRINKS)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_RAF_LEMON_PIE)
def get_raf_lemon_pie(message):
    raf_lemon_pie = Goods(bot, message, config.S_SPECIAL_DRINKS_SELECTION)
    raf_lemon_pie.get_current_good(config.S_SPECIAL_DRINKS)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_KAPUCHINO)
def get_kapuchino(message):
    kapuchino = Goods(bot, message, config.S_COFFEE_SELECTION)
    kapuchino.get_current_good(config.S_COFFEE)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_LATTE_MAKIATO)
def get_latte_makiato(message):
    latte_makiato = Goods(bot, message, config.S_COFFEE_SELECTION)
    latte_makiato.get_current_good(config.S_COFFEE)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_KAKAO)
def get_kakao(message):
    kakao = Goods(bot, message, config.S_HOT_DRINKS_SELECTION)
    kakao.get_current_good(config.S_HOT_DRINKS)


'''@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_HOT_DRINKS_TEA_TYPE)
def get_tea_type(message):
    tea = Goods(bot, message, config.S_TEA)
    tea.get_current_good(config.S_HOT_DRINKS)'''


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_TEA)
def get_tea(message):
    tea = Goods(bot, message, config.S_HOT_DRINKS_TEA_TYPE)
    tea.get_tea_type(config.S_HOT_DRINKS, config.S_TEA) #config.S_TEA_ENGLISH or config.S_TEA_ERL


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_SPECIAL_DRINKS_SELECTION)
def get_special_drinks_selection(message):

    user_id = message.from_user.id

    if message.text == 'Назад':
        db_users.delete_item(dt, user_id)
        mass = list(gh_menu[config.S_SPECIAL_DRINKS])
        markup = create_menu(mass)
        bot.send_message(user_id, 'Вы вернулись в меню выбора особых напитков', reply_markup=markup)
        db_users.set_state(user_id, config.S_ITEM_SELECTION)
    else:
        db_users.set_state(user_id, config.S_ADD_ITEM)
        db_users.set_item_size(dt, user_id, message)
        add_item(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_COFFEE_SELECTION)
def get_coffee_selection(message):

    user_id = message.from_user.id

    if message.text == 'Назад':
        db_users.delete_item(dt, user_id)
        mass = list(gh_menu[config.S_COFFEE])
        markup = create_menu(mass)
        bot.send_message(user_id, 'Вы вернулись в меню выбора кофе', reply_markup=markup)
        db_users.set_state(user_id, config.S_ITEM_SELECTION)
    else:
        db_users.set_state(user_id, config.S_ADD_ITEM)
        db_users.set_item_size(dt, user_id, message)
        add_item(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_HOT_DRINKS_TEA_TYPE)
def get_hot_drinks_selection(message):

    user_id = message.from_user.id

    if message.text == 'Назад':
        db_users.delete_item(dt, user_id)
        mass = list(gh_menu[config.S_HOT_DRINKS])
        markup = create_menu(mass)
        bot.send_message(user_id, 'Вы вернулись в меню выбора горячих напитков', reply_markup=markup)
        db_users.set_state(user_id, config.S_ITEM_SELECTION)
    else:
        db_users.set_state(user_id, config.S_HOT_DRINKS_SELECTION)
        db_users.set_tea_type(dt, user_id, message)
        add_item(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_HOT_DRINKS_SELECTION)
def get_hot_drinks_selection(message):

    user_id = message.from_user.id

    if message.text == 'Назад':
        db_users.delete_item(dt, user_id)
        mass = list(gh_menu[config.S_TEA])
        markup = create_menu(mass)
        bot.send_message(user_id, 'Вы вернулись в меню выбора чая', reply_markup=markup)
        db_users.set_state(user_id, config.S_HOT_DRINKS_TEA_TYPE)
    else:
        db_users.set_state(user_id, config.S_ADD_ITEM)
        db_users.set_item_size(dt, user_id, message)
        add_item(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_ADD_ITEM)
def add_item(message):   

    user_id = message.from_user.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Да, в главное меню', 'Нет, оплатить')
    bot.send_message(user_id, 'Товар добавлен в корзину. Хотите что-нибудь еще?', reply_markup=markup)
    db_users.set_state(user_id, config.S_PAYMENT)
    get_payment(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_PAYMENT)
def get_payment(message):

    user_id = message.from_user.id

    if message.text == 'Да, в главное меню':
        db_users.set_state(user_id, config.S_GET_CAT)
        get_categories(message)
    if message.text == 'Нет, оплатить':     
        markup = types.InlineKeyboardMarkup()
        btn_pay = types.InlineKeyboardButton(text='Оплатить', url='www.habr.com') #Спасибо за использование бота. Это тестовая версия, оплата будет добавлена позже
        markup.add(btn_pay)
        bot.send_message(user_id, db_users.get_item(dt, user_id), reply_markup = markup)
        make_order(message)
        db_users.set_state(user_id, config.S_MAKE_ORDER)

bot.polling(none_stop = True)