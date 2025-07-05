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