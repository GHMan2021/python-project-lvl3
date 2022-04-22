import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup


def save_data(url, output_dir):
    # удаление "http(s)://" и ".html(/)", "/" в конце
    # url = ru.hexlet.io/courses
    pattern = r'^https?\:\/\/|\.html\/?$|\/$'
    url_temp = re.sub(pattern, "", url)
    # выделение адреса сайта
    # name_site = ru.hexlet.io
    name_site = url_temp.split('/')[0]
    # замена ".",  ":",  "/" на "-"
    # name_site = ru-hexlet-io
    pattern = r'[\.\:\/]'
    name_site = re.sub(pattern, "-", name_site)
    # name_url = ru-hexlet-io-courses
    pattern = r'[\.\:\/]'
    name_url = re.sub(pattern, "-", url_temp)
    # запись пути файла, возвращаемое значение функции path_to_file
    file_name = "{}.html".format(name_url)
    path_to_file = Path(output_dir / file_name)
    # создание папки
    folder_name = "{}_files".format(name_url)
    Path(output_dir / folder_name).mkdir()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img'):
        src_path = img['src'].replace('/', '-')
        img['src'] = "{}/{}{}".format(folder_name, name_site, src_path)
    path_to_file.write_text(soup.prettify())

    return path_to_file


def download(url, output_dir=None):
    output_dir = Path(Path.cwd() / output_dir)
    path_to_file = save_data(url, output_dir)

    return path_to_file
