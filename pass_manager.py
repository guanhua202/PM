import shelve
from random import randint
from random import shuffle
from time import sleep

def pass_manager_menu():
    print('\n       🔐 Простейший менеджер паролей\n')
    print('1. Список паролей')
    print('2. Сохранить новый пароль')
    print('3. Сгенерировать новый пароль')
    print('--------------------------------')
    print('0. Закрыть <Менеджер паролей>')
    print('--------------------------------')

def display_passwords():
    print('ID |     SITE      | PASSWORD')
    print('-----------------------------')

    if db['password_manager'] == []:
        print('Тут пусто.')
    else:
        for item in db['password_manager']:
            print(f"{str(item['id']).ljust(2)} | {item['site'].ljust(13)} | {item['password']}")

def password_generator(en_up, en_low, special_chars):

    password_options = {'pass_len' : 0, 'en_up' : False, 'en_low' : False, 'special_chars' : False}

    def pass_gen_menu(pass_len, en_up, en_low, special_chars):
        print('\n       🔑 Простейший генератор паролей\n')
        print('1. Длина пароля:', ('Нет', pass_len)[pass_len > 1])
        print('2. Большие буквы:', ('Выкл', 'Вкл')[en_up])
        print('3. Маленькие буквы:', ('Выкл', 'Вкл')[en_low])
        print('4. Спец.символы:', ('Выкл', 'Вкл')[special_chars])
        print('-----------------------')
        print('5. Начать генерацию')
        print('-----------------------')

    def password_generator(on_symbols, new_gen_pass):
        while len(new_gen_pass) != pass_len:
            shuffle(on_symbols)
            new_gen_pass += on_symbols[randint(0, len(on_symbols) - 1)]
        print('-' * (12 + len(new_gen_pass)))
        print(f"Ваш пароль: {new_gen_pass}")
        print('-' * (12 + len(new_gen_pass)))
        
        return new_gen_pass

    gen_pass = ""

    while gen_pass == "":

        # Запуск меню
        pass_gen_menu(password_options['pass_len'], password_options['en_up'], password_options['en_low'], password_options['special_chars'])

        # Выбор опции по нумерации
        options = int(input("Выберите опцию: "))

        if options == 1:
            pass_len = int(input("Введите длину пароля: "))
            password_options['pass_len'] = pass_len

        elif options == 2:
            if password_options['en_up']:
                password_options['en_up'] = False
            else:
                password_options['en_up'] = True

        elif options == 3:
            if password_options['en_low']:
                password_options['en_low'] = False
            else:
                password_options['en_low'] = True
                
        elif options == 4:
            if password_options['special_chars']:
                password_options['special_chars'] = False
            else:
                password_options['special_chars'] = True

        elif options == 5:
            if password_options['pass_len'] > 10:
                use_gen_list = []
                if password_options['en_up']:
                    use_gen_list += en_up
                if password_options['en_low']:
                    use_gen_list += en_low
                if password_options['special_chars']:
                    use_gen_list += special_chars
                if use_gen_list != []:
                    gen_pass = password_generator(use_gen_list, gen_pass)
                else:
                    print('--------------------------------')
                    print('Вы не выбрали ни одного символа.')
                    print('--------------------------------')
                    input("Нажмите Enter для продолжения...")		
                sleep(1)
                db['password_manager'].append({'id' : len(db['password_manager']) + 1, 'site' : input("Название сайта: ").lower(), 'password' : gen_pass})
                input("Нажмите Enter для продолжения...")
            else:
                print('---------------------------------------------')
                print("Длина пароля должна быть минимум 10 символов.")
                print('---------------------------------------------')
                input("Нажмите Enter для продолжения...")

# Запуск главной функции
pass_manager_menu()

db = shelve.open('db_pass_manager', writeback=True)

main_action = int(input("Выберите опцию меню: "))

while main_action != 0:
    
    if main_action == 1:
        print('\n| Пароли из Базы |')
        print('-----------------------------')
        display_passwords()
        print('-----------------------------')
        print('1. Выбрать ID Пароля для работы с ним')
        print('0. Вернуться в меню')

        select_option = int(input("Выберите опцию меню: "))

        if select_option == 1:
            # ID Модифицируемого пароля
            modify_pass_id = int(input("Введите ID Пароля: "))

            # Запускаем цикл поиска пароля по ID
            for item in db['password_manager']:
                # Нашли, а дальше обрабатываем и прерываем цикл
                if item['id'] == modify_pass_id:
                    print(f'Выбран:\n{item['id']} | {item['password']}')
                    print('-----------------------------')
                    # print('1. Зашифровать ()')
                    print('1. Сменить')
                    print('2. Удалить')

                    modify = int(input("Выберите опцию меню: "))
                    pass_id = item['id']

                    # if modify == 1:
                        # pass

                    if modify == 1:
                        item['password'] = input("Введите новый пароль: ")
                        print('Новый пароль записан в базу.')
                        break
                    elif modify == 2:
                        del db['password_manager'][pass_id - 1]
                        print('Пароль удалён из базы.')
                        break
        else:
            del main_action

    elif main_action == 2:
        db['password_manager'].append({'id' : len(db['password_manager']) + 1, 'site' : input("Введите ссылку на сайт: ").lower(), 'password' : input("Введите пароль для сохранения: ")})
        print('Пароль успешно сохранён. Для проверки нажмите <1>')

    elif main_action == 3:
        en_up = [
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                ]

        en_low = [
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                ]
    
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '/', '?']

        password_generator(en_up, en_low, special_chars)

    pass_manager_menu()
    main_action = int(input("Выберите опцию меню: "))