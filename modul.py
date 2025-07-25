import os, datetime, pickle, glob, locale, ui, validate, csv
locale.setlocale(locale.LC_TIME, 'ru')


# Вывод заметок на экран
def table_note(collection: list) -> None:
    """
    :param collection: list список заметок
    :return: None
    """

    for i in range(len(collection)):

        for j in range(6):

            if i == 0:
                print(f'\033[33m{collection[i][j]: ^20}\033[0m', end='')

            elif j == 2 and i != 0:

                if collection[i][j] == 'срочная':
                    print(f'\033[31m{collection[i][j]: ^20}\033[0m', end='')

                elif collection[i][j] == 'важная':
                    print(f'\033[35m{collection[i][j]: ^20}\033[0m', end='')

                else:
                    print(f'{collection[i][j]: ^20}', end='')

            else:
                print(f'{collection[i][j]: ^20}', end='')

        print()

# Сортировка заметок
def sorting() -> None:

    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    name_files = requesting_file_name_from_directory(ui.dict_input_user['Сортировать'], ui.dict_input_error['нет файла'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)

    except:
        ui.information_for_user(ui.dict_output_user['пустой'])
        return

    if not isinstance(collection, list):
        ui.information_for_user(ui.dict_output_user['не таблица'])

    if collection[0][6] != '':

        password = input(ui.dict_input_user['пароль'])

        while password != collection[0][6]:

            ui.input_error(ui.dict_input_error['не верно пароль'])
            password = input(ui.dict_input_user['пароль'])

            if password == collection[0][6]:
                break

            elif password == 'exit':
                return

    print(f'\nВаши заметки - {collection[0][7]}шт')
    print('-' * 120)
    sort_collection = []
    table_note(collection)
    print()

    for key in ui.dict_menu_sort_note.keys():
        print(f'\033[36m{key}\033[0m - {ui.dict_menu_sort_note[key]}')

    print()
    sort_menu = ui.input_user(ui.dict_input_user['сортировка меню'])
    while sort_menu not in ['1', '2', '3']:
        ui.input_error(ui.dict_input_error['Ошибка ввода'])
        sort_menu = ui.input_user(ui.dict_input_user['сортировка меню'])

    match sort_menu:
        case '1':

            def key_data(i):
                data = datetime.datetime.strptime(i[0],"%d.%B.%Y")
                return data

            sort_collection = sorted(collection[1:], key = key_data)

        case '2':

            def key_word(i):
                if i[2] == 'срочная':
                    return '1'
                elif i[2] == 'важная':
                    return '2'
                else:
                    return '3'

            sort_collection = sorted(collection[1:], key = key_word)

        case '3':
            sort_collection = sorted(collection[1:], key = lambda i: i[3])

    sort_collection.insert(0, collection[0])
    table_note(sort_collection)

# Добавление заметок в сборник
def add_notes_collection() -> None:
    """

    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    name_files = requesting_file_name_from_directory(ui.dict_input_user['Добавить заметки'], ui.dict_input_error['нет файла'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)

    except:

        ui.information_for_user(ui.dict_output_user['пустой'])
        collection = create_new_note()
        try:
            with open(path_and_base_name, "wb") as file:
                pickle.dump(collection, file)

            ui.information_for_user(ui.dict_output_user['успешно заметка'])
            return

        except:
            ui.information_for_user(ui.dict_output_user['не создан'])
            return


    if not isinstance(collection, list):

        collection = create_new_note()

    else:

        if collection[0][6] != '':

            password = input(ui.dict_input_user['пароль'])

            while password != collection[0][6]:

                ui.input_error(ui.dict_input_error['не верно пароль'])
                password = input(ui.dict_input_user['пароль'])

                if password == collection[0][6]:
                    break

                elif password == 'exit':
                    return

        name_note_in_list = ['']

        for i in range (1, len(collection)):

            name_note_in_list.append(collection[i][3])

        collection = note(name_note_in_list, collection)

        if collection[0][6] == '':

            password_yes_no = input(ui.dict_input_user['пароль_y_n'])

            if validate.choice_yes_no(password_yes_no, ui.dict_input_user['пароль_y_n'], ui.dict_input_error['y/n']):
                password = input(ui.dict_input_user['пароль'])
                collection[0][6] = password

        else:
            password_yes_no = input(ui.dict_input_user['пароль нет'])
            if validate.choice_yes_no(password_yes_no, ui.dict_input_user['пароль нет'], ui.dict_input_error['y/n']):
                collection[0][6] = ''


        collection[0][7] = str(len(collection) - 1)

    try:
        with open(path_and_base_name, "wb") as file:
            pickle.dump(collection, file)

        ui.information_for_user(ui.dict_output_user['успешно заметка'])

    except:
        ui.information_for_user(ui.dict_output_user['не создан'])

# Запрос имени файла из списка в директории
def requesting_file_name_from_directory(requesting: str, error: str) -> str:

    """
    :param requesting: str сообщение из словаря, что требуется
    :param error: str сообщение из словаря, в случае ошибки
    :return:
    """
    list_name_files = list_name_file()
    name_files = ui.input_user(requesting)

    while not name_files in list_name_files:
        ui.input_error(error)
        name_files = ui.input_user(requesting)

    return name_files

# Экспорт сборника заметок в CSV файл
def exporting_collection_in_CSV_file() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()

    name_files = requesting_file_name_from_directory(ui.dict_input_user['Файл CSV'], ui.dict_input_error['нет файла'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)

    except:

        ui.information_for_user(ui.dict_output_user['не таблица'])
        return

    base_name = name_files + '.csv'
    path = ui.input_user(ui.dict_input_user['Путь CSV'])

    while not validate.directory_exists_yes_no(path):

        ui.input_error(ui.dict_input_error['Нет пути'])
        path = ui.input_user(ui.dict_input_user['Путь CSV'])

    path_and_base_name = os.path.join(path, base_name)
    separator = ui.input_user(ui.dict_input_user[',/;'])

    while separator not in [',', ';']:
        ui.input_error(ui.dict_input_error['Не символ ,/;'])
        separator = ui.input_user(ui.dict_input_user[',/;'])

    print(ui.dict_output_user['выбранный символ'],separator)

    with open(path_and_base_name, mode = "w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = separator, lineterminator = "\r")

        for row in collection:

            file_writer.writerow(row[:6])

        ui.information_for_user(ui.dict_output_user['успешно CSV'])

# Удалить выбранную заметку из сборника
def delete_select_note_in_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    list_name_files = list_name_file()
    name_files = ui.input_user(ui.dict_input_user['удалить заметку'])

    while not name_files in list_name_files:

        ui.input_error(ui.dict_input_error['нет файла'])
        name_files = ui.input_user(ui.dict_input_user['удалить заметку'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)

    except:

        ui.information_for_user(ui.dict_output_user['не таблица'])
        return
    list_name_note = []
    print('\nВ сборнике следующие имена заметок:')

    for i in range(1, len(collection)):
            list_name_note.append(collection[i][3])
            print(collection[i][3])

    name_note = ui.input_user(ui.dict_input_user['удалить 1 заметку'])

    while not name_note in list_name_note:

        ui.input_error(ui.dict_input_error['нет заметки'])
        name_note = ui.input_user(ui.dict_input_user['удалить 1 заметку'])

    for i in range(1, len(collection)):

        if collection[i][3] == name_note:

            del collection[i]
            break

    try:
        with open(path_and_base_name, "wb") as file:
            pickle.dump(collection, file)

        ui.information_for_user(ui.dict_output_user['заметка удалена'])

    except:
        ui.information_for_user(ui.dict_output_user['не создан'])

# Редактирование заметки выбранного сборника
def edit_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()

    name_files = requesting_file_name_from_directory(ui.dict_input_user['редактировать сборник'], ui.dict_input_error['нет файла'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)

    except:

        ui.information_for_user(ui.dict_output_user['не таблица'])
        return
    list_name_note = []
    print('\nВ сборнике следующие имена заметок:')

    for i in range(1, len(collection)):
            list_name_note.append(collection[i][3])
            print(collection[i][3])

    name_note = ui.input_user(ui.dict_input_user['редактировать заметку'])

    while not name_note in list_name_note:

        ui.input_error(ui.dict_input_error['нет заметки'])
        name_note = ui.input_user(ui.dict_input_user['редактировать заметку'])

    for i in range(1, len(collection)):
        if collection[i][3] == name_note:
            collection[i][0] = datetime.datetime.today().strftime("%d.%B.%Y")
            for key in ui.dict_note_fields.keys():
                print('Значение редактируемого поля: ', collection[i][key])
                field = ui.input_user(ui.dict_note_fields[key])

                if key == 2:
                    if field.lower() == 'срочная':
                        collection[i][key] = field

                    elif field.lower() == 'важная':
                        collection[i][key] = field

                    else:
                        collection[i][key] = 'обычная'

                    continue

                if key == 3:

                    while (field in list_name_note and field != collection[i][key]) or field == '':
                        print(field, collection[i][key])
                        ui.input_error(ui.dict_input_error['имя заметки'])
                        field = ui.input_user(ui.dict_note_fields[key])

                    collection[i][key] = field
                    continue


                collection[i][key] = field

            break

    try:
        with open(path_and_base_name, "wb") as file:
            pickle.dump(collection, file)

        ui.information_for_user(ui.dict_output_user['заметка изменена'])

    except:
        ui.information_for_user(ui.dict_output_user['не создан'])

# Проверка наличия рабочей директории и наличия сборников
def are_collections_yes_no() -> bool:
    """
    :return: bool
    """
    if not validate.directory_exists_yes_no(ui.path):

        ui.information_for_user(ui.dict_output_user['Нет Директории'])
        return False

    if list_name_file() == []:

        ui.information_for_user(ui.dict_output_user['Нет сборников'])
        return False

    return True

# Создание новой заметки в новом сборнике
def create_new_note_in_new_collection() -> None:
    """
    :return: None
    """
    path_and_base_name = create_collection()

    if path_and_base_name == None:

        ui.information_for_user(ui.dict_output_user['не создан'])
        return

    collection = create_new_note()

    try:
        with open(path_and_base_name, "wb") as file:
            pickle.dump(collection, file)

        ui.information_for_user(ui.dict_output_user['успешно заметка'])

    except:
        ui.information_for_user(ui.dict_output_user['не создан'])

# Удалить все заметки из сборника
def delete_all_note_in_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    list_name_files = list_name_file()

    name_files = ui.input_user(ui.dict_input_user['удалить все заметки'])

    while name_files not in list_name_files:
        ui.input_error(ui.dict_input_error['нет файла'])
        name_files = ui.input_user(ui.dict_input_user['удалить все заметки'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)
    yes_no = ui.input_user(ui.dict_output_user['Все не восстановить заметки'])
    yes_no_result = validate.choice_yes_no(yes_no, ui.dict_output_user['Все не восстановить заметки'], ui.dict_input_error['y/n'])

    if yes_no_result:

        with open(path_and_base_name, "wb") as file:

            ui.information_for_user(ui.dict_output_user['все заметки удалены'])

# Вывод в консоль всех заметок сборника
def console_output_all_note_from_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    name_files = requesting_file_name_from_directory(ui.dict_input_user['чтение заметок'], ui.dict_input_error['нет файла'])

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:
        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)
    except:
        ui.information_for_user(ui.dict_output_user['пустой'])
        return

    if not validate.data_is_list(collection):

        ui.information_for_user(ui.dict_output_user['пустой'])

        return

    if collection[0][6] != '':

        password = input(ui.dict_input_user['пароль'])

        while password != collection[0][6]:

            ui.input_error(ui.dict_input_error['не верно пароль'])
            password = input(ui.dict_input_user['пароль'])

            if password == collection[0][6]:
                break

            elif password == 'exit':
                return

    print(f'\nВаши заметки - {collection[0][7]}шт')
    print('-' * 120)

    table_note(collection)

# Заполнение полей таблицы
def note(name_note_in_list: list = [''], collection = []) -> list:
    """
    :param name_note_in_list: list Список имен всех заметок сборника
    :param collection: list Пустой список таблицы
    :return:
    """

    print('\033[36mЗаполните следующие поля:\033[0m')
    new_note_yes_no = 'y'
    while new_note_yes_no in ['Y', 'y']:
        note = []
        note.append(datetime.datetime.today().strftime("%d.%B.%Y"))
        for key in ui.dict_note_fields.keys():
            field = input(ui.dict_note_fields[key])
            if key == 2:
                if field.lower() == 'срочная':
                    note.append(field.lower())

                elif field.lower() == 'важная':
                    note.append(field.lower())

                else:
                    note.append('обычная')

                continue

            if key == 3:

                while field in name_note_in_list or field.isspace():
                    print('\033[31mТакое имя заметки существует\033[0m, выберете другое')
                    field = input(ui.dict_note_fields[key])
                name_note_in_list.append(field)

            note.append(field)

        collection.append(note)

        new_note_yes_no = input(ui.dict_input_user['еще одну'])
        new_note_yes_no = 'y' if validate.choice_yes_no(new_note_yes_no, ui.dict_input_user['еще одну'],
                                                        ui.dict_input_error['y/n']) else 'no'
        print()

    return collection

# Формирование массива заметок
def create_new_note() -> list:
    """
    :return: list
    """

    heading = ['Дата', 'Тип', 'Важность', 'Имя', 'Содержание', 'Владелец', '', '']
    collection = note()
    password_yes_no = input(ui.dict_input_user['пароль_y_n'])

    if validate.choice_yes_no(password_yes_no, ui.dict_input_user['пароль'],ui.dict_input_error['y/n']):
        password = input(ui.dict_input_user['пароль'])
        heading[6] = password


    heading[7] = str(len(collection))
    collection.insert(0, heading)

    return collection

# Создание пустого файла сборника
def create_collection() -> (str, None):
    """
    :return: str, None
    """

    if not create_directory(ui.path):

        ui.information_for_user(ui.dict_output_user['не создать'])
        return

    list_name_files = list_name_file()
    name_files = ui.input_user(ui.dict_input_user['Введите имя файла'])

    while True:

        while not validate.check_value_input_user_name_file(name_files):

            ui.input_error(ui.dict_input_error['недопустимое имя'])
            name_files = ui.input_user(ui.dict_input_user['Новое имя файла'])

        if name_files in list_name_files:

            ui.input_error(ui.dict_output_user['уже есть'])
            name_files = ui.input_user(ui.dict_input_user['Новое имя файла'])

        else:
            break

    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:

        with open(path_and_base_name, "wb") as file:

            ui.information_for_user(ui.dict_output_user['успешно файл'])

            return path_and_base_name

    except:

        ui.information_for_user(ui.dict_output_user['не создан'])

        return

# Список имен файлов сборников без расширения
def list_name_file() -> list:
    """
    :return: list
    """
    list_name_file = []
    mask_file = os.path.join(ui.path, '*.ses')
    files = glob.glob(mask_file)

    for elm in files:
        base_name = os.path.basename(elm)
        file_name = os.path.splitext(base_name)
        list_name_file.append(file_name[0])

    return list_name_file

# Вывод меню удаления файлов сборников
def menu_delete_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()

    print()
    ui.menu_del_collection()
    menu_item = ui.input_user(ui.dict_input_user['Удалить сборник меню'])

    while True:

        match menu_item:
            case '1':
                del_selected_file_collection()
                return

            case '2':
                del_all_file_collection()
                return
            case '3':
                return

        ui.input_error(ui.dict_input_error['Ошибка ввода'])
        menu_item = ui.input_user(ui.dict_input_user['Удалить сборник меню'])

# Удалить файл выбранной коллекции
def del_selected_file_collection() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()

    name_files = requesting_file_name_from_directory(ui.dict_input_user['Удалить сборник'], ui.dict_input_error['нет файла'])

    basename = name_files + '.ses'
    yes_no = ui.input_user(ui.dict_output_user['не восстановить'])
    yes_no_result = validate.choice_yes_no(yes_no, ui.dict_output_user['не восстановить'], ui.dict_input_error['y/n'])

    if yes_no_result:
       os.remove(os.path.join(ui.path, basename))
       ui.information_for_user(ui.dict_output_user['успешно удален'])
       print()
       return

    else:
        return

# Удалить все файлы коллекции
def del_all_file_collection() -> None:

    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()
    list_name_files = list_name_file()
    yes_no = ui.input_user(ui.dict_output_user['Все не восстановить'])
    yes_no_result = validate.choice_yes_no(yes_no, ui.dict_output_user['Все не восстановить'], ui.dict_input_error['y/n'])

    if yes_no_result:

        for name in list_name_files:
            basename = name + '.ses'
            os.remove(os.path.join(ui.path, basename))

        ui.information_for_user(ui.dict_output_user['все успешно удалено'])
        print()
        return

    else:
        return

# Переименование выбранного файла сборника
def menu_rename_selected_file_collection() -> None:

    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return

    file_collections()

    name_files = requesting_file_name_from_directory(ui.dict_input_user['Переименовать'], ui.dict_input_error['нет файла'])
    base_name = name_files + '.ses'
    path_and_base_name = os.path.join(ui.path, base_name)

    try:
        with open(path_and_base_name, "rb") as file:
            collection = pickle.load(file)
            result = True
    except:
        result = False

    if result:

        if isinstance(collection, list):

            if collection[0][6] != '':

                password = input(ui.dict_input_user['пароль'])

                while password != collection[0][6]:

                    ui.input_error(ui.dict_input_error['не верно пароль'])
                    password = input(ui.dict_input_user['пароль'])

                    if password == collection[0][6]:
                        break

                    elif password == 'exit':
                        return

    new_name_files = ui.input_user(ui.dict_input_user['Новое имя файла'])

    while True:

        while not validate.check_value_input_user_name_file(new_name_files):

            ui.input_error(ui.dict_input_error['недопустимое имя'])
            new_name_files = ui.input_user(ui.dict_input_user['Новое имя файла'])

        if new_name_files in list_name_file():

            ui.input_error(ui.dict_output_user['уже есть'])
            new_name_files = ui.input_user(ui.dict_input_user['Новое имя файла'])

        else:
            break

    name_files = name_files + '.ses'
    new_name_files = new_name_files + '.ses'
    old_name = os.path.join(ui.path,name_files)
    new_name = os.path.join(ui.path,new_name_files)

    try:
        os.rename(old_name, new_name)
        ui.information_for_user(ui.dict_output_user['успешно переименован'])
        print()
        return

    except:
        ui.information_for_user(ui.dict_input_error['Ошибка переименования'])

# Проверка и создание директории программы
def create_directory(path_file:str) -> bool:
    """
    :param path_file: str Путь к директории программы
    :return: bool Создана директория Да/Нет
    """
    if not validate.directory_exists_yes_no(path_file):

        try:

            os.mkdir(os.path.join(os.getenv('LOCALAPPDATA'), 'Notes'))
            return True

        except:

            return False

    else:

        return True

# Выводит на экран имена файлов сборников без расширения
def file_collections() -> None:
    """
    :return: None
    """
    if not are_collections_yes_no():
        ui.information_for_user(ui.dict_output_user['невозможное действие'])
        return
    list_name_files = list_name_file()

    print(f'\n{ui.dict_output_user['доступно']}')

    for filename in list_name_files:

        print(filename)