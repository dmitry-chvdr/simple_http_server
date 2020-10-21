import requests

BASE_URL = 'http://127.0.0.1:8000/file/'


def upload_file():
    with open('requirements.txt', 'rb') as file:
        response = requests.post(BASE_URL, file)
        return response


def test_upload_file():
    response = upload_file()
    assert response.status_code == 201


def test_download_file():
    file_hash = upload_file().content.decode()
    response = requests.get(BASE_URL + file_hash)
    assert response.status_code == 200


def test_delete_file():
    file_hash = upload_file().content.decode()
    response = requests.delete(BASE_URL + file_hash)
    assert response.status_code == 204


def test_download_file_not_exist():
    file_hash = '115123asd15152312aa'
    response = requests.get(BASE_URL + file_hash)
    assert response.status_code == 404


def test_delete_file_not_exist():
    file_hash = '115123asd15152312aa'
    response = requests.delete(BASE_URL + file_hash)
    assert response.status_code == 404
