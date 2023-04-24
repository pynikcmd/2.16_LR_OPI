#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import datetime


def get_person():
    """""
    Запросить данные о человеке.
    """
    name = input("Фамилия Имя: ")
    number = int(input("Номер телефона: "))
    bday = list(map(int, input("Дата рождения: ").split('.')))
    d_bday = datetime.date(bday[2], bday[1], bday[0])

    # Создать словарь.
    return {
        'name': name,
        'number': number,
        'birthday': d_bday,
    }


def display_people(staff):
    """
    Список данных о людях.
    """
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^14} |'.format(
                "№",
                "Фамилия Имя",
                "Номер телефона",
                "Дата рождения"
            )
        )
        print(line)

        # Вывести данные о всех людях.
        for idx, person in enumerate(staff, 1):
            print(
                f'| {idx:>4} |'
                f' {person.get("name", ""):<30} |'
                f' {person.get("number", 0):<20} |'
                f' {person.get("birthday")}      |'
            )
        print(line)

    else:
        print("Список людей пуст.")


def json_deserial(obj):
    """
    Деериализация объектов datetime
    """
    for i in obj:
        if isinstance(i["birthday"], str):
            i["birthday"] = datetime.datetime.strptime(i["birthday"], '%Y-%m-%d').date()


def json_serial(obj):
    """
    Сериализация объектов datetime
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()


def find_nomer(staff, nomer):
    """
    Выбрать людей с заданным номером телефона.
    """
    # Сформировать список людей.
    result = []

    for n in staff:
        if nomer in n.values():
            result.append(n)

    # Проверка на наличие записей
    if len(result) == 0:
        res = "Запись не найдена"
        return res

    # Возвратить список выбранных людей.
    return result


def save_people(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=json_serial)


def load_people(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    """
    Главная функция программы.
    """
    # Список людей.
    people = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input("Введите команду >>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о человеке.
            person = get_person()

            # Добавить в словарь список.
            people.append(person)
            # Отсортировать список в случае необходимости.
            if len(people) > 1:
                people.sort(key=lambda item: item.get('d_bday', ''))

        elif command == 'list':
            # Отобразить всех людей.
            display_people(people)

        elif command == 'find':
            n = int(input('Введите номер телефона: '))

            # Выбрать людей с заданной фамилией.
            finded = find_nomer(people, n)
            # Отобразить выбранных работников.
            display_people(finded)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_people(file_name, people)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            people = load_people(file_name)
            json_deserial(people)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n"
                  "add - добавить человека;\n"
                  "list - вывести список людей;\n"
                  "find - найти человека по фамилии;\n"
                  "help - отобразить справку;\n"
                  "exit - завершить работу с программой.\n")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
