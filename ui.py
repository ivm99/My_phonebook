
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

def show_all_contacts(data):
    for item in data:
        print(f'{item["id"]} {item["surname"]} {item["name"]} {item["tel"]} {item["description"]}')