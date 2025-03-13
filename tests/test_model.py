import pytest
from pydantic import ValidationError

from model.model import User


def test_valid_user():
    valid_user_json = """{
        "name": "John Doe",
        "age": 60,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    user = User.model_validate_json(valid_user_json)
    assert user.name == "John Doe"
    assert user.age == 60
    assert user.email == "john.doe@example.com"
    assert user.is_employed is True

def test_invalid_user():
    invalid_user_json = """{
        "name": "John Doe",
        "age": 70,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "N",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    with pytest.raises(ValidationError):
        User.model_validate_json(invalid_user_json)

def test_user_name_letters_only():
    invalid_user_json = """{
        "name": "John 1234",
        "age": 70,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "Nasdf",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    with pytest.raises(ValueError):
        User.model_validate_json(invalid_user_json)


    # Валидация:
    # Проверка, что если пользователь указывает, что он занят (is_employed = true),
    # его возраст должен быть от 18 до 65 лет.
def test_work_eligible():
    to_young = """{
        "name": "John Doe",
        "age": 17,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    with pytest.raises(Exception):
        User.model_validate_json(to_young)
