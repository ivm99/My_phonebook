import json
import logger


def modify_contact(sorted_data, full_data):
    """Функция находит и изменяет заданную запись c контактом"""
    temp = []

    if len(sorted_data) > 1:
        for i in sorted_data:
            temp.append(int(i["id"]))
        # Здесь нужно добавить проверку, что пользователь ввел только индекс из списка
        id_for_change = int(input(f'Введите id контакта из данного списка {temp}: '))
        if id_for_change in temp:
            index_for_change = search_of_index_to_modify(id_for_change, full_data)
            field_to_change = int(input(
                'Что вы хотите изменить: 1 - Фамилию, 2 - Имя, 3 - номер, 4 - комментарий: '))
            if field_to_change == 1:
                surname = input("Введите новую фамилию: ")
                full_data[index_for_change]["surname"] = surname
                print(
                    f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
                logger.change_con(full_data[index_for_change])
                return full_data
            elif field_to_change == 2:
                name = input("Введите новое имя: ")
                full_data[index_for_change]["name"] = name
                print(
                    f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
                logger.change_con(full_data[index_for_change])
                return full_data
            elif field_to_change == 3:
                tel = input("Введите новый номер: ")
                full_data[index_for_change]["tel"] = tel
                print(
                    f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
                logger.change_con(full_data[index_for_change])
                return full_data
            elif field_to_change == 4:
                description = input("Введите новый комментарий: ")
                full_data[index_for_change]["description"] = description
                print(
                    f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
                logger.change_con(full_data[index_for_change])
                return full_data
        else:
            print("Вы ввели неверный номер")
            return False
    elif len(sorted_data) == 1:
        #Поиск индекса записи в общей базе, которую нужно изменить
        id_for_change = take_id_from_dictionary(sorted_data)
        index_for_change = search_of_index_to_modify(id_for_change, full_data)
        field_to_change = input('Что вы хотите изменить: 1 - Фамилию, 2 - Имя, 3 - номер, 4 - комментарий: ')
        if field_to_change == '1':
            surname = input("Введите новую фамилию: ")
            full_data[index_for_change]["surname"] = surname
            print(f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
            logger.change_con(full_data[index_for_change])
            return full_data
        elif field_to_change == '2':
            name = input("Введите новое имя: ")
            full_data[index_for_change]["name"] = name
            print(f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
            logger.change_con(full_data[index_for_change])
            return full_data
        elif field_to_change == '3':
            tel = input("Введите новый номер: ")
            full_data[index_for_change]["tel"] = tel
            print(f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
            logger.change_con(full_data[index_for_change])
            return full_data
        elif field_to_change == '4':
            description = input("Введите новый комментарий: ")
            full_data[index_for_change]["description"] = description
            print(f'Измененный контакт: {full_data[index_for_change]["id"]} {full_data[index_for_change]["surname"]} {full_data[index_for_change]["name"]} {full_data[index_for_change]["tel"]} {full_data[index_for_change]["description"]}')
            logger.change_con(full_data[index_for_change])
            return full_data
    else:
        print('Возврат в главное меню')
        return False

def take_id_from_dictionary(sorted_data):
    id = sorted_data[0]["id"]
    return id

def search_of_index_to_modify(id, full_data):
    for i, item in enumerate(full_data):
            for key, val in item.items():
                if key == "id" and val == id:
                    index_for_change = i
    return index_for_change

def write_json_full(data):
    if data == False:
        return 'Возврат в главное меню'
    else:
        with open('phone_directory.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print('База данных успешно обновлена')
           
