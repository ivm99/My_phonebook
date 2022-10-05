import json
import logger

def delete_contact(sorted_data, full_data):
    
    """Функция находит и удаляет заданную запись c контактом"""
    temp = []  
    if len(sorted_data)>1:
        for item in sorted_data:
            temp.append(item["id"])
        index_for_delete = int(input(f'Введите id контакта из данного списка {temp}: '))     #Здесь нужно добавить проверку, что пользователь ввел только индекс из списка
        if index_for_delete in temp:
            confirm = input('Вы уверены, что хотите удалить данный контакт? Да/Нет: ')  # Подтверждение, что пользователь действительно хочет удалить данный контакт
            if confirm.capitalize() == 'Да':    #Ввод подтверждения
                for item in full_data:
                    if index_for_delete == item["id"]:
                        logger.delete_contact(item)
                        full_data.remove(item)    #Если Да, то удаляем контакт из базы
                print('Контакт удален')
                return full_data
            else:    #Иначе, возвращаемся в главное меню
                print('Возврат в главное меню')
                return False
        else: 
            print("Вы ввели неверный номер")
            return False 
    elif len(sorted_data) == 1:
        confirm = input('Вы уверены, что хотите удалить данный контакт? Да/Нет: ')  # Подтверждение, что пользователь действительно хочет удалить данный контакт
        if confirm.capitalize() == 'Да':    #Ввод подтверждения
            for item in full_data:
                    if sorted_data[0]["id"] == item["id"]:
                        logger.delete_contact(item)
                        full_data.remove(item)    #Если Да, то удаляем контакт из базы
            print('Контакт удален')
            return full_data
        else:
            print('Возврат в главное меню')
            return False
    else:
        print('Возврат в главное меню')
        return False 
