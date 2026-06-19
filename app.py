from pydantic import BaseModel, EmailStr, ValidationError, model_validator,Field

class Address(BaseModel):
    city: str
    street: str
    house_number: int

class User(BaseModel):
    name: str = Field(...,min_length=2, max_length=10)
    age: int = Field(strict=True)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def check_employment_age(self) -> 'User':
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError('Если пользователь занят, возраст должен быть от 18 до 65 лет.')
        return self

def process_user_registration(user_dict: dict) -> str:
    try:
        user = User.model_validate(user_dict)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return f"Ошибка валидации: {e.errors()[0]['msg']}"

if __name__ == "__main__":

    test_cases = [
        {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com",
            "is_employed": True,
            "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}
        },
        {
            "name": "John Doe",
            "age": 70,
            "email": "john@example.com",
            "is_employed": True,
            "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}
        },
        {
            "name": "Ivan",
            "age": 25,
            "email": "bad-email",
            "is_employed": False,
            "address": {"city": "Moscow", "street": "Arbat", "house_number": 1}
        }
    ]

    for i, data in enumerate(test_cases, 1):
        print(f"--- Тест {i} ---")
        print(process_user_registration(data))
        print()