from flask import Flask, request, jsonify, abort, make_response
from datetime import datetime
app = Flask(__name__)
import logging as log

interviews = [
    {
        'id': 1,
        'scheduled_date':datetime(2019, 2, 24),
        'candidate_name': 'Sam Henry',
        'experience': "Managing Director",
        'description': "Role for MD", 
        'completed': False
    },
    {
        'id': 2,
        'scheduled_date':datetime(2019, 2, 25),
        'candidate_name': 'Tom Hank',
        'experience': "Sales Person",
        'description': "Sales executive", 
        'completed': True
    }
]

@app.route('/api/v1.0/interviews', methods=['GET'])
def get_interviews():
    return jsonify({'interview': interviews})


@app.route('/api/v1.0/interviews/<int:interview_id>', methods=['GET'])
def get_interview(interview_id):
    interview = [interview for interview in interviews if interview['id'] == interview_id]
    if len(interview) == 0:
        abort(404)
    return jsonify({'interviews': interview[0]})


@app.route('/api/v1.0/interviews', methods=['POST'])
def schedule_interview():
    if not request.json or not 'candidate_name' in request.json:
        abort(400)
    interview = {
        'id': interviews[-1]['id'] + 1,
        'scheduled_date': "",
        'candidate_name': request.json['candidate_name'],
        'experience': request.json.get('experience', ""),        
        'description': request.json.get('description', ""),
        'done': False
    }
    interviews.append(interview)
    return jsonify({'interview': interview}), 201


@app.route('/api/v1.0/interviews/<int:interview_id>', methods=['DELETE'])
def delete_interview(interview_id):
    interview = [interview for interview in interviews if interview['id'] == interview_id]
    if len(interview) == 0:
        abort(404)
    interviews.remove(interview[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)