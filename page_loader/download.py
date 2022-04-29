import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError
import logging


param_format = '%(filename)s::%(funcName)s::%(levelname)s: %(message)s'
logging.basicConfig(level='WARNING', format=param_format)


def check_tag(tag, u_netlog):
    if any([tag.has_attr('src'), tag.has_attr('href')]):
        attr = tag.get('href', tag.get('src'))
        a = urlparse(attr)
        if all([a.scheme != '', a.netloc != u_netlog]):
            return False
        return True
    return False


def conv_name(attr):
    a = urlparse(attr)
    pattern = r'[\.\:]'
    a_netloc = re.sub(pattern, "-", a.netloc)
    pattern = r'[\/]'
    a_path = re.sub(pattern, "-", a.path)
    if a_path.find('.') == -1:
        a_path = a_path + '.html'
    return "{}{}".format(a_netloc, a_path)


def save_data_to_dir(output_dir, tag_lists):
    for _dict in tag_lists:
        if _dict['type'] == 'img':
            resp = requests.get(_dict['link'])
            path_to_file = Path(output_dir / _dict['filename'])
            path_to_file.write_bytes(resp.content)
        else:
            resp = requests.get(_dict['link'])
            path_to_file = Path(output_dir / _dict['filename'])
            path_to_file.write_text(resp.text)
    return True


def format_page(url, output_dir):

    req = Request(url)
    try:
        urlopen(req)
    except URLError as e:
        msg = "Other errors"
        if hasattr(e, 'reason'):
            msg = f"We failed to reach a server. Reason: {e.reason}"
            logging.warning(msg)
        elif hasattr(e, 'code'):
            msg = f"The server couldn\'t fulfill the request. " \
                  f"Error code: {e.code}"
            logging.warning(msg)
        return msg

    u = urlparse(url)
    u_netlog = u.netloc

    name_html = conv_name(url)
    path_to_html = Path(output_dir / name_html)

    name_dir = re.sub(r'(.html)$', '_files', name_html)
    output_dir = Path(output_dir / name_dir)
    output_dir.mkdir()

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    tag_list_all = soup(['link', 'img', 'script'])

    tag_lists = []
    for tag in tag_list_all:
        if check_tag(tag, u_netlog):
            tag_dict = {}
            # замена атрибута тега, список словарей с ресурсами
            if tag.name == 'link':
                full_url = urljoin(url, tag['href'])
                tag['href'] = full_url
                tag['href'] = "{}/{}".format(name_dir, conv_name(full_url))

                # словарь для загрузки файлов
                tag_dict['link'] = full_url
                tag_dict['filename'] = str(conv_name(full_url))
                tag_dict['type'] = 'text'
                # список словарей
                tag_lists.append(tag_dict)
            else:
                full_url = urljoin(url, tag['src'])
                tag['src'] = full_url
                tag['src'] = "{}/{}".format(name_dir, conv_name(full_url))

                # словарь для загрузки файлов
                tag_dict['link'] = full_url
                tag_dict['filename'] = str(conv_name(full_url))
                tag_dict['type'] = 'img'
                # список словарей
                tag_lists.append(tag_dict)

    path_to_html.write_text(soup.prettify())

    # скачивание файлов в папку
    save_data_to_dir(output_dir, tag_lists)

    return path_to_html


def download(url, output_dir=None):
    logging.info(f'''
    Run the program with the parameters:
    save to folder - {output_dir}
    link to the page - {url}
    --------------------------''')

    output_dir = Path(Path.cwd() / output_dir)

    if not Path.exists(output_dir):
        msg = 'This folder does not exist or path'
        logging.warning(msg)
        return msg

    path_to_file = format_page(url, output_dir)

    return path_to_file
