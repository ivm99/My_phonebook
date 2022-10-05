import json
import csv
import logger

def export():
    try:
        num = int(input('Введите формат для экспорта (1 - .csv или 2 - .txt): '))
        if num == 1:
            export_1()
        elif num == 2:
            export_2()
        else:
            print('Вы ввели неверный номер')
    except:
        print('Вы ввели не число')


def export_1():
    with open('phone_directory.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    count = 0
    with open("phone_directory_export1.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["id", "Фамилия", "Имя", "Телефон", "Описание"])
        for i in data:
            file_writer.writerow([i["id"], i["surname"],i["name"], i["tel"], i["description"]])
            count+=1
    logger.export_csv()
    print(f'Экспорт завершен успешно.')
    print(f'Всего экспортировано {count} контактов.')

def export_2():
    with open('phone_directory.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    count = 0
    str_data = ''
    for elem in data:
            for key, val in elem.items():
                str_data += str(key) + ': ' + str(val) +'\n'
            str_data += '\n'
            count+=1
    with open("phone_directory_export2.txt", mode="w", encoding='utf-8') as file:
        file.write(str_data)
    logger.export_txt()
    print(f'Экспорт завершен успешно.')
    print(f'Всего экспортировано {count} контактов.')
        
