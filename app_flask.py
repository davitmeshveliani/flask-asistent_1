from flask import Flask
app = Flask(__name__)


#1): @app.route("/") — добавлен слэш для корректного указания корневого маршрута.#


@app.route('/')
def home():
    return 'Hello, davit!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)