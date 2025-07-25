import os

# Удаление из ввода пользователя символов паразитов в начале и конце строки
def del_menu_item_symbol(line: str) -> str:
    """
    :param line:
    :return:
    """
    line = line.strip(' ,.<>?/')

    return line

# Запрос да/нет от пользователя на выполнение действия
def choice_yes_no(result: str, message: str, error: str) -> bool:
    """
    :param result: Ввод от пользователя
    :param message: действие программы требующее подтверждение
    :param error: сообщение об ошибке в случае неверного ввода
    :return: bool
    """

    result = del_menu_item_symbol(result)

    while result not in ['Y', 'y', 'N', 'n']:
        print(error)
        result = input(message)
        result = del_menu_item_symbol(result)

    if result in ['Y', 'y']:
        return True

    return False

# Проверка выбора пункта меню в зависимости от активного меню
def check_value_menu_item(result_user_input, numb_menu) -> bool:
    """
    :param result_user_input: значение пункта меню
    :param numb_menu: ключ активации меню
    :return: bool
    """
    if numb_menu == 'menu_one':
        return result_user_input in ['1', '2', 'exit']

    elif numb_menu == 'menu_collection':
        return result_user_input in ['1', '2', '3', '4', '5', '6', '7', 'exit']

    elif numb_menu == 'menu_note':
        return result_user_input in ['1', '2', '3', '4', '5', '6', '7', '8', 'exit']

    else:
        return False

# Проверка допустимости имени файла
def check_value_input_user_name_file(input_user_name_file: str) -> bool:
    """
    :param input_user_name_file: Имя файла от пользователя
    :return: Допустимое имя Да/Нет
    """
    for symbol in input_user_name_file:

        if symbol not in acceptable_characters:
            return False

    return True

# Проверка cуществует директория да/нет
def directory_exists_yes_no(path_the_directory: str) -> bool:
    """
    :param path_file: Путь к директории программы
    :return: Да/нет
    """
    return os.path.exists(path_the_directory)

# Существует файл в директории да/нет
def file_exists_in_directory(path_the_directory, file) -> bool:

    return file in os.listdir(path_the_directory)

# Каталог пуст да/нет
def catalog_is_empty(path_the_directory) -> bool:

    return len(os.listdir(path_the_directory)) == 0

# Проверка экземпляра на класс лист
def data_is_list(lst: (None, list)) -> bool:
    """
    :param lst: список
    :return: bool
    """
    return isinstance(lst, list)

# Строка допустимых символов имени файла
acceptable_characters = ('-_,.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
                            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя')