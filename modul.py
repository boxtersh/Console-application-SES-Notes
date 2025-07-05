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