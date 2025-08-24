import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def init_index():
    return "THIS IS MY FIRST HANDLER"
print("TEST APP")