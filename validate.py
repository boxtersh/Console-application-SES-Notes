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