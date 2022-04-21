import re
import requests
from pathlib import Path


def conv_name(url):
    # удаление "http(s)://" и ".html(/)", "/" в конце
    pattern = r'^https?\:\/\/|\.html\/?$|\/$'
    name = re.sub(pattern, "", url)
    # замена ".",  ":",  "/" на "-"
    pattern = r'[\.\:\/]'
    name = re.sub(pattern, "-", name)

    return name


def save_data(url, output_directory):
    name = conv_name(url)
    filename = "{}.html".format(name)
    path_to_file = Path(output_directory / filename)

    response = requests.get(url)
    path_to_file.write_text(response.text)
    # создание папки *_files
    folder_name = "{}_files".format(name)
    Path(output_directory / folder_name).mkdir()

    return path_to_file

def download(url, output_directory=None):
    output_directory = Path(Path.cwd() / output_directory)
    path_to_file = save_data(url, output_directory)

    return path_to_file
