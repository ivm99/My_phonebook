import json

def read_json(file):
    try:
         with open('phone_directory.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except:
        print('В базе еще нет ни одного контакта :(')

def search_contact(data, text):
    found_contacts = []
    for index, contact in enumerate(data):
        if text.lower() in contact["surname"].lower() or text.lower() in contact["name"].lower() or text.lower() in str(contact["tel"]) or text.lower() in contact["description"].lower():
            found_contacts.append(contact)    
            print(f'Найден контакт: {contact["id"]} {contact["surname"]} {contact["name"]} {contact["tel"]} {contact["description"]}')    #Выводим заданный контакт      
    return found_contacts


