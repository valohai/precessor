from io import BytesIO

from PIL import Image

from precessor_tests.utils import get_response


def test_precessor_works(monkeypatch):
    response = get_response({
        'PATH_INFO': '/http://example.com/doggo.jpg',
        'QUERY_STRING': 'resize=80x80,lanczos&rotate=90&flip=xy',
    })
    assert response['status'] == '200 OK'
    img = Image.open(BytesIO(response['content']))
    assert img.format == 'JPEG'
    assert img.size == (80, 80)
