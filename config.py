from telebot import types

import db_users
from gh_menu import gh_menu

TOKEN = '938186499:AAGIUmfg_ep52x5a9oT0UCxzImdmVptLDMg'

# КОНСТАНТЫ СОСТОЯНИЙ
S_GET_CAT = 'Список категорий'
S_CHOOSE_CAT = 'Выбор категории'

# КОНСТАНТЫ КАТЕГОРИЙ
S_SPECIAL_DRINKS = 'Особые напитки'
S_COFFEE = 'Кофе'
S_HOT_DRINKS = 'Горячие напитки'

# КОНСТАНТЫ ТОВАРОВ
S_ITEM_SELECTION = 'Выбор товара'


S_SPECIAL_DRINKS_SELECTION = 'Выбор размера особых напитков'
S_COFFEE_SELECTION = 'Выбор размера кофе'
S_HOT_DRINKS_SELECTION = 'Выбор размера горячих напитков'
S_HOT_DRINKS_TEA_TYPE = 'Выбор типа чая горячих напитков'

S_TEA_ENGLISH = 'Английский завтрак'
S_TEA_ERL = 'Эрл грей'

S_ADD_ITEM = 'Товар добавлен в корзину'
S_PAYMENT = 'Меню оплаты'

S_MAKE_ORDER = 'Сделать заказ'


S_SPECIAL_DRINKS_CHOICE = 'Выбор особых напитков'



S_LATTE_LAVANDA_SHALFEI = 'Латте Лаванда Шалфей'
S_LATTE_LAVANDA_SHALFEI_CHOICE = 'Латте Лаванда Шалфей Выбор'

S_RAF_LEMON_PIE = 'Раф Лимонный Пай'
S_RAF_LEMON_PIE_CHOICE = 'Раф Лимонный Пай Выбор'

S_KAPUCHINO = 'Капучино'
S_KAPUCHINO_CHOICE = 'Капучино Выбор'

S_LATTE_MAKIATO = 'Латте Макиато'
S_LATTE_MAKIATO_CHOICE = 'Латте Макиато Выбор'

S_KAKAO = 'Какао'
S_KAKAO_CHOICE = 'Какао Выбор'

S_TEA = 'Чай'
S_TEA_CHOICE = 'Чай Выбор'



S_LATTE_LAVANDA_SHALFEI_300 = '300 мл - 139 руб'
S_LATTE_LAVANDA_SHALFEI_400 = '400 мл - 169 руб'

S_RAF_LEMON_PIE_300 = 'Раф Лимонный Пай 300 мл - 159 руб'
S_RAF_LEMON_PIE_400 = 'Раф Лимонный Пай 400 мл - 179 руб'

S_KAPUCHINO_300 = 'Капучино 300 мл - 119 руб'
S_KAPUCHINO_400 = 'Капучино 400 мл - 149 руб'

S_LATTE_MAKIATO_300 = 'Латте Макиато 300 мл - 119 руб'
S_LATTE_MAKIATO_400 = 'Латте Макиато 400 мл - 139 руб'

S_KAKAO_300 = 'Какао 300 мл - 119 руб'
S_KAKAO_400 = 'Какао 400 мл - 149 руб'

S_TEA_ENGLISH_300 = 'Чай 300 мл - 99 руб'
S_TEA_ENGLISH_400 = 'Чай 400 мл - 109 руб'

S_TEA_ERL_300 = 'Чай Эрл Грей 300 мл - 99 руб'
S_TEA_ERL_400 = 'Чай Эрл Грей 400 мл - 109 руб'

#print(list(gh_menu[S_HOT_DRINKS][S_TEA][S_ENGLISH_BREAKFAST]))
#print(gh_menu[S_HOT_DRINKS][S_TEA].get(99))


#ОСОБЫЕ НАПИТКИ
list_of_latte = ['Латте Лаванда Шалфей']

'''print(gh_menu[S_SPECIAL_DRINKS][S_LATTE_LAVANDA_SHALFEI]['300 мл - 139 руб'])
for k,v in gh_menu.items(): 
    print(list(v.keys()))'''

def create_menu(mass, back = True):
    """
    This function allows to creat menu of buttons.
    mass - the list of string (buttons)
    back - back button, if true, add a button back. Default back=True
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(mass) == 1:
        markup.row(mass[0]) #Если массив содержит только 1 элемент, то просто добавить его
    else:
        while len(mass) > 0:  
            try:
                cut = mass[:2] #Берем только первые два элемента массива и добавляем их в клавиатуру
                markup.row(cut[0], cut[1])
                del mass[:2] #Удаляем эти элементы, так как их уже добавили
                
                if len(mass) == 1:
                    markup.row(mass[0])
                    break #Если массив содержит 1 элемент, то добавить его и выйти из цикла
            except:
                print('WTF')
    

    if back == True: 
        markup.row('Назад')
    
    return markup


class Goods:
    def __init__(self, bot, message, state):
        self.bot = bot
        self.message = message 
        self.state = state

        #self - ссылка на экземпляр этого класса 
        #bot - это объект нашего бота, который мы создаем в самом начале файла bot.py (bot = telebot.TeleBot(config.TOKEN) )
        #message - это объект библиотеки pyTelegramBotAPI, он нужен для получения данных о пользователе, отправленным им текстом и еще много всего.
        #state - состояние пользователя, которое мы хотим ему присвоить

    def get_goods_list(self):
        user_id = self.message.from_user.id
        mass = list(gh_menu[self.message.text])
        markup = create_menu(mass)
        self.bot.send_message(user_id, 'Выберите напиток', reply_markup=markup)
        db_users.set_state(user_id, self.state)

    def get_current_good(self, cat):
        user_id = self.message.from_user.id
        mass = list(gh_menu[cat][self.message.text])
        markup = create_menu(mass) #back = False
        if self.message.text == 'Чай':
            self.bot.send_message(user_id, 'Выберите вид чая', reply_markup=markup)
        else:
            self.bot.send_message(user_id, 'Выберите размер', reply_markup=markup)
        db_users.set_state(user_id, self.state)

    def get_tea_type(self, cat, type):
        user_id = self.message.from_user.id
        mass = list(gh_menu[cat][type][self.message.text])
        markup = create_menu(mass) #back = False
        self.bot.send_message(user_id, 'Выберите размер чая', reply_markup=markup)
        db_users.set_state(user_id, self.state)