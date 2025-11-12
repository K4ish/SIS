
# Create Flask structure documentation with proper formatting

flask_doc = """
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


REQUIREMENTS.TXT:
=================
Flask==3.0.0
Flask-MySQLdb==2.0.0
mysqlclient==2.2.0
werkzeug==3.0.0


KEY FLASK ROUTES & FUNCTIONALITY:
==================================

1. LOGIN ROUTE (/login)
   - Validates enrollment number and password
   - Creates session on successful login
   - Hashes passwords using SHA256
   - Updates last login timestamp

2. DASHBOARD ROUTE (/dashboard)
   - Displays student profile information
   - Shows course and semester details
   - Lists recent notifications
   - Requires authentication

3. ATTENDANCE ROUTE (/attendance)
   - Displays subject-wise attendance
   - Calculates attendance percentage
   - Shows attendance trends
   - Requires authentication

4. GRADES ROUTE (/grades)
   - Shows internal and external marks
   - Displays subject-wise grades
   - Calculates current semester GPA
   - Requires authentication

5. INTERNSHIPS ROUTE (/internships)
   - Lists all internship records
   - Shows earned credits
   - Displays verification status
   - Requires authentication

6. FEES ROUTE (/fees)
   - Shows fee structure
   - Displays payment history
   - Calculates balance due
   - Requires authentication

7. LOGOUT ROUTE (/logout)
   - Clears session data
   - Redirects to login page


GPA CALCULATION ALGORITHM:
==========================
Step 1: Retrieve all grades for the student in the specified semester
Step 2: For each subject, get grade_points and credits
Step 3: Calculate weighted sum: sum(grade_points × credits)
Step 4: Calculate total credits: sum(credits)
Step 5: GPA = weighted sum / total credits
Step 6: Round to 2 decimal places

Formula: GPA = Σ(grade_points × credits) / Σ(credits)

Example:
Subject 1: Grade Points = 9.0, Credits = 4  → 9.0 × 4 = 36
Subject 2: Grade Points = 8.5, Credits = 3  → 8.5 × 3 = 25.5
Subject 3: Grade Points = 9.5, Credits = 4  → 9.5 × 4 = 38
Total: 99.5 / 11 = 9.05 GPA


ATTENDANCE CALCULATION:
=======================
Step 1: Count total classes for student in subject
Step 2: Count classes marked as 'Present'
Step 3: Percentage = (Present / Total) × 100
Step 4: Round to 2 decimal places


SECURITY BEST PRACTICES:
========================
1. Password Hashing: Use SHA256 for password storage
2. Session Management: Use Flask's secure session with secret key
3. SQL Injection Prevention: Use parameterized queries
4. CSRF Protection: Implement Flask-WTF for form protection
5. Input Validation: Validate all user inputs
6. File Upload Security: Use secure_filename() for uploads
7. Authentication Required: Check session before accessing routes
8. Secure Cookies: Set HttpOnly and Secure flags
9. Database Connection: Use connection pooling
10. Error Handling: Never expose sensitive error details


CSS DESIGN GUIDELINES:
======================
Color Palette (White & Classic Theme):
- Background: #FFFFFF (Pure White)
- Text Primary: #333333 (Dark Grey)
- Text Secondary: #666666 (Medium Grey)
- Accent: #E0E0E0 (Light Grey)
- Hover: #4A90E2 (Light Blue)
- Border: #DDDDDD (Very Light Grey)

Typography:
- Font Family: 'Poppins' or 'Open Sans'
- Heading: 24-32px, font-weight: 600
- Body: 14-16px, font-weight: 400
- Small: 12px, font-weight: 400

Card Design:
- Background: #FFFFFF
- Border: 1px solid #DDDDDD
- Border Radius: 8px
- Box Shadow: 0 2px 4px rgba(0,0,0,0.08)
- Padding: 20px
- Margin: 16px 0

Sidebar:
- Width: 250px
- Background: #F8F9FA
- Border-right: 1px solid #DDDDDD
- Active Item: Light blue background (#E3F2FD)
- Hover: #F0F0F0


MYSQL DATABASE SETUP:
=====================
CREATE DATABASE unihub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE unihub;

-- Run all table creation scripts from unihub_database_schema.txt

-- Create indexes for performance
CREATE INDEX idx_student_enrollment ON students(enrollment_number);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_grades_student_semester ON grades(student_id, semester);
CREATE INDEX idx_user_email ON users(email);


DEPLOYMENT CHECKLIST:
=====================
1. Set strong SECRET_KEY in production
2. Use environment variables for database credentials
3. Enable HTTPS/SSL
4. Set DEBUG=False
5. Configure proper logging
6. Set up database backups
7. Configure file upload limits
8. Set up CORS if needed
9. Enable rate limiting
10. Configure firewall rules
11. Set up monitoring and alerts
12. Regular security updates
"""

print(flask_doc)

# Save to file
with open('unihub_flask_documentation.txt', 'w') as f:
    f.write(flask_doc)

print("\n\n✓ Flask documentation saved to 'unihub_flask_documentation.txt'")
