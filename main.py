from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas
import collections

CURRENT_YEAR = date.today().year
FOUNDATION_YEAR = 1920
YEARS = CURRENT_YEAR - FOUNDATION_YEAR

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')


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
    else:
        return f"{years} лет"


def load_wine_data():
    first_wines = pandas.read_excel('wine.xlsx').T.to_dict()
    second_wines = pandas.read_excel('wine2.xlsx', na_values='None', keep_default_na=False).T.to_dict()
    third_wines = pandas.read_excel('wine3.xlsx', na_values='None', keep_default_na=False).T.to_dict()
    return first_wines, second_wines, third_wines


def generate_html(years, wines):
    rendered_page = template.render(
        years=get_year_word_form(years),
        wines=wines
    )
    with open('template.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    first_wines, second_wines, third_wines = load_wine_data()
    grouped_wines = group_production(third_wines)
    generate_html(YEARS, grouped_wines)
    run_server()


if __name__ == '__main__':
    main()
