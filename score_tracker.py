from flask import Flask, render_template, redirect, flash, session, request, jsonify
import json
import math
import requests

app = Flask(__name__)
app.secret_key = 'this-should-be-something-unguessable'

# ---------- Define classes for data types ---------- #
tests = {}
class Test:
    def __init__(self, number):
        self.number = number
        self.scores = {}
        self.score_average = 0
        
    def add_student_score(self, id, score):
        self.scores[id] = score
        tests = 0
        cummulative = 0
        for id in self.scores:
          cummulative += self.scores[id]
          tests += 1
        new_average = cummulative/tests
        self.score_average = new_average
students = {}
class Student:
    def __init__(self, id):
        self.id = id
        self.scores = {}
        self.score_average = 0
        
    def add_test_score(self, number, score):
        self.scores[number] = score
        tests = 0
        cummulative = 0
        for id in self.scores:
          cummulative += self.scores[id]
          tests += 1
        new_average = cummulative/tests
        self.score_average = new_average

def update_stored(data):
    """Update stored student and test score data given data from external scores API"""
    
    student_id = data['studentId']
    test_id = data['exam']
    score = data['score']
    
    stored_student = students.get(student_id, None)
    if stored_student:
        stored_student.add_test_score(test_id, score)
    else:
        new_student = Student(student_id)
        new_student.add_test_score(test_id, score)
        students[student_id] = new_student
      
    stored_test = tests.get(test_id, None)
    if stored_test:
        stored_test.add_student_score(student_id, score)
    else:
        new_test = Test(test_id)
        new_test.add_student_score(student_id, score)
        tests[test_id] = new_test
        
    
# ---------- Set up processing of data ---------- #
session = requests.Session()
clean_data = []

def streaming(): # set up data generation
    request = requests.Request("GET",' http://live-test-scores.herokuapp.com/scores').prepare()
    response = session.send(request, stream=True) # continuously accepts data

    for line in response.iter_lines():
        if line:
            yield line # allows continued interation on incoming data

def read_stream():
    for line in streaming():
        if line.decode("utf-8").startswith('data:'):
            line_data = line.decode("utf-8")[6:]
            data = json.loads(line_data)
            update_stored(data)

# read_stream() 

# ---------- Define Routes ---------- #
@app.route("/", methods=['GET'])
def define_accessible_routes():
    """A route that shows a user where and how to access data"""
    return """Accessible routes are: 1) /students 2) /students/{id} 3) /exams 4) /exams/{id}"""
        
@app.route("/students", methods=['GET'])
def get_students():
    """A route that returns a list of student objects with at least one score present"""
    stored_students = json.dumps(students)
    return students

@app.route("/students/{id}", methods=['GET'])
def get_student_scores(id):
    """A route that returns the tests (with scores) and the test average for the given student id"""
    student = students.get(id, None)
    if student:
        return json.dumps(student.__dict__)

@app.route("/exams", methods=['GET'])
def get_exams():
    """A route that returns a list of score objects that are recorded"""
    stored_exams = json.dumps(tests)
    return stored_exams

@app.route("/exams/{number}", methods=['GET'])
def get_exam_scores(number):
    """A route that returns the student scores and the test average for a given test number"""
    exam = tests.get(number, None)
    if exam:
        return json.dumps(exam.__dict__)
    
# ---------- Error Handling for 404 Errors ---------- #
@app.errorhandler(404)
def redirect_to_root(e):
    """If the user tries to access a route that is not above, they are redirected to root which displays information about the score_tracker API"""
    return redirect('/')


# ---------- Flask App Bits ---------- #
if __name__ == "__main__":
    app.debug = True 
    
    app.run(port=6000, host='127.0.0.1')
    app.run()
    read_stream()
