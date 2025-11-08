# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from flask import render_template, request, jsonify
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random

db = database()

@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    x = random.choice(['I love playing soccer!',
    'My favorite date is January 13th :D!',
    'I can make tiramisu!',
    'My dreams are often from 1800s',
    'At times, I can feel my spidey-senses, and it’s like my reflexes already know the next move!'])
    return render_template('home.html', fun_fact = x)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/piano')
def piano():
    return render_template('piano.html')

@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    pprint(resume_data)
    return render_template('resume.html', resume_data = resume_data)

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        print("=" * 50)
        print("FEEDBACK ROUTE CALLED")
        
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('comment')  # Form field is 'comment'
        
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        
        # Insert into database - column is 'message' not 'comment'
        query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
        print(f"Query: {query}")
        print(f"Parameters: [{name}, {email}, {message}]")
        
        result = db.query(query, [name, email, message])
        print(f"Query result: {result}")
        
        print("Feedback saved successfully!")
        print("=" * 50)
        
        # Return success JSON
        return jsonify({'success': True, 'message': 'Thank you for your feedback!'})
    except Exception as e:
        print("=" * 50)
        print(f"ERROR in feedback route: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/feedback-list')
def feedback_list():
    try:
        # Get all feedback from database
        query = "SELECT name, message, submitted_at FROM feedback ORDER BY submitted_at DESC"
        feedbacks = db.query(query)
        return render_template('feedback_list.html', feedbacks=feedbacks)
    except Exception as e:
        print(f"Error getting feedback: {e}")
        return render_template('feedback_list.html', feedbacks=[])