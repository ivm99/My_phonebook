import create
import ui
import menu
import check
import search
import logger
import delete
import modol_export
import modol_import
import modify


def main_func():
    menu.main_menu()
    while True:
        #Выбор пункта меню
        punct_menu = check.check_main_menu()
        #Показать список пунктов меню
        if punct_menu == 0:
            menu.main_menu()
        #Добавление нового контакта
        elif punct_menu == 1:
            dict_ph = ui.gen_person()
            create.write_json(dict_ph)
        #Поиск контакта
        elif punct_menu == 2:
            if check.check_directory():                                     #Проверка не пустой ли справочник
                all_contacts = search.read_json('phone_directory.json')     #Считавание всей базы из файла 'phone_directory.json'
                found_contacts = search.search_contact(all_contacts)    #Поиск контакта по критерям
                if found_contacts != []:                                #Проверка найден ли хотя бы один контакт
                    #Выбор пункта - что дальше делаем с контактом
                    futher_action = input('Что вы хотите сделать с найденным контактом: 1 - удалить, 2 - изменить, 3 - ничего: ')
                    if futher_action == '1': 
                        data = delete.delete_contact(found_contacts, all_contacts)     #Удаление контакта
                        modify.write_json_full(data)
                    elif futher_action == '2':
                        data = modify.modify_contact(found_contacts, all_contacts)     #Изменение контакта
                        modify.write_json_full(data)
                    else:
                        menu.main_menu()                                        #Выход в главное меню
        #Вывод всех контактов
        elif punct_menu == 3:           
            if check.check_directory(): ui.show_all_contacts(search.read_json('phone_directory.json'))
        #Изменение контакта
        elif punct_menu == 4:           
            if check.check_directory(): 
                all_contacts = search.read_json('phone_directory.json')
                found_contacts = search.search_contact(all_contacts)
                data = modify.modify_contact(found_contacts, all_contacts)
                modify.write_json_full(data)
        #Удаление контакта
        elif punct_menu == 5:           
            if check.check_directory(): 
                all_contacts = search.read_json('phone_directory.json')
                found_contacts = search.search_contact(all_contacts)
                data = delete.delete_contact(found_contacts, all_contacts)
                modify.write_json_full(data)
        #Экспорт        
        elif punct_menu == 6:           
            if check.check_directory(): 
                modol_export.export()
        elif punct_menu == 7: 
                modol_import.import_file()
        #Завершение работы
        else:
            print('Работа со справочников закончена')
            break
        

