import re
import requests
from pathlib import Path


def conv_to_filename(url):
    # удаление "http(s)://" и ".html(/)", "/" в конце
    pattern = r'^https?\:\/\/|\.html\/?$|\/$'
    filename = re.sub(pattern, "", url)
    # замена ".",  ":",  "/" на "-"
    pattern = r'[\.\:\/]'
    filename = re.sub(pattern, "-", filename)
    filename = "{}.html".format(filename)

    return filename


def save_page(url, output_directory):
    filename = conv_to_filename(url)
    path_to_file = Path(output_directory / filename)

    response = requests.get(url)
    with open(path_to_file, 'w', encoding='utf-8') as f:
        f.write(response.text)

    return path_to_file


def download(url, output_directory=None):
    if not output_directory:
        output_directory = Path.cwd()

    return save_page(url, Path(output_directory))
