import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import config
import create, check, search, delete, modify, import_export

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
PHONEBOOK_OPTION, CREATE_SURNAME, CREATE_NAME, CREATE_PHONE_NUMBER, CREATE_COMMENT, SEARCH_CONTACT, CHOOSE_CONTACT, CHOOSE_ACTION, FIELD_TO_MODIFY, CHANGE_SURNAME, CHANGE_NAME, CHANGE_TEL, CHANGE_COMMENT, CONTACTS_EXPORT, CONTACTS_IMPORT = range(15)


# функция обратного вызова точки входа в разговор
def start(update, _):
    # Начинаем разговор с вопроса
    update.message.reply_text(
    'Выберите пункт меню для продолжения:\n'
        '  1. Записать контакт\n'
        '  2. Найти контакт\n'
        '  3  Показать все контакты\n'
        '  4  Изменить контакт\n'
        '  5. Удалить контак\n'
        '  6. Экспорт контактов\n'
        '  7. Импорт контактов\n\n'
    'Чтобы завершить работу со справочником введите команду /cancel')
    # переходим к этапу `PHONEBOOK_OPTION`
    return PHONEBOOK_OPTION

# Обрабатываем пол пользователя
def phonebook_option(update, _):
    user = update.message.from_user
    # определяем выбранную опцию
    pb_option = update.message.text
    # Пишем в журнал опцию
    logger.info("Выбрана опция %s: %s", user.first_name, pb_option)
    # Следующее сообщение
    # update.message.reply_text(f'Выбрана опция: {pb_option}')
    # переходим к этапу `PHOTO`
    if pb_option == '1':
        update.message.reply_text('Создаем новую запись')
        update.message.reply_text('Введите фамилию')
        return CREATE_SURNAME
    if pb_option == '2':
        update.message.reply_text('Поиск контакта')
        update.message.reply_text('Введите имя контакта, номер телефона или комментарий:')
        return SEARCH_CONTACT
    if pb_option == '3':
        all_contacts = search.read_json('phone_directory.json')
        update.message.reply_text(f'Всего контактов: {len(all_contacts)}')
        for i, contact in enumerate(all_contacts):
            update.message.reply_text(f'Контакт №{i+1}: {contact["surname"]} {contact["name"]} {contact["tel"]} {contact["description"]}')
        return PHONEBOOK_OPTION
    if pb_option == '4' or pb_option == '5':
        update.message.reply_text('Введите имя контакта, номер телефона или комментарий:')
        return SEARCH_CONTACT
    if pb_option == '6':
        update.message.reply_text('Экспорт контактов')
        update.message.reply_text('Выберите формат для экспорта: \n\n'
        '1 - CSV, 2 - TXT')
        return CONTACTS_EXPORT
    if pb_option == '7':
        update.message.reply_text('Импорт контактов')
        update.message.reply_text('Выберите формат для импорта: \n\n'
        '1 - CSV, 2 - TXT')
        return CONTACTS_IMPORT
    

# Обрабатываем фотографию пользователя
def create_contact_surname(update, _):
    global surname
    # определяем пользователя
    user = update.message.from_user
    # берем фамилию 
    surname = update.message.text
    if len(surname) <=20:
        # Пишем в журнал сведения о фото
        logger.info("Фамилия %s: %s", user.first_name, surname)
        # Отвечаем на сообщение
        update.message.reply_text('Введите имя (не более 10 символов)')
        # переходим к этапу `CREATE_NAME`
        return CREATE_NAME
    else:
        update.message.reply_text('Слишком длинная фамилия. Должно быть не более 20 символов, попробуйте еще раз')

def create_contact_name(update, _):
    global name
    # определяем пользователя
    user = update.message.from_user
    # берем имя 
    name = update.message.text
    if len(name) <=10:
        # Пишем в журнал
        logger.info("Имя %s: %s", user.first_name, name)
        # Отвечаем на сообщение
        update.message.reply_text('Введите номер телефона (здесь могут быть только цифры, не более 12 знаков)')
        # переходим к этапу `CREATE_PHONE_NUMBER`
        return CREATE_PHONE_NUMBER
    else:
        update.message.reply_text('Слишком длинное имя. Должно быть не более 10 символов, попробуйте еще раз')


def create_phone_number(update, _):
    global phone_number
    # определяем пользователя
    user = update.message.from_user
    # берем номер телефона 
    phone_number = update.message.text
    if len(phone_number) <= 12:
        try:
            phone_number = int(phone_number)
            logger.info("Номер телефона %s: %s", user.first_name, phone_number)
            # Отвечаем на сообщение
            update.message.reply_text('Введите комментарий (не более 20 символов)')
            # переходим к этапу `CREATE_COMMENT`
            return CREATE_COMMENT
        except:
            update.message.reply_text('Вы ввели не цифры, попробуйте еще раз')
    else:
        update.message.reply_text('Слишком длинный номер. Должно быть не более 12 символов, попробуйте еще раз')
def create_comment(update, _):
    global comment
    # определяем пользователя
    user = update.message.from_user
    # берем комментарий 
    comment = update.message.text
    # Пишем в журнал
    if len(comment) <=20:
        logger.info("Комментарий %s: %s", user.first_name, comment)
        person = create.gen_person(surname, name, phone_number, comment)
        create.write_json(person)
        update.message.reply_text(f'Контакт:\n\n {surname} {name} {phone_number} {comment} \n\nуспешно создан')
        return PHONEBOOK_OPTION
    else:
        update.message.reply_text('Слишком длинный комментарий. Должно быть не более 20 символов, попробуйте еще раз')

str_for_filter = ''

def search_contact(update, _):
    global found_contacts, str_for_filter, all_contacts
    str_for_filter = '^('
     # определяем пользователя
    user = update.message.from_user
    # берем введенный текст 
    s_text = update.message.text
    # Пишем в журнал
    logger.info("Комментарий %s: %s", user.first_name, s_text)
    if check.check_directory():                                     #Проверка не пустой ли справочник 
        all_contacts = search.read_json('phone_directory.json')     #Считавание всей базы из файла 'phone_directory.json'
        found_contacts = search.search_contact(all_contacts, s_text)    #Поиск контакта по критерям
        if found_contacts != []:                                #Проверка найден ли хотя бы один контакт
            update.message.reply_text('Найдены контакты:')
            for index, contact in enumerate(found_contacts):
                update.message.reply_text(f'Контакт №{index+1}: {contact["surname"]} {contact["name"]} {contact["tel"]} {contact["description"]}')
                str_for_filter += f'{index+1}|'
            str_for_filter = str_for_filter[:-1] + ')$'
            print (str_for_filter)
            #Выбор контакта для дальнейших действий
            update.message.reply_text('Выберите контакт (номер):')
            return CHOOSE_CONTACT
        else:
            update.message.reply_text('Такого контакта нет в базе. Попробуйте еще раз')
    else:
            update.message.reply_text('Cправочник пока еще пустой')
            return PHONEBOOK_OPTION
            
def choose_contact(update, _):
    global contact_for_action
    #  определяем пользователя
    user = update.message.from_user
    try:
        contact_index = int(update.message.text)
        if contact_index > 0:
            contact_for_action = found_contacts[contact_index-1]
            # Пишем в журнал
            logger.info("Комментарий %s: %s", user.first_name, f'{contact_for_action["surname"]} {contact_for_action["name"]} {contact_for_action["tel"]} {contact_for_action["description"]}')
            update.message.reply_text('Выбран контакт\n\n'
                                    f'{contact_for_action["surname"]} {contact_for_action["name"]} {contact_for_action["tel"]} {contact_for_action["description"]} \n\n'
                                    'Что вы хотите сделать с найденным контактом:\n\n1 - удалить, 2 - изменить, 3 - ничего:')
            return CHOOSE_ACTION
    except:
        update.message.reply_text('Вы ввели не число. Попробуйте еще раз')
            
            
def choose_action(update, _):        
    #  определяем пользователя
    user = update.message.from_user
    contact_action = update.message.text
    # Пишем в журнал
    logger.info("Комментарий %s: %s", user.first_name, contact_action)
    if contact_action == '1': 
        data = delete.delete_contact(contact_for_action, all_contacts)     #Удаление контакта
        modify.write_json_full(data)
        update.message.reply_text('Контакт удален')
        return PHONEBOOK_OPTION
    elif contact_action == '2':
        update.message.reply_text('Что вы хотите изменить: \n\n1 - Фамилию, 2 - Имя, 3 - номер, 4 - комментарий')
        return FIELD_TO_MODIFY
    else:
        return start(update, _)


def field_to_modify(update, _):  
    global field_to_change
    user = update.message.from_user
    field_to_change = update.message.text
    # Пишем в журнал
    logger.info("Комментарий %s: %s", user.first_name, field_to_change)
    if field_to_change == '1':
        update.message.reply_text('Введите новую фамилию')
        return CHANGE_SURNAME
    elif field_to_change == '2':
        update.message.reply_text('Введите новое имя')
        return CHANGE_NAME
    elif field_to_change == '3':
        update.message.reply_text('Введите новый номер')
        return CHANGE_TEL
    else:
        update.message.reply_text('Введите новый комментарий')
        return CHANGE_COMMENT

def change_surname(update, _):
    global new_surname
    new_surname = update.message.text
    modify.modify_contact(contact_for_action, all_contacts, field_to_change, new_surname)
    modify.write_json_full(all_contacts)
    update.message.reply_text('Контакт изменен')
    return PHONEBOOK_OPTION

def change_name(update, _):
    global new_name
    new_name = update.message.text
    modify.modify_contact(contact_for_action, all_contacts, field_to_change, new_name)
    modify.write_json_full(all_contacts)
    update.message.reply_text('Контакт изменен')
    return PHONEBOOK_OPTION

def change_tel(update, _):
    global new_tel
    new_tel = update.message.text
    modify.modify_contact(contact_for_action, all_contacts, field_to_change, new_tel)
    modify.write_json_full(all_contacts)
    update.message.reply_text('Контакт изменен')
    return PHONEBOOK_OPTION

def change_comment(update, _):
    global new_comment
    new_comment = update.message.text
    modify.modify_contact(contact_for_action, all_contacts, field_to_change, new_comment)
    modify.write_json_full(all_contacts)
    update.message.reply_text('Контакт изменен')
    return PHONEBOOK_OPTION
    
def choose_export_format(update, _):
    export_format = update.message.text
    if check.check_directory(): 
        if export_format == '1':
            import_export.export_1()
            update.message.reply_text('Экспорт завершен успешно')
            return PHONEBOOK_OPTION
        elif export_format == '2':
            import_export.export_2()
            update.message.reply_text('Экспорт завершен успешно')
            return PHONEBOOK_OPTION

def choose_import_format(update, _):
    import_format = update.message.text
    if check.check_directory(): 
        if import_format == '1':
            import_export.from_csv_to_json()
            update.message.reply_text('Импорт завершен успешно')
            return PHONEBOOK_OPTION
        elif import_format == '2':
            import_export.from_txt_to_json()
            update.message.reply_text('Импорт завершен успешно')
            return PHONEBOOK_OPTION


# Обрабатываем команду /skip для фото
def menu(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал
    logger.info("Пользователь %s не отправил фото.", user.first_name)
    # Отвечаем на сообщение
    update.message.reply_text('Вы вышли в главное меню')
    # переходим к этапу `PHONEBOOK_OPTION`
    return phonebook_option(update, _)


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s завершил работу со справочником.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Вы завершили работу со справочником'
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(config.TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            PHONEBOOK_OPTION: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7)$'), phonebook_option)],
            CREATE_SURNAME: [MessageHandler(Filters.all, create_contact_surname), CommandHandler('menu', menu)],
            CREATE_NAME: [MessageHandler(Filters.all, create_contact_name), CommandHandler('menu', menu)],
            CREATE_PHONE_NUMBER: [MessageHandler(Filters.all, create_phone_number), CommandHandler('menu', menu)], 
            CREATE_COMMENT: [MessageHandler(Filters.all, create_comment), CommandHandler('menu', menu)],
            SEARCH_CONTACT: [MessageHandler(Filters.all, search_contact), CommandHandler('menu', menu)],
            CHOOSE_CONTACT: [MessageHandler(Filters.regex(str_for_filter), choose_contact), CommandHandler('menu', menu)],
            CHOOSE_ACTION: [MessageHandler(Filters.regex('^(1|2|3)$'), choose_action), CommandHandler('menu', menu)],
            FIELD_TO_MODIFY: [MessageHandler(Filters.regex('^(1|2|3|4)$'), field_to_modify), CommandHandler('menu', menu)],
            CHANGE_SURNAME: [MessageHandler(Filters.all, change_surname), CommandHandler('menu', menu)],
            CHANGE_NAME: [MessageHandler(Filters.all, change_name), CommandHandler('menu', menu)],
            CHANGE_TEL: [MessageHandler(Filters.all, change_tel), CommandHandler('menu', menu)],
            CHANGE_COMMENT: [MessageHandler(Filters.all, change_comment), CommandHandler('menu', menu)],
            CONTACTS_EXPORT: [MessageHandler(Filters.regex('^(1|2)$'), choose_export_format), CommandHandler('menu', menu)],
            CONTACTS_IMPORT: [MessageHandler(Filters.regex('^(1|2)$'), choose_import_format), CommandHandler('menu', menu)]
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()