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
    img = Path("tests/fixtures/test1/nodejs.png").read_bytes()
    page = Path("tests/fixtures/test1/index.html").read_text()
    page_right = Path("tests/fixtures/test1/ru-hexlet-io-courses.html")

    with tempfile.TemporaryDirectory() as tmp:
        requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=img)
        requests_mock.get('https://ru.hexlet.io/courses', text=page)

        result = download('https://ru.hexlet.io/courses', tmp)
        path_to_img = Path(Path(tmp) / 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png')

        assert result.read_text() == page_right.read_text()
        assert img == path_to_img.read_bytes()
