from flask import Flask, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError,Field

app = Flask(__name__)
@app.get("/")
async def root():
    return {"message": "Welcome to my API! Go to /docs to see the documentation."}

# შენი მოდელები Pydantic-ით რჩება
class Address(BaseModel):
    city: str
    street: str
    house_number: int

class User(BaseModel):
    name: str
    age: int = Field(strict=True)
    email: EmailStr
    is_employed: bool
    address: Address

@app.route('/register/', methods=['POST'])
def register_user():
    data = request.json
    try:
        user = User(**data)
        # ვალიდაციის ლოგიკა
        if user.is_employed and not (18 <= user.age <= 65):
            return jsonify({"error": "Wiek musi wynosić od 18 do 65 lat."}), 400
        return jsonify({"message": "User registered successfully", "data": user.model_dump()})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

if __name__ == "__main__":
    app.run(debug=True)