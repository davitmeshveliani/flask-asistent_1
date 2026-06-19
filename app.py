from flask import Flask, request, jsonify
from pydantic import ValidationError
from models import User

app = Flask(__name__)

@app.route('/register/', methods=['POST'])
def register_user():
    data = request.json
    try:
        user = User.model_validate(data)
        return jsonify({"message": "User registered successfully", "data": user.model_dump()}), 200
    except ValidationError as e:
        errors = e.errors()
        readable_errors = []
        for error in errors:readable_errors.append({
                "loc": error["loc"],
                "msg": str(error["msg"]) })
        return jsonify({"errors": readable_errors}), 422


if __name__ == "__main__":
    app.run(debug=True)