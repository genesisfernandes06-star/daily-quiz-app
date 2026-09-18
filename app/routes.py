from flask import Blueprint, jsonify, request
from .models import Question
from sqlalchemy.sql.expression import func

main = Blueprint('main', __name__)

@main.route('/quiz', methods=['GET'])
def get_quiz():
    requested_topic = request.args.get('topic', 'GK') 
    
    questions = Question.query.filter_by(topic=requested_topic).order_by(func.random()).limit(5).all()
    
    quiz_data = []
    for q in questions:
        quiz_data.append({
            "id": q.question_id,
            "question": q.question_text,
            "options": {
                "A": q.option_a,
                "B": q.option_b,
                "C": q.option_c,
                "D": q.option_d
            }
        })
        
    return jsonify(quiz_data)