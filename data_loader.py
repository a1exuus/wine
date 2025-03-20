import pandas
import collections
import argparse
import sys


def get_input_data():
    parser = argparse.ArgumentParser(description='Данный скрипт структурирует меню и возраст сайта и сразу же вносит изменения в файл сайта')
    parser.add_argument('-path', '-path_to_xlsx_file', help='Путь до .xlsx файла вашего меню', type=str)
    parser.add_argument('-command', choices=['runserver'], help='Команды для скрипта')
    return parser.parse_args(sys.argv[1:]).path


def load_wine_data(path_to_xlsx):
    wines = pandas.read_excel(f'{path_to_xlsx}.xlsx', na_values='None', keep_default_na=False).T.to_dict()
    return wines


def group_production(production):
    output = collections.defaultdict(list)
    for _, product in production.items():
        if product:
            output[product['Категория']].append(product)
    return output


def get_year_word_form(years: int) -> str:
    if 11 <= years % 100 <= 19:
        return f"{years} лет"
    last_digit = years % 10
    if last_digit == 1:
        return f"{years} год"
    elif 2 <= last_digit <= 4:
        return f"{years} года"
    return f"{years} лет"
