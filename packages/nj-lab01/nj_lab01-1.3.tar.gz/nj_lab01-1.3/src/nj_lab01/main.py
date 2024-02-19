from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def say_hello_class():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'Hello, Class CYB 600! Current Time: {current_time}'

if __name__ == '__main__':
    app.run(debug=True, port=8080)