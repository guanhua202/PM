# Импортируем модуль shelve для простого хранения данных в файле (как словарь)
import shelve
# Импортируем функцию randint для генерации случайных чисел
from random import randint
# Импортируем shuffle для перемешивания списка
from random import shuffle
# Импортируем sleep для создания пауз в выполнении программы
from time import sleep

# Функция отрисовки главного меню
def pass_manager_menu():
    print('\n       🔐 Простейший менеджер паролей\n')
    print('1. Список паролей')
    print('2. Сохранить новый пароль')
    print('3. Сгенерировать новый пароль')
    print('--------------------------------')
    print('0. Закрыть <Менеджер паролей>')
    print('--------------------------------')

# Функция вывода всех сохранённых паролей из базы данных
def display_passwords():
    # Заголовок таблицы
    print('ID |     SITE      | PASSWORD')
    print('-----------------------------')

    # Если список паролей пуст, выводим сообщение
    if db['password_manager'] == []:
        print('Тут пусто.')
    else:
        # Проходим по каждому элементу и красиво выводим его поля
        for item in db['password_manager']:
            print(f"{str(item['id']).ljust(2)} | {item['site'].ljust(13)} | {item['password']}")

# Генератор паролей с настройками
def password_generator(en_up, en_low, special_chars):
    # Словарь с текущими настройками генерации: длина и флаги групп символов
    password_options = {'pass_len' : 0, 'en_up' : False, 'en_low' : False, 'special_chars' : False}

    # Внутренняя функция для отрисовки меню настроек генератора
    def pass_gen_menu(pass_len, en_up, en_low, special_chars):
        print('\n       🔑 Простейший генератор паролей\n')
        # Если длина больше 1, показываем число, иначе слово "Нет"
        print('1. Длина пароля:', ('Нет', pass_len)[pass_len > 1])
        # Показываем Вкл/Выкл для каждой группы символов
        print('2. Большие буквы:', ('Выкл', 'Вкл')[en_up])
        print('3. Маленькие буквы:', ('Выкл', 'Вкл')[en_low])
        print('4. Спец.символы:', ('Выкл', 'Вкл')[special_chars])
        print('-----------------------')
        print('5. Начать генерацию')
        print('-----------------------')

    # Функция, которая непосредственно генерирует пароль из доступных символов
    def password_generator(on_symbols, new_gen_pass):
        # Пока длина пароля не достигнет нужной, случайно выбираем символы
        while len(new_gen_pass) != pass_len:
            # Перемешиваем список символов для большей случайности
            shuffle(on_symbols)
            # Добавляем случайный символ из списка
            new_gen_pass += on_symbols[randint(0, len(on_symbols) - 1)]
        print('-' * (12 + len(new_gen_pass)))
        print(f"Ваш пароль: {new_gen_pass}")
        print('-' * (12 + len(new_gen_pass)))
        return new_gen_pass

    # Переменная для хранения сгенерированного пароля (пустая строка — значит ещё не создан)
    gen_pass = ""

    # Цикл генерации: повторяется, пока пароль не будет создан
    while gen_pass == "":
        # Показываем меню с текущими настройками
        pass_gen_menu(password_options['pass_len'], password_options['en_up'], password_options['en_low'], password_options['special_chars'])

        # Запрашиваем выбор пользователя
        options = int(input("Выберите опцию: "))

        # Установка длины пароля
        if options == 1:
            pass_len = int(input("Введите длину пароля: "))
            password_options['pass_len'] = pass_len

        # Включение/выключение больших букв
        elif options == 2:
            if password_options['en_up']:
                password_options['en_up'] = False
            else:
                password_options['en_up'] = True

        # Включение/выключение маленьких букв
        elif options == 3:
            if password_options['en_low']:
                password_options['en_low'] = False
            else:
                password_options['en_low'] = True

        # Включение/выключение спецсимволов
        elif options == 4:
            if password_options['special_chars']:
                password_options['special_chars'] = False
            else:
                password_options['special_chars'] = True

        # Запуск генерации
        elif options == 5:
            # Минимальная длина пароля — 10 символов
            if password_options['pass_len'] > 10:
                use_gen_list = []  # Список допустимых символов
                # Добавляем выбранные группы символов
                if password_options['en_up']:
                    use_gen_list += en_up
                if password_options['en_low']:
                    use_gen_list += en_low
                if password_options['special_chars']:
                    use_gen_list += special_chars
                # Если хоть одна группа выбрана, запускаем генерацию
                if use_gen_list != []:
                    gen_pass = password_generator(use_gen_list, gen_pass)
                else:
                    # Предупреждение, что не выбрано ни одной группы
                    print('--------------------------------')
                    print('Вы не выбрали ни одного символа.')
                    print('--------------------------------')
                    input("Нажмите Enter для продолжения...")		
                sleep(1)
                # Сохраняем сгенерированный пароль в базу, запрашиваем название сайта
                db['password_manager'].append({'id' : len(db['password_manager']) + 1, 'site' : input("Название сайта: ").lower(), 'password' : gen_pass})
                input("Нажмите Enter для продолжения...")
            else:
                # Если длина меньше 10, выводим сообщение и возвращаемся в меню настроек
                print('---------------------------------------------')
                print("Длина пароля должна быть минимум 10 символов.")
                print('---------------------------------------------')
                input("Нажмите Enter для продолжения...")

# ---------- Точка входа в программу ----------
# Выводим главное меню
pass_manager_menu()

# Открываем (или создаём) файл базы данных с автоматической записью изменений
db = shelve.open('db_pass_manager', writeback=True)

# Если ключ 'password_manager' ещё не существует, создаём пустой список
if 'password_manager' not in db:
    db['password_manager'] = []

# Запрашиваем первое действие у пользователя
main_action = int(input("Выберите опцию меню: "))

# Основной цикл программы: работает, пока не выбрана опция 0 (выход)
while main_action != 0:
    
    # Опция 1: просмотр списка паролей и действия над ними
    if main_action == 1:
        print('\n| Пароли из Базы |')
        print('-----------------------------')
        display_passwords()
        print('-----------------------------')
        print('1. Выбрать ID Пароля для работы с ним')
        print('0. Вернуться в меню')

        select_option = int(input("Выберите опцию меню: "))

        # Если выбрали работу с конкретным паролем
        if select_option == 1:
            # Запрашиваем ID пароля, который будем менять/удалять
            modify_pass_id = int(input("Введите ID Пароля: "))

            # Ищем пароль по ID в базе
            for item in db['password_manager']:
                if item['id'] == modify_pass_id:
                    # Выводим информацию о найденном пароле
                    print(f'Выбран:\n{item["id"]} | {item["password"]}')
                    print('-----------------------------')
                    print('1. Сменить')
                    print('2. Удалить')

                    modify = int(input("Выберите опцию меню: "))
                    pass_id = item['id']
                    
                    # Меняем пароль на новый
                    if modify == 1:
                        item['password'] = input("Введите новый пароль: ")
                        print('Новый пароль записан в базу.')
                        break
                    # Удаляем запись по индексу (ID - 1)
                    elif modify == 2:
                        del db['password_manager'][pass_id - 1]
                        print('Пароль удалён из базы.')
                        break
        # Если выбрали 0, просто возвращаемся в главное меню (удаляем текущее действие)
        else:
            del main_action

    # Опция 2: сохранить новый пароль вручную
    elif main_action == 2:
        db['password_manager'].append({'id' : len(db['password_manager']) + 1, 'site' : input("Введите ссылку на сайт: ").lower(), 'password' : input("Введите пароль для сохранения: ")})
        print('Пароль успешно сохранён. Для проверки нажмите <1>')

    # Опция 3: генерация нового пароля
    elif main_action == 3:
        # Списки доступных символов
        en_up = [
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                ]

        en_low = [
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                ]
    
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '/', '?']

        # Запускаем генератор с этими наборами символов
        password_generator(en_up, en_low, special_chars)

    # После выполнения действия снова показываем меню и ждём выбора
    pass_manager_menu()
    main_action = int(input("Выберите опцию меню: "))

# Закрываем базу данных при выходе из программы
db.close()
