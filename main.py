from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas
import collections
import argparse

CURRENT_YEAR = date.today().year
FOUNDATION_YEAR = 1920
YEARS = CURRENT_YEAR - FOUNDATION_YEAR

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def get_input_data():
    parser = argparse.ArgumentParser(description='Данный скрипт структурирует меню и возраст сайта и сразу же вносит изменения в файл сайта')
    parser.add_argument('-path', '--path_to_xlsx_file', help='Путь до .xlsx вайла вашего меню', type=str, default='wine.xlsx')
    parser.parse_args()


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


def load_wine_data():
    wines = pandas.read_excel('wine3.xlsx', na_values='None', keep_default_na=False).T.to_dict()
    return wines


def generate_html(years, wines, template):
    rendered_page = template.render(
        years=get_year_word_form(years),
        wines=wines
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    template = env.get_template('template.html')
    wines = load_wine_data()
    grouped_wines = group_production(wines)
    generate_html(YEARS, grouped_wines, template)
    run_server()


if __name__ == '__main__':
    main()
