from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas
import collections

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

current_year = date.today().year
years = current_year - 1920

first_wines_read_out = pandas.read_excel('wine.xlsx').T.to_dict()
second_wines_read_out = pandas.read_excel('wine2.xlsx', na_values='None', keep_default_na=False).T.to_dict()
third_wines_read_out = pandas.read_excel('wine3.xlsx', na_values='None', keep_default_na=False).T.to_dict()


def group_production(production):
    output = collections.defaultdict(list)
    for i, product in production.items():
        if product:
            output[product['Категория']].append(product)
        else:
            continue
    return output


def get_year_word_form(years: int) -> str:
    if 11 <= years % 100 <= 19:
        return str(years) + " лет"
    last_digit = years % 10
    if last_digit == 1:
        return str(years) + " год"
    elif 2 <= last_digit <= 4:
        return str(years) + " года"
    else:
        return str(years) + " лет"


output = group_production(second_wines_read_out)


rendered_page = template.render(
    years=get_year_word_form(years),
    wines=group_production(third_wines_read_out)
)

with open('template.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

