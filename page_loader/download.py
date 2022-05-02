import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from progress.bar import Bar

from page_loader.logger import logger_config
import logging.config


logging.config.dictConfig(logger_config)
logger = logging.getLogger()


def convert_link_into_name(link):
    lnk = urlparse(link)
    # замена символов на тире в названии сайта
    pattern = r'[\.\:]'
    lnk_netloc = re.sub(pattern, "-", lnk.netloc)
    # замена символа "/" на "-" в пути адреса
    pattern = r'[\/]'
    lnk_path = re.sub(pattern, "-", lnk.path)
    # добавление расширения .html к странице
    if lnk_path.find('.') == -1:
        lnk_path = lnk_path + '.html'
    return "{}{}".format(lnk_netloc, lnk_path)


def save_data(resp, path_to_file, tag_name):
    # Запуск прогрессбара
    filename = Path(path_to_file).name
    bar = Bar('--- Loading file: {}'.format(filename),
              suffix='%(percent).f%%', max=1)
    bar.next()

    if tag_name == 'img':
        path_to_file.write_bytes(resp.content)
    else:
        path_to_file.write_text(resp.text)

    bar.finish()

    return True


def format_page(url, resp_content, output_dir):
    logger.info(f'''
    Run func with the parameters:
    url: {url}
    resp.content: html file
    path to output folder: {output_dir}''')

    name_html = convert_link_into_name(url)
    path_to_html = Path(output_dir / name_html)

    name_dir = re.sub(r'(.html)$', '_files', name_html)
    output_dir = Path(output_dir / name_dir)

    # Запуск прогрессбара
    dir_name = Path(output_dir).name
    bar = Bar('Create directory: {}'.format(dir_name),
              suffix='%(percent).f%%', max=1)
    bar.next()

    try:
        output_dir.mkdir()
    except FileNotFoundError:
        raise FileNotFoundError
    except PermissionError:
        raise PermissionError

    bar.finish()
    logger.info('Directory created')

    soup = BeautifulSoup(resp_content, 'html.parser')

    tag_attr_dict = {'img': 'src', 'link': 'href', 'script': 'src'}

    # список из тегов 'link', 'img', 'script'
    # при наличии атрибута 'src' или 'href'
    tag_list_all = soup.find_all(
        lambda tag:
        tag.name in ['link', 'img', 'script'] and any(
            [tag.has_attr('src'), tag.has_attr('href')]
        )
    )
    logger.info('Created list of selected tags')

    for tag in tag_list_all:
        attr = tag_attr_dict[tag.name]
        attr_link = tag.get(attr)
        # полная ссылка до ресурса
        url_attr = urljoin(url, attr_link)
        # имя аттрибута в новом формате
        name_attr = convert_link_into_name(url_attr)

        if urlparse(url_attr)[1] == urlparse(url)[1]:
            # изменить имя на заданное
            url_attr_name = "{}/{}".format(name_dir, name_attr)
            # сохранить по ссылке в заданном имени
            path_to_file = Path(output_dir / name_attr)
            resp = requests.get(url_attr)
            logger.info(f'Check url_attr: {resp}')
            save_data(resp, path_to_file, tag.name)
            # присвоить новое значение attr
            tag[attr] = url_attr_name

    # Запуск прогрессбара
    filename = Path(path_to_html).name
    bar = Bar('Create html-file: {}'.format(filename),
              suffix='%(percent).f%%', max=1)
    bar.next()

    # запись изменений в html документе
    path_to_html.write_text(soup.prettify())
    logger.info('Overwrite html-file')

    bar.finish()

    return path_to_html


def download(url, output_dir=Path.cwd()):
    logger.info(f'''
    Run the program with the parameters:
    store in the folder: {output_dir},
    site link: {url}''')

    path_to_output_dir = Path(Path.cwd() / output_dir)
    logger.info(f'''
    Absolute path to output directory:
    {path_to_output_dir}''')

    # Проверка подключения к сайту
    try:
        resp = requests.get(url)
    except OSError:
        raise OSError
    logger.info('URL checked')

    path_to_file = format_page(url, resp.content, path_to_output_dir)
    logger.info('Print path_to_file')

    return path_to_file
