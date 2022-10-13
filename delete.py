import json
import logger

def delete_contact(sorted_data, full_data):
    
    """Функция находит и удаляет заданную запись c контактом"""
    
    for item in full_data:
        if sorted_data["id"] == item["id"]:
            full_data.remove(item)    
            logger.delete_contact(item)
    print('Контакт удален')
    return full_data

