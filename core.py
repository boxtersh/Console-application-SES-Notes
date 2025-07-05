import os, ui, time, validate, modul, glob

def start()-> None:
    """
    :return: None
    """
    os.system('cls')
    time.sleep(1)
    ui.print_hi_bye(ui.dict_hi['Привет'])
    time.sleep(2)
    os.system('cls')
    numb_menu = ui.menu_options()

# Основной цикл программы

    while True:

        match numb_menu:
            case 'menu_one': ui.menu_one()
            case 'menu_collection': ui.menu_collection()
            case 'menu_note': ui.menu_note()

        result_user_input = ui.select_item_menu(numb_menu)
        result = validate.check_value_menu_item(result_user_input, numb_menu)

        if result:

            if numb_menu == 'menu_one':

                match result_user_input:
                    case '1': modul.create_collection()                         # Создать сборник заметок
                    case '2': modul.create_new_note_in_new_collection()         # Создать заметку в новом сборнике
                    case 'exit': break                                          # Выход из программы

            elif numb_menu == 'menu_collection':

                match result_user_input:
                    case '1': modul.file_collections()                          # Показать доступные сборники заметок
                    case '2': modul.console_output_all_note_from_collection()   # Вывести заметки сборника
                    case '3': modul.create_collection()                         # Создать сборник заметок
                    case '4': modul.menu_rename_selected_file_collection()      # Переименовать сборник заметок
                    case '5': modul.menu_delete_collection()                    # Удалить сборник заметок
                    case '6': numb_menu = 'menu_note'                           # Меню работы с заметками
                    case '7': modul.exporting_collection_in_CSV_file()          # Экспорт сборника заметок в CSV файл
                    case 'exit': break

            elif numb_menu == 'menu_note':

                match result_user_input:
                    case '1': modul.create_new_note_in_new_collection()         # Создать заметки в новом сборнике
                    case '2': modul.add_notes_collection()                      # Добавить заметки в сборник
                    case '3': modul.console_output_all_note_from_collection()   # Вывести заметки сборника
                    case '4': modul.edit_collection()                           # Редактировать заметку
                    case '5': modul.sorting()                                   # Сортировать заметки
                    case '6': modul.delete_select_note_in_collection()          # Удалить заметку
                    case '7': modul.delete_all_note_in_collection()             # Удалить ВСЕ заметки
                    case '8': numb_menu = 'menu_collection'                     # Меню работы со сборниками заметок
                    case 'exit': break

            if numb_menu == 'menu_note':
                numb_menu = 'menu_note'

            else:
                numb_menu = ui.menu_options()


        else:
            print('\033[31mОшибка ввода пункта меню\033[0m, повторите ввод')


    os.system('cls')
    time.sleep(1)
    ui.print_hi_bye(ui.dict_hi['Пока'])
    time.sleep(2)
    os.system('cls')