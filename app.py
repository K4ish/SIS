
# Create a sample Flask application structure document for UniHub

flask_structure = """
UNIHUB FLASK APPLICATION STRUCTURE
====================================

PROJECT DIRECTORY STRUCTURE:
----------------------------
UniHub/
│
├── app.py                      # Main Flask application file
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── static/                     # Static files (CSS, JS, Images)
│   ├── css/
│   │   ├── style.css          # Main stylesheet
│   │   └── dashboard.css      # Dashboard-specific styles
│   ├── js/
│   │   ├── main.js            # Main JavaScript file
│   │   └── dashboard.js       # Dashboard functionality
│   └── images/
│       ├── logo.png
│       └── default-avatar.png
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── dashboard.html         # Student dashboard
│   ├── attendance.html        # Attendance view
│   ├── grades.html            # Grades view
│   ├── internships.html       # Internship credits view
│   ├── fees.html              # Fee details view
│   └── admin/                 # Admin templates
│       ├── admin_dashboard.html
│       └── manage_students.html
│
└── uploads/                    # User uploaded files
    ├── profile_photos/
    └── certificates/

MAIN APPLICATION FILE (app.py):
================================
"""

flask_code = '''
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your-password'
app.config['MYSQL_DB'] = 'unihub'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize MySQL
mysql = MySQL(app)

# Helper Functions
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_attendance_percentage(student_id, subject_id):
    """Calculate attendance percentage for a student in a subject"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Total classes
    cursor.execute('''
        SELECT COUNT(*) as total 
        FROM attendance 
        WHERE student_id = %s AND subject_id = %s
    ''', (student_id, subject_id))
    total = cursor.fetchone()['total']
    
    # Present classes
    cursor.execute('''
        SELECT COUNT(*) as present 
        FROM attendance 
        WHERE student_id = %s AND subject_id = %s AND status = 'Present'
    ''', (student_id, subject_id))
    present = cursor.fetchone()['present']
    
    return (present / total * 100) if total > 0 else 0

def calculate_gpa(student_id, semester):
    """Calculate GPA for a student in a specific semester"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('''
        SELECT g.grade_points, s.credits 
        FROM grades g
        JOIN subjects s ON g.subject_id = s.subject_id
        WHERE g.student_id = %s AND g.semester = %s
    ''', (student_id, semester))
    
    records = cursor.fetchall()
    
    if not records:
        return 0.0
    
    total_grade_points = sum(r['grade_points'] * r['credits'] for r in records)
    total_credits = sum(r['credits'] for r in records)
    
    return round(total_grade_points / total_credits, 2) if total_credits > 0 else 0.0

# Routes

@app.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle student login"""
    msg = ''
    
    if request.method == 'POST' and 'enrollment_number' in request.form and 'password' in request.form:
        enrollment_number = request.form['enrollment_number']
        password = request.form['password']
        password_hash = hash_password(password)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT s.*, u.user_id, u.email, c.course_name 
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.enrollment_number = %s AND u.password_hash = %s AND u.is_active = TRUE
        ''', (enrollment_number, password_hash))
        
        student = cursor.fetchone()
        
        if student:
            # Create session
            session['loggedin'] = True
            session['user_id'] = student['user_id']
            session['student_id'] = student['student_id']
            session['enrollment_number'] = student['enrollment_number']
            session['name'] = f"{student['first_name']} {student['last_name']}"
            
            # Update last login
            cursor.execute('UPDATE users SET last_login = NOW() WHERE user_id = %s', 
                         (student['user_id'],))
            mysql.connection.commit()
            
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect enrollment number or password!'
    
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    """Student dashboard"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get student details
    cursor.execute('''
        SELECT s.*, c.course_name, c.course_code 
        FROM students s
        JOIN courses c ON s.course_id = c.course_id
        WHERE s.student_id = %s
    ''', (session['student_id'],))
    student = cursor.fetchone()
    
    # Get recent notifications
    cursor.execute('''
        SELECT title, content, created_at 
        FROM admin_notifications 
        WHERE is_active = TRUE AND target_audience IN ('All', 'Students')
        ORDER BY created_at DESC LIMIT 5
    ''')
    notifications = cursor.fetchall()
    
    return render_template('dashboard.html', student=student, notifications=notifications)

@app.route('/attendance')
def attendance():
    """View attendance records"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get subjects with attendance percentage
    cursor.execute('''
        SELECT DISTINCT s.subject_id, s.subject_name, s.subject_code 
        FROM subjects s
        JOIN attendance a ON s.subject_id = a.subject_id
        WHERE a.student_id = %s
    ''', (session['student_id'],))
    subjects = cursor.fetchall()
    
    # Calculate attendance percentage for each subject
    for subject in subjects:
        subject['percentage'] = calculate_attendance_percentage(
            session['student_id'], 
            subject['subject_id']
        )
    
    return render_template('attendance.html', subjects=subjects)

@app.route('/grades')
def grades():
    """View grades and GPA"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get current semester
    cursor.execute('SELECT semester FROM students WHERE student_id = %s', 
                  (session['student_id'],))
    current_semester = cursor.fetchone()['semester']
    
    # Get grades for current semester
    cursor.execute('''
        SELECT g.*, s.subject_name, s.subject_code, s.credits 
        FROM grades g
        JOIN subjects s ON g.subject_id = s.subject_id
        WHERE g.student_id = %s AND g.semester = %s
    ''', (session['student_id'], current_semester))
    grades = cursor.fetchall()
    
    # Calculate GPA
    gpa = calculate_gpa(session['student_id'], current_semester)
    
    return render_template('grades.html', grades=grades, gpa=gpa, semester=current_semester)

@app.route('/internships')
def internships():
    """View internship credits"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('''
        SELECT * FROM internships 
        WHERE student_id = %s 
        ORDER BY start_date DESC
    ''', (session['student_id'],))
    internship_records = cursor.fetchall()
    
    # Calculate total credits
    total_credits = sum(i['credits_earned'] for i in internship_records)
    
    return render_template('internships.html', 
                         internships=internship_records, 
                         total_credits=total_credits)

@app.route('/fees')
def fees():
    """View fee details"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get fee structure
    cursor.execute('''
        SELECT fs.* 
        FROM fee_structure fs
        JOIN students s ON fs.course_id = s.course_id
        WHERE s.student_id = %s AND fs.semester = s.semester
    ''', (session['student_id'],))
    fee_structure = cursor.fetchone()
    
    # Get payment history
    cursor.execute('''
        SELECT * FROM fee_payments 
        WHERE student_id = %s 
        ORDER BY payment_date DESC
    ''', (session['student_id'],))
    payments = cursor.fetchall()
    
    # Calculate balance
    total_paid = sum(p['amount_paid'] for p in payments)
    balance = fee_structure['total_fee'] - total_paid if fee_structure else 0
    
    return render_template('fees.html', 
                         fee_structure=fee_structure, 
                         payments=payments, 
                         balance=balance)

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('student_id', None)
    session.pop('enrollment_number', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
'''

full_doc = flask_structure + flask_code

print(full_doc)

# Save to file
with open('unihub_flask_structure.txt', 'w') as f:
    f.write(full_doc)

print("\n\n✓ Flask application structure saved to 'unihub_flask_structure.txt'")
