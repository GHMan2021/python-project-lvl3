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
    with open("tests/fixtures/index.html") as f:
        page = f.read()

    with open("tests/fixtures/ru-hexlet-io-courses.html") as f:
        page_correct = f.read()

    with tempfile.TemporaryDirectory() as tmp:
        requests_mock.get('https://ru.hexlet.io/courses', text=page)
        result = download('https://ru.hexlet.io/courses', tmp)

        with open(result) as f:
            assert f.read() == page_correct
