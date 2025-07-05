import os, validate

# Вывод строки приветствия в начале и конце программы
def print_hi_bye(messag: str) -> None:
    """
    :param messag: Приветственное сообщение
    :return: None
    """
    print(f'\n{messag}')

# Вывод меню рабочая директория программы
def menu_one() -> str:
    """
    Меню программы. Рабочая директория есть, но нет ни одного сборника заметок
    :return: str
    """
    print(f'\n\033[35mУ Вас нет ни одного сборника\033[0m\n\033[36mМеню:\033[0m')
    for key in dict_menu_one.keys():
        print(f'\033[36m{key}\033[0m - {dict_menu_one[key]}')

    print()
    numb_menu = 'menu_one'

    return numb_menu

# Вывод меню работы со сборниками
def menu_collection() -> str:
    """
    Меню работы с каталогами (файлами)
    :return:
    """
    print(f'\n\033[36mМеню работы со сборниками:\033[0m')
    for key in dict_menu_collection.keys():
        print(f'\033[36m{key}\033[0m - {dict_menu_collection[key]}')

    print()
    numb_menu = 'menu_collection'

    return numb_menu









