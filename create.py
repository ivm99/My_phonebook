import json
import logger


def gen_person():
    surname = input('Введите фамилию:')
    name = input('Введите имя:')
    tel = input('Введите номер телефона:')
    description = input('Дополнительная информация:')

    person = {
        'id':0,
        'surname': surname,
        'name': name,
        'tel': tel,
        'description': description
    }
    return person


def write_json(person_dict):
    try:
        with open('phone_directory.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except:
        data = []
    last_id = int(data[len(data)-1]["id"])
    person_dict["id"] = last_id + 1
    data.append(person_dict)
    with open('phone_directory.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logger.create_contact(person_dict)
    print('Контакт успешно добавлен')




