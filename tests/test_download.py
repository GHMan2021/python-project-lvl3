import tempfile
from pathlib import Path
import pytest
from page_loader import download
from urllib.parse import urljoin


TEST_URL = 'https://ru.hexlet.io/courses'
TEST_URL_CSS = 'https://ru.hexlet.io/assets/application.css'
TEST_URL_PNG = 'https://ru.hexlet.io/assets/professions/nodejs.png'
TEST_URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'


def test_download_returns_path_file_and_folder_name(requests_mock):
    with tempfile.TemporaryDirectory() as tmp:
        path_to_folder = Path(Path(tmp) / 'ru-hexlet-io-courses_files')
        path_to_file = Path(Path(tmp) / 'ru-hexlet-io-courses.html')

        requests_mock.get(TEST_URL)
        result = download(TEST_URL, tmp)

        assert str(path_to_file) == result
        assert path_to_folder.exists()


def test_download_returns_page_right_and_img(requests_mock):
    page = Path("tests/fixtures/test/index.html").read_bytes()
    page_right = Path("tests/fixtures/test/ru-hexlet-io-courses.html").read_bytes()
    img = Path("tests/fixtures/test/nodejs.png").read_bytes()
    script = Path("tests/fixtures/test/index.html").read_bytes()

    requests_mock.get(TEST_URL, content=page)
    requests_mock.get(TEST_URL_CSS, content=page)
    requests_mock.get(TEST_URL_PNG, content=img)
    requests_mock.get(TEST_URL_JS, content=script)

    with tempfile.TemporaryDirectory() as tmp:
        download(TEST_URL, tmp)

        path_to_img = Path(Path(tmp) / 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png')
        path_to_script = Path(Path(tmp) / 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js')
        path_to_page = Path(Path(tmp) / 'ru-hexlet-io-courses.html')

        assert page_right == path_to_page.read_bytes()
        assert img == path_to_img.read_bytes()
        assert script == path_to_script.read_bytes()


def test_download_returns_to_output_folder_path(requests_mock):
    page = Path("tests/fixtures/test/index.html").read_bytes()
    img = Path("tests/fixtures/test/nodejs.png").read_bytes()
    script = Path("tests/fixtures/test/index.html").read_bytes()

    requests_mock.get(TEST_URL, content=page)
    requests_mock.get(TEST_URL_CSS, content=page)
    requests_mock.get(TEST_URL_PNG, content=img)
    requests_mock.get(TEST_URL_JS, content=script)

    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(Path(tmp) / 'output_folder')
        output_dir.mkdir()

        download(TEST_URL, output_dir)
        path_to_page = Path(Path(tmp) / 'output_folder' / 'ru-hexlet-io-courses.html')

        assert path_to_page.exists()


def test_download_returns_err_path_dir():
    with pytest.raises(FileNotFoundError):
        assert download(TEST_URL, 'non-existent folder')


BASE_URL = 'https://site.com/404'


@pytest.mark.parametrize('code', [404, 500])
def test_download_returns_response_with_error(requests_mock, code):
    url = urljoin(BASE_URL, str(code))
    requests_mock.get(url, status_code=code)

    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(Exception):
            assert download(url, tmp)
