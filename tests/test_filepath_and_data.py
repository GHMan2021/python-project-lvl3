# import os
import tempfile
from pathlib import Path
from page_loader import download


def test_download_returns_filepath(requests_mock):
    with tempfile.TemporaryDirectory() as tmp:
        path_to_file = Path(Path(tmp) / 'ru-hexlet-io-courses.html')
        requests_mock.get('https://ru.hexlet.io/courses')
        result = download('https://ru.hexlet.io/courses', tmp)

        assert path_to_file == result
        assert Path.exists(result)


def test_download_returns_html_page(requests_mock):
    page = Path("tests/fixtures/index.html").read_text()
    page_right = Path("tests/fixtures/ru-hexlet-io-courses.html").read_text()

    with tempfile.TemporaryDirectory() as tmp:
        requests_mock.get('https://ru.hexlet.io/courses', text=page)
        result = download('https://ru.hexlet.io/courses', tmp)

        assert result.read_text() == page_right


def test_download_returns_folder_name(requests_mock):
    with tempfile.TemporaryDirectory() as tmp:
        requests_mock.get('https://ru.hexlet.io/courses')
        download('https://ru.hexlet.io/courses', tmp)
        path_to_folder = Path(Path(tmp) / 'ru-hexlet-io-courses_files')

        assert Path.exists(path_to_folder)
