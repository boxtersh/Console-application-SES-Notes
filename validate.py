import os

# Удаление из ввода пользователя символов паразитов в начале и конце строки
def del_menu_item_symbol(line: str) -> str:
    """
    :param line:
    :return:
    """
    line = line.strip(' ,.<>?/')

    return line