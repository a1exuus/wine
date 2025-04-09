from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
from data_loader import load_wine_data, group_production, get_year_word_form, get_input_data


def generate_html(years, wines, template):
    rendered_page = template.render(years=get_year_word_form(years), wines=wines)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print("Сервер запущен на http://0.0.0.0:8000")
    server.serve_forever()


def main():
    current_year = date.today().year
    foundation_year = 1920
    years = current_year - foundation_year
    
    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    path_to_xlsx = get_input_data()

    if path_to_xlsx[1] == 'runserver':
        run_server()

    wines = load_wine_data(path_to_xlsx)
    grouped_wines = group_production(wines)
    generate_html(years, grouped_wines, template)
    
    run_server()


if __name__ == '__main__':
    main()
