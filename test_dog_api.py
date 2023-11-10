# Тест на получение списка всех пород собак

import requests
import pytest

@pytest.fixture
def api_request():
    def make_request(endpoint):
        response = requests.get(f"https://dog.ceo/api/{endpoint}")
        response.raise_for_status()
        return response.json()
    return make_request

@pytest.mark.parametrize("breed", ["hound", "retriever", "bulldog"])
def test_get_all_breeds(api_request, breed):
    data = api_request("breeds/list/all")
    assert breed in data["message"]

def test_get_random_dog_image(api_request):
    data = api_request("breeds/image/random")
    assert data["status"] == "success"
    assert data["message"].endswith(".jpg")

# Тест на получение списка подпороды для заданной породы

import requests
import pytest

@pytest.mark.parametrize("breed", ["collie", "poodle", "bulldog"])
def test_get_subbreeds(breed):
    url = f"https://dog.ceo/api/breed/{breed}/list"
    
    # Выполняем запрос
    response = requests.get(url)
    
    # Проверяем успешность запроса
    assert response.status_code == 200, f"Failed to retrieve subbreeds for {breed}. Status code: {response.status_code}"
    
    # Проверяем, что в ответе есть ожидаемая порода
    data = response.json()
    assert breed in data["message"], f"Expected subbreed '{breed}' not found in the response for {breed}. Response: {data}"

# Тест на получение информации о случайной фотографии собаки и её породе

import requests
import pytest

@pytest.mark.parametrize("count", [1, 2, 3, 4])
def test_get_random_dog_info(count):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["message"].endswith(".jpg")

    breed = data["message"].split("/")[-2]
    response_breed = requests.get(f"https://dog.ceo/api/breed/{breed}/list")
    data_breed = response_breed.json()
    assert response_breed.status_code == 200
    assert breed in data_breed["message"]