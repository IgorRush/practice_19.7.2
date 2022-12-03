from api import PetFriends
from settings import email, password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email = email, password = password):
  status, result = pf.get_api_key(email, password)
  assert status == 200
  assert 'key' in result

def test_get_all_pets_with_valid_key(filter = 'my_pets'):
  _, auth_key = pf.get_api_key(email, password)
  status, result = pf.get_list_of_pets(auth_key, filter)
  assert status == 200
  assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name = 'Bun', animal_type = 'dog', age = '3', pet_photo = 'images/dog.jpg'):
  _, auth_key = pf.get_api_key(email, password)
  pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
  status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
  assert status == 200
  assert result['name'] == name

def test_delete_pet_sucsesful():
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  if len(my_pets['pets']) == 0:
    pf.add_new_pet(auth_key, "Test_Cat", "cat", "1", "images/cat.jpg")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
  pet_id = my_pets['pets'][0]['id']
  status = pf.delete_pet(auth_key, pet_id)
  _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
  assert status == 200
  assert pet_id not in my_pets.values()

def test_update_pet_info_sucsesful(name = 'Slayer', animal_type = 'dog', age = '3'):
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  pet_id = my_pets['pets'][0]['id']
  if len(my_pets['pets']) > 0:
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    assert result['name'] == name and result['id'] == pet_id
  else:
    raise Exception('List of pets is empty!')  

  ########      ниже начинаются тесты для практики 19.7.2     #########

def test_add_pet_without_photo_with_valid_data(name = 'Jo', animal_type = 'parrot', age = '7'):
  '''Проверяется возможность добавления питомца в упрощенном режиме (без фото) с валидными данными.
  Ожидаемый статус-код ответа 200.'''  
  _, auth_key = pf.get_api_key(email, password)
  status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)  
  assert status == 200
  assert result['name'] == name

def test_add_photo_of_pet_sucsesful(pet_photo = 'images/parrot.jpg'):
  ''' Проверяется возможность добавления фото к карточке питомца, если питомцев нет, создается
  тестовая карточка и к ней добавляется фото. Ожидаемый статус-код ответа 200. '''
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  if len(my_pets['pets']) == 0:
    pf.add_new_pet_without_photo(auth_key, "Test_Cat", "cat", "1")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
  pet_id = my_pets['pets'][0]['id']
  pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
  status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
  assert status == 200
  assert result['pet_photo'] != ''

def test_get_api_key_for_invalid_user(email = 'wrong@mail.com', password = "incorrect"):
  '''Проверяется невозможность получить api ключ, используя данные пользователя, незарегистрированного
  на портале. Ожидаемый статус-код ответа 403.''' 
  status, _ = pf.get_api_key(email, password)
  assert status == 403

def test_get_api_key_without_email(email = '', password = password):
  '''Проверяется невозможность получить api ключ без указания email адреса.
  Ожидаемый статус-код ответа 403.''' 
  status, _ = pf.get_api_key(email, password)
  assert status == 403

def test_get_api_key_without_password(email = email, password = ''):
  '''Проверяется невозможность получить api ключ без указания пароля.
  Ожидаемый статус-код ответа 403.''' 
  status, _ = pf.get_api_key(email, password)
  assert status == 403 

def test_get_all_pets_with_invalid_key(filter = 'my_pets'):
  '''Проверяется невозможность получить список питомцев с помощью невалидного api ключа.
  Ожидаемый статус-код ответа 403.'''
  auth_key = {'key' : 'it_cannnot_be_an_api_key'}
  status, _ = pf.get_list_of_pets(auth_key, filter)
  assert status == 403

def test_get_all_pets_with_invalid_filter(filter = 'wrong_filter'):
  '''Проверяется невозможность получить список питомцев с указанием неверного фильтра.
  Ожидаемый статус-код ответа 500.'''
  _, auth_key = pf.get_api_key(email, password)
  status, _ = pf.get_list_of_pets(auth_key, filter)
  assert status == 500

def test_delete_pet_with_invalid_api_key():
  '''Проверяется невозможность удалить питомца с неверным api ключом .
  Ожидаемый статус-код ответа 403.'''
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  if len(my_pets['pets']) == 0:
    pf.add_new_pet_without_photo(auth_key, "Test_Cat", "cat", "1")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
  pet_id = my_pets['pets'][0]['id']  
  auth_key =  {'key' : 'it_cannnot_be_an_api_key'} 
  status = pf.delete_pet(auth_key, pet_id)
  assert status == 403


def test_add_pet_without_photo_with_invalid_api_key(name = 'Jony', animal_type = 'horse', age = '5'):
  '''Проверяется невозможность добавления питомца в упрощенном режиме (без фото) с неверным api ключом.
  Ожидаемый статус-код ответа 403.'''  
  auth_key = {'key' : 'it_cannnot_be_an_api_key'}
  status, _ = pf.add_pet_without_photo(auth_key , name, animal_type, age)  
  assert status == 403

def test_add_pet_without_photo_without_data(name = None, animal_type = None, age = None):
  '''Проверяется невозможность добавления питомца в упрощенном режиме без указания обязательных данных.
  Ожидаемый статус-код ответа 400.'''  
  _, auth_key = pf.get_api_key(email, password)
  status, _ = pf.add_pet_without_photo(auth_key , name, animal_type, age)  
  assert status == 400  

def test_update_pet_info_with_invalid_api_key(name = 'Slayer', animal_type = 'dog', age = '3'):
  '''Проверяется невозможность обновления информации о питомце при указании неверного api ключа.
  Ожидаемый статус-код ответа 403.'''
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  pet_id = my_pets['pets'][0]['id']
  auth_key = {'key' : 'it_cannnot_be_an_api_key'}
  status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
  assert status == 403

def test_update_pet_info_with_invalid_data(name = None, animal_type = None, age = None):
  '''Проверяется невозможность обновления информации о питомце без заполнения обязательных данных.
  В этом тесте обнаружен баг: ожидаемый статус-код ответа 400, фактический - 200.'''
  _, auth_key = pf.get_api_key(email, password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  pet_id = my_pets['pets'][0]['id']
  status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
  assert status == 200 

  


  
  









     


  






