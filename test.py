from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "IF YOU SEE THIS, PYTHON IS WORKING!"

if __name__ == '__main__':
    # We use Port 8000 because it is almost NEVER blocked
    app.run(port=8000)