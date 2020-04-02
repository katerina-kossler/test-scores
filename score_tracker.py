from flask import Flask, render_template, redirect, flash, session, request, jsonify
import json

app = Flask(__name__)
app.secret_key = 'this-should-be-something-unguessable'


@app.route("/", methods=['GET'])
def define_accessible_routes():
    """A route that shows a user where and how to access data"""
    pass
        
@app.route("/students", methods=['GET'])
def get_students():
    """A route that returns a list of student objects with at least one score present"""
    pass

@app.route("/students/{id}", methods=['GET'])
def get_student_scores(id):
    """A route that returns the test's (with scores) and the test average for the given student id"""
    pass

@app.route("/exams", methods=['GET'])
def get_exams():
    """A route that returns a list of score objects that are recorded"""
    pass

@app.route("/exams/{id}", methods=['GET'])
def get_student_scores(number):
    """A route that returns """
    pass
    
# ---------- Error Handling for 404 Errors ---------- #
@app.errorhandler(404)
def redirect_to_root(e):
    """If the user tries to access a route that is not above, they are redirected to root which displays information about the score_tracker API"""
    return redirect('/')


# ---------- Flask App Bits ---------- #
if __name__ == "__main__":
    app.debug = True 
    
    connect_to_db(app)
    
    app.run(port=5000, host='0.0.0.0')
    app.run()
