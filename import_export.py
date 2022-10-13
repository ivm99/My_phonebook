# импорт необходимых библиотек
import csv 
import json
import logger

def import_file():
    try:
        n = int(input('Введите формат для импорта (1 - .csv или 2 - .txt): '))
        if n == 1:
            from_csv_to_json()
        elif n == 2:
            from_txt_to_json()
        else:
            print('Вы ввели некорректный номер')
    except:
        print('Вы ввели не число')


def from_csv_to_json():
    # считывание данных из CSV-файла
    with open('phone_directory_import1.csv', 'r', encoding = 'utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))
    # запись данных
    with open('phone_directory.json', 'w', encoding = 'utf-8') as jsonfile: 
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        print('Данные успешно импортированы')
    logger.import_csv()


def from_txt_to_json():
    # считывание данных из txt-файла
    with open('phone_directory_import2.txt', 'r', encoding = 'utf-8') as txtfile:
        #Создаем пустой список
        data = []
        dict_list = []
        #Создаем список строк
        lines = txtfile.readlines()
        #Наполняем список словарями        
        for line in lines:
            if line != '\n':
                line = line.replace(' ','')
                line = line.replace('\n','')
                line = line.split(':')
                data.append(line)
    for i in range(0,len(data)-4,5):
        person = {data[i][0]: int(data[i][1]),
        data[i+1][0]: data[i+1][1],
        data[i+2][0]: data[i+2][1],
        data[i+3][0]: data[i+3][1],
        data[i+4][0]: data[i+4][1]}
        dict_list.append(person)
    with open('phone_directory.json', 'w', encoding='utf-8') as file:
        json.dump(dict_list, file, indent=4, ensure_ascii=False)
        print('Данные успешно импортированы')
    logger.import_txt()
        
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
 