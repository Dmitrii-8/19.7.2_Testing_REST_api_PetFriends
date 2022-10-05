from app import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что:
    1. Код статуса запроса 200.
    2. В переменной result содержится слово key'''
    status, result = pf.get_app_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем, что код статуса запроса 200 и что список всех питомцев не пустой.
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной api_key,
    затем применяем метод get_list_of_pets() проверяя статус ответа и что список питомцев не пуст'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pets_with_valid_data(name='Fart', animal_type='cat', age='3', pet_photo='images/Fart.jpg'):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой.
    Для этого в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ
    в переменную api_key, проверяем статус ответа и то что ответ содержит добавленные данные.
     '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Mars', 'cat', '4', 'images/Fart.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info(name='из', animal_type='измененный', age='5'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pets_with_valid_data_without_photo(name='MarsБезФото', animal_type='кот', age='7'):
    '''Проверяем возможность добавления нового питомца, без фото'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_at_pet(pet_photo='images/Graf.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pet_negative_age_number(name='Fart', animal_type='cat', age='-3', pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден, если питомец будет добавлен на сайт с отрицательным числом в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'


def test_add_pet_with_four_digit_age_number(name='Fart', animal_type='cat', age='9876', pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
    Тест пройден не будет, если питомец будет добавлен на сайт, с числом превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом превышающим 3 знака в поле возраст'


def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='3', pet_photo='images/Fart.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец, с пустым значением в имени, добавлен на сайт '


def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='cat', age='5', pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием.
    Добавление питомца имя которого превышает 10 слов.
    Тест не будет пройден если питомец будет добавлен на сайт с именем состоящим из более 10 слов'''

    name = 'Don Huan Pablo de la Rusa Franchesko Ivanetti Graf Sebastiyan Yan Agilletti Septim Mikola Fa Lesso'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count < 10, 'Питомец, с именем больше 10 слов - добавлен. '


def test_add_pet_with_special_characters_in_variable_animal_type(name='Fart', age='3', pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с использованием специальных символов вместо букв,
    в переменной animal_type.
    Тест пройден не будет, если питомец будет добавлен на сайт, с использованием спец.символов
    вместо букв, в поле порода.'''
    animal_type = 'Cat%@'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Питомец, с недопустимыми спец.символами - добавлен '


def test_add_pet_with_numbers_in_variable_animal_type(name='Fart', animal_type='87543', age='3',
                                                      pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест пройден не будет, если питомец будет добавлен на сайт, с цифрами вместо букв, в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец на сайт добавлен, с цифрами вместо букв в поле порода.'

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с валидным емейл и с невалидным паролем.
    Проверяем - нет ли ключа в ответе.'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с валидным емейл и с невалидным паролем.
    Проверяем - нет ли ключа в ответе'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Fart', age='2', pet_photo='images/Fart.jpg'):
    '''Проверка с негативным сценарием.
    Добавление питомца название породы которого превышает 10 слов.
    Тест пройден не будет, в том случае, если питомец будет добавлен на сайт
    с названием породы состоящим, из более чем 10-ти слов'''

    animal_type = 'рандомный набор пород домашний дикий британец сиамский рэдгдолл бурма мэнкс гавана ликой'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 10, 'Питомец с названием породы больше 10 слов - добавлен. '

