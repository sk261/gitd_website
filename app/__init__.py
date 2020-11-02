from flask import Flask
app = Flask(__name__)
from app import routes

app.secret_key = b'\xeb2\xb6?\xbd\xc7^HZG\xfcJ#\x1f\xbf\xe1O\x9c\xd0\xd6.\xb1\xd8|K\x08\xa9c\xa0\x10'
