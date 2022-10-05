import json
from colorama import Fore, Back, Style

def check_main_menu():
    """
    Проверка корректности ввода пунка меню.
    """
    while True:
        try:
            num = int(
                input(Fore.BLACK + "" + Back.GREEN + 'Выберите пункт меню (0 - показать пункты меню): ' + Style.RESET_ALL))
            if 0 <= num < 9:
                return num
            else:
                print(Fore.BLACK + "" + Back.YELLOW + 'Такого пункта в меню нет. Попробуйте еще раз.' + Style.RESET_ALL)
        except ValueError:
            print(Fore.BLACK + "" + Back.RED + 'Вы ввели некорректное значение! Попробуйте снова.' + Style.RESET_ALL)


def check_directory():
    """
    Проверка, пустой ли справочник.
    """
    try:
        with open('phone_directory.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data != []: return True
    except ValueError:
        print(Fore.BLACK + "" + Back.RED + 'Ваш справочник пока еще пустой!' + Style.RESET_ALL)
        return False

