
from email import header
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
  def __init__(self) -> None:
      self.base_url = 'https://petfriends.skillfactory.ru'

  def get_api_key(self, email: str, password: str) -> json:
    headers = {
      'email' : email,
      'password' : password
    }    
    res = requests.get(self.base_url + '/api/key', headers=headers)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result 

  def get_list_of_pets(self, auth_key: json, filter: str) -> json:
    headers = {'auth_key' : auth_key['key']}
    filter = {'filter' : filter}
    res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result

  def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
    data = MultipartEncoder(
      fields = {
        'name' : name,
        'animal_type' : animal_type,
        'age' : age,
        'pet_photo' : (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
      }
    ) 
    headers = {'auth_key' : auth_key['key'], 'Content-Type': data.content_type}
    res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result

  def delete_pet(self, auth_key: json, pet_id: str) -> int:
    headers = {'auth_key' : auth_key['key']}
    res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
    status = res.status_code
    return status 

  def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
    headers = {'auth_key' : auth_key['key']}
    data = {
      'name' : name,
      'animal_type' : animal_type,
      'age' : age
    }   
    res = requests.put(self.base_url + f'/api/pets/{pet_id}', headers=headers, data=data)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result

  def add_pet_without_photo(self,auth_key: json, name: str, animal_type: str, age: str) -> json:
    '''Метод отправляет запрос на сервер о создании новой карточки питомца без фото и
        возвращает статус запроса и result в формате JSON с данными питомца'''
    headers = {'auth_key' : auth_key['key']}
    data = {
      'name' : name,
      'animal_type' : animal_type,
      'age' : age,
    }
    res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result

  def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
    '''Метод отправляет запрос на сервер о добавлении фото к карточке питомца с указанным ID и
        возвращает статус запроса и result в формате JSON с измененными данными питомца'''
    data = MultipartEncoder(
      fields = {
        'pet_photo' : (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
      }
    ) 
    headers = {'auth_key' : auth_key['key'], 'Content-Type': data.content_type}
    res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
    status = res.status_code
    try:
      result = res.json()
    except:
      result = res.text
    return status, result





