from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/quiz')
def get_quiz():
    # Simple keys: 'q' and 'a'
    return jsonify({
        "q": "What is the chemical symbol for Water?",
        "a": "H2O",
        "b": "CO2"
    })

if __name__ == '__main__':
    # Using Port 8000 because we know it works!
    app.run(debug=True, port=8000)