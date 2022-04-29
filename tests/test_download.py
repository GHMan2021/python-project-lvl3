import tempfile
from pathlib import Path
from page_loader import download


def test_download_returns_path_file_and_folder_name(requests_mock):
    with tempfile.TemporaryDirectory() as tmp:
        path_to_folder = Path(Path(tmp) / 'ru-hexlet-io-courses_files')
        path_to_file = Path(Path(tmp) / 'ru-hexlet-io-courses.html')

        requests_mock.get('https://ru.hexlet.io/courses')
        result = download('https://ru.hexlet.io/courses', tmp)

        assert path_to_file == result
        assert path_to_folder.exists()


def test_download_returns_page_right_and_img(requests_mock):
    page = Path("tests/fixtures/test/index.html").read_text()
    page_right = Path("tests/fixtures/test/ru-hexlet-io-courses.html")

    img = Path("tests/fixtures/test/nodejs.png").read_bytes()

    script = Path("tests/fixtures/test/index.html").read_text()

    requests_mock.get('https://ru.hexlet.io/courses', text=page)
    requests_mock.get('https://ru.hexlet.io/assets/application.css', text=page)
    requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=img)
    requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js', text=script)

    with tempfile.TemporaryDirectory() as tmp:
        result = download('https://ru.hexlet.io/courses', tmp)

        path_to_img = Path(Path(tmp) / 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png')
        path_to_script = Path(Path(tmp) / 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js')

        assert page_right.read_text() == result.read_text()
        assert img == path_to_img.read_bytes()
        assert script == path_to_script.read_text()


def test_download_returns_err_path_dir():
    try:
        download('https://ru.hexlet.io/courses', 'non-existent folder')
    except ValueError as error:
        assert error


def test_download_returns_to_output_folder_path(requests_mock):
    page = Path("tests/fixtures/test/index.html").read_text()
    img = Path("tests/fixtures/test/nodejs.png").read_bytes()
    script = Path("tests/fixtures/test/index.html").read_text()

    requests_mock.get('https://ru.hexlet.io/courses', text=page)
    requests_mock.get('https://ru.hexlet.io/assets/application.css', text=page)
    requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=img)
    requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js', text=script)

    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(Path(tmp) / 'output_folder')
        output_dir.mkdir()

        download('https://ru.hexlet.io/courses', output_dir)
        path_to_page = Path(Path(tmp) / 'output_folder' / 'ru-hexlet-io-courses.html')

        assert path_to_page.exists()


def test_download_returns_site_error():
    try:
        with tempfile.TemporaryDirectory() as tmp:
            download('https://uu.hexlet.io/courses', tmp)
    except ConnectionError as error:
        assert error
