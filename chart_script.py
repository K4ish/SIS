
import plotly.graph_objects as go
import numpy as np

# Create figure
fig = go.Figure()

# Define entity positions (x, y) - arranged in a logical layout
entities = {
    'users': {'pos': (1, 8), 'fields': ['user_id PK', 'username', 'email', 'password_hash', 'user_type']},
    'students': {'pos': (1, 5), 'fields': ['student_id PK', 'user_id FK', 'enrollment_num', 'first_name', 'last_name', 'course_id FK', 'semester']},
    'courses': {'pos': (4, 6), 'fields': ['course_id PK', 'course_code', 'course_name', 'department']},
    'subjects': {'pos': (4, 3), 'fields': ['subject_id PK', 'subject_code', 'subject_name', 'course_id FK', 'semester', 'credits']},
    'attendance': {'pos': (7, 4), 'fields': ['attendance_id PK', 'student_id FK', 'subject_id FK', 'attend_date', 'status']},
    'grades': {'pos': (7, 1), 'fields': ['grade_id PK', 'student_id FK', 'subject_id FK', 'internal_marks', 'external_marks', 'grade_points']},
    'internships': {'pos': (1, 2), 'fields': ['internship_id PK', 'student_id FK', 'company_name', 'credits_earned']},
    'fee_payments': {'pos': (1, 0), 'fields': ['payment_id PK', 'student_id FK', 'amount_paid', 'payment_date']}
}

# Define relationships with line types
relationships = [
    ('users', 'students', '1:1'),
    ('courses', 'students', '1:N'),
    ('courses', 'subjects', '1:N'),
    ('students', 'attendance', '1:N'),
    ('subjects', 'attendance', '1:N'),
    ('students', 'grades', '1:N'),
    ('subjects', 'grades', '1:N'),
    ('students', 'internships', '1:N'),
    ('students', 'fee_payments', '1:N')
]

# Draw relationship lines
for entity1, entity2, rel_type in relationships:
    x1, y1 = entities[entity1]['pos']
    x2, y2 = entities[entity2]['pos']
    
    fig.add_trace(go.Scatter(
        x=[x1, x2],
        y=[y1, y2],
        mode='lines',
        line=dict(color='#21808d', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

# Draw entity boxes with fields
for entity_name, entity_data in entities.items():
    x, y = entity_data['pos']
    fields = entity_data['fields']
    
    # Create field text
    field_text = '<br>'.join(fields)
    
    # Add entity box (represented as a scatter point with large marker)
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode='markers+text',
        marker=dict(size=80, color='#B3E5EC', line=dict(color='#21808d', width=2)),
        text=entity_name.upper(),
        textposition='top center',
        textfont=dict(size=11, color='#13343b', family='Arial Black'),
        showlegend=False,
        hovertext=f"<b>{entity_name}</b><br>{field_text}",
        hoverinfo='text'
    ))

# Update layout
fig.update_layout(
    title='UniHub Database ERD',
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 8.5]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 9]),
    plot_bgcolor='#F3F3EE',
    paper_bgcolor='#F3F3EE'
)

# Save the figure
fig.write_image('unihub_erd.png')
fig.write_image('unihub_erd.svg', format='svg')

print("ERD diagram created successfully")
