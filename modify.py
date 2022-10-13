import json
import logger

def modify_contact(sorted_data, full_data, field_to_change, text):
    """Функция находит и изменяет заданную запись c контактом"""

    #Поиск индекса записи в общей базе, которую нужно изменить
    id_for_change = sorted_data["id"]
    index_for_change = search_of_index_to_modify(id_for_change, full_data)
    if field_to_change == '1':
        full_data[index_for_change]["surname"] = text
        logger.change_con(full_data[index_for_change])
        return full_data
    elif field_to_change == '2':
        full_data[index_for_change]["name"] = text
        logger.change_con(full_data[index_for_change])
        return full_data
    elif field_to_change == '3':
        full_data[index_for_change]["tel"] = text
        logger.change_con(full_data[index_for_change])
        return full_data
    elif field_to_change == '4':
        full_data[index_for_change]["description"] = text
        logger.change_con(full_data[index_for_change])
        return full_data


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
           
