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