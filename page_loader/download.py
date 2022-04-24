import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def save_data(url, output_dir):
    pattern = r'^https?\:\/\/|\.html\/?$|\/$'
    name_url = re.sub(pattern, "", url)
    # name_url = ru.hexlet.io/courses

    pattern = r'[\.\:\/]'
    name_html = re.sub(pattern, "-", name_url) + '.html'
    path_to_html = Path(output_dir / name_html)

    name_dir = re.sub(pattern, "-", name_url) + '_files'
    output_dir = Path(output_dir / name_dir)
    output_dir.mkdir()

    o = urlparse(url)

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    for img in soup.find_all('img'):
        i = urlparse(img['src'])
        if all([i.scheme != '', i.netloc != o.netloc]):
            continue
        else:
            img_url = urljoin(url, img['src'])
            # https://ru.hexlet.io/assets/java.png

            pattern = r'[\.\:\/]'
            img_name = re.sub(pattern, "-", o.netloc)
            # ru-hexlet-io

            img_name = f"{img_name}{img['src']}"
            # ru-hexlet-io/assets/java.png

            img_name = img_name.replace("/", '-')
            # ru-hexlet-io-assets-java.png

            img_path = Path(output_dir / img_name)
            # .../ru-hexlet-io-assets-java.png

            with open(img_path, 'wb') as f:
                f.write(requests.get(img_url).content)

            img['src'] = f"{name_dir}/{img_name}"

    path_to_html.write_text(soup.prettify())

    # p = Path(Path.cwd() / 'tests/fixtures/test2/ru-hexlet-io-courses.html')
    # soup = BeautifulSoup(p.read_text(), 'html.parser')
    # print(soup.prettify())

    return path_to_html


def download(url, output_dir=None):
    output_dir = Path(Path.cwd() / output_dir)
    path_to_file = save_data(url, output_dir)

    return path_to_file
