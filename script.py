
# Create a comprehensive database schema design for UniHub system
# This will document the tables, relationships, and attributes needed

schema_design = """
DATABASE SCHEMA DESIGN FOR UNIHUB - UNIVERSITY STUDENT INFORMATION PORTAL
==========================================================================

1. USERS TABLE (users)
   - user_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - username (VARCHAR(50), UNIQUE, NOT NULL)
   - email (VARCHAR(100), UNIQUE, NOT NULL)
   - password_hash (VARCHAR(255), NOT NULL)
   - user_type (ENUM('student', 'faculty', 'admin'), NOT NULL)
   - is_active (BOOLEAN, DEFAULT TRUE)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - last_login (TIMESTAMP, NULL)

2. STUDENTS TABLE (students)
   - student_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - user_id (INT, FOREIGN KEY -> users.user_id, UNIQUE)
   - enrollment_number (VARCHAR(20), UNIQUE, NOT NULL)
   - first_name (VARCHAR(50), NOT NULL)
   - last_name (VARCHAR(50), NOT NULL)
   - profile_photo (VARCHAR(255), NULL)
   - date_of_birth (DATE, NOT NULL)
   - gender (ENUM('Male', 'Female', 'Other'), NOT NULL)
   - phone (VARCHAR(15), NULL)
   - address (TEXT, NULL)
   - course_id (INT, FOREIGN KEY -> courses.course_id)
   - semester (INT, NOT NULL)
   - admission_date (DATE, NOT NULL)
   - status (ENUM('Active', 'Inactive', 'Graduated'), DEFAULT 'Active')

3. COURSES TABLE (courses)
   - course_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - course_code (VARCHAR(20), UNIQUE, NOT NULL)
   - course_name (VARCHAR(100), NOT NULL)
   - department (VARCHAR(100), NOT NULL)
   - duration_years (INT, NOT NULL)
   - total_semesters (INT, NOT NULL)
   - description (TEXT, NULL)

4. SUBJECTS TABLE (subjects)
   - subject_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - subject_code (VARCHAR(20), UNIQUE, NOT NULL)
   - subject_name (VARCHAR(100), NOT NULL)
   - course_id (INT, FOREIGN KEY -> courses.course_id)
   - semester (INT, NOT NULL)
   - credits (INT, NOT NULL)
   - max_marks_internal (INT, DEFAULT 30)
   - max_marks_external (INT, DEFAULT 70)
   - description (TEXT, NULL)

5. ATTENDANCE TABLE (attendance)
   - attendance_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - student_id (INT, FOREIGN KEY -> students.student_id)
   - subject_id (INT, FOREIGN KEY -> subjects.subject_id)
   - attendance_date (DATE, NOT NULL)
   - status (ENUM('Present', 'Absent', 'Late'), NOT NULL)
   - marked_by (INT, FOREIGN KEY -> users.user_id)
   - remarks (TEXT, NULL)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - UNIQUE KEY (student_id, subject_id, attendance_date)

6. GRADES TABLE (grades)
   - grade_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - student_id (INT, FOREIGN KEY -> students.student_id)
   - subject_id (INT, FOREIGN KEY -> subjects.subject_id)
   - internal_marks (DECIMAL(5,2), NULL)
   - external_marks (DECIMAL(5,2), NULL)
   - total_marks (DECIMAL(5,2), NULL)
   - grade (VARCHAR(2), NULL)
   - grade_points (DECIMAL(3,2), NULL)
   - semester (INT, NOT NULL)
   - academic_year (VARCHAR(10), NOT NULL)
   - status (ENUM('Pass', 'Fail', 'Pending'), NULL)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - UNIQUE KEY (student_id, subject_id, semester, academic_year)

7. INTERNSHIPS TABLE (internships)
   - internship_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - student_id (INT, FOREIGN KEY -> students.student_id)
   - company_name (VARCHAR(100), NOT NULL)
   - position (VARCHAR(100), NOT NULL)
   - start_date (DATE, NOT NULL)
   - end_date (DATE, NOT NULL)
   - duration_months (INT, NOT NULL)
   - description (TEXT, NULL)
   - credits_earned (INT, DEFAULT 0)
   - certificate_path (VARCHAR(255), NULL)
   - status (ENUM('Ongoing', 'Completed', 'Verified'), DEFAULT 'Ongoing')
   - verified_by (INT, FOREIGN KEY -> users.user_id, NULL)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

8. FEE_STRUCTURE TABLE (fee_structure)
   - fee_structure_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - course_id (INT, FOREIGN KEY -> courses.course_id)
   - semester (INT, NOT NULL)
   - tuition_fee (DECIMAL(10,2), NOT NULL)
   - library_fee (DECIMAL(10,2), DEFAULT 0)
   - lab_fee (DECIMAL(10,2), DEFAULT 0)
   - other_fee (DECIMAL(10,2), DEFAULT 0)
   - total_fee (DECIMAL(10,2), NOT NULL)
   - academic_year (VARCHAR(10), NOT NULL)
   - UNIQUE KEY (course_id, semester, academic_year)

9. FEE_PAYMENTS TABLE (fee_payments)
   - payment_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - student_id (INT, FOREIGN KEY -> students.student_id)
   - fee_structure_id (INT, FOREIGN KEY -> fee_structure.fee_structure_id)
   - amount_paid (DECIMAL(10,2), NOT NULL)
   - payment_date (DATE, NOT NULL)
   - payment_method (ENUM('Cash', 'Card', 'Online', 'Cheque'), NOT NULL)
   - transaction_id (VARCHAR(100), UNIQUE, NULL)
   - receipt_number (VARCHAR(50), UNIQUE, NOT NULL)
   - status (ENUM('Pending', 'Completed', 'Failed'), DEFAULT 'Completed')
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

10. ADMIN_NOTIFICATIONS TABLE (admin_notifications)
    - notification_id (INT, PRIMARY KEY, AUTO_INCREMENT)
    - title (VARCHAR(200), NOT NULL)
    - content (TEXT, NOT NULL)
    - type (ENUM('Circular', 'Announcement', 'Alert'), NOT NULL)
    - target_audience (ENUM('All', 'Students', 'Faculty'), DEFAULT 'All')
    - attachment_path (VARCHAR(255), NULL)
    - created_by (INT, FOREIGN KEY -> users.user_id)
    - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    - is_active (BOOLEAN, DEFAULT TRUE)

KEY RELATIONSHIPS:
==================
1. users -> students (One-to-One)
2. courses -> students (One-to-Many)
3. courses -> subjects (One-to-Many)
4. students -> attendance (One-to-Many)
5. subjects -> attendance (One-to-Many)
6. students -> grades (One-to-Many)
7. subjects -> grades (One-to-Many)
8. students -> internships (One-to-Many)
9. courses -> fee_structure (One-to-Many)
10. students -> fee_payments (One-to-Many)
11. fee_structure -> fee_payments (One-to-Many)

INDEXES FOR PERFORMANCE:
========================
- Index on students.enrollment_number
- Index on attendance.attendance_date
- Index on grades.student_id, grades.semester
- Index on fee_payments.student_id, fee_payments.payment_date
- Index on users.email
- Composite index on (subject_id, semester) in subjects table
"""

print(schema_design)

# Save to file
with open('unihub_database_schema.txt', 'w') as f:
    f.write(schema_design)

print("\n\n✓ Schema design saved to 'unihub_database_schema.txt'")
