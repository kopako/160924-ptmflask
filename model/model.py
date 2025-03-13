import re

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


# Модели:
# Address: Должен содержать следующие поля:
# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.
# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.
class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)

class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @classmethod
    @field_validator("name")
    def validate_name(cls, value):
        if re.findall(r"[^a-zA-Z\s]+$", value):
            raise ValueError("Name must contain only letters")
        return value

    # Валидация:
    # Проверка, что если пользователь указывает, что он занят (is_employed = true),
    # его возраст должен быть от 18 до 65 лет.
    @model_validator(mode='after')
    def validate_age(self):
        if self.is_employed and not(18 < self.age < 65):
            raise ValueError("Employed age must be between 18 and 65")
        return self