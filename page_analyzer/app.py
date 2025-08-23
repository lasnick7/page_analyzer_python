from flask import Flask

app = Flask(__name__)

@app.route('/')
def init_index():
    return "THIS IS MY FIRST HANDLER"
print("TEST APP")