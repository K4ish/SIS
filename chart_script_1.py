
import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Define node positions (x, y coordinates)
positions = {
    'start': (0.5, 1.0),
    'access': (0.5, 0.92),
    'enter': (0.5, 0.84),
    'validate': (0.5, 0.75),
    'error': (0.15, 0.66),
    'session': (0.5, 0.60),
    'update': (0.5, 0.52),
    'redirect': (0.5, 0.44),
    'dashboard': (0.5, 0.35),
    'navigate': (0.5, 0.23),
    'end': (0.5, 0.10)
}

# Node labels
labels = {
    'start': 'Start',
    'access': 'Student accesses<br>login page',
    'enter': 'Enters enrollment<br>number & password',
    'validate': 'System validates<br>credentials',
    'error': 'Show error<br>message',
    'session': 'Create session',
    'update': 'Update last<br>login timestamp',
    'redirect': 'Redirect to<br>dashboard',
    'dashboard': 'Dashboard displays:<br>Profile, Course info<br>Semester, Notifications',
    'navigate': 'Navigate to: Attendance<br>Grades, Internship Credits<br>Fee Details, or Logout',
    'end': 'End'
}

# Add invisible scatter trace for positioning
fig.add_trace(go.Scatter(
    x=[pos[0] for pos in positions.values()],
    y=[pos[1] for pos in positions.values()],
    mode='markers',
    marker=dict(size=0.1, color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip'
))

# Draw arrows/connections
arrows = [
    ('start', 'access'),
    ('access', 'enter'),
    ('enter', 'validate'),
    ('validate', 'error', 'Invalid'),
    ('error', 'access'),
    ('validate', 'session', 'Valid'),
    ('session', 'update'),
    ('update', 'redirect'),
    ('redirect', 'dashboard'),
    ('dashboard', 'navigate'),
    ('navigate', 'end')
]

# Add arrows
for arrow in arrows:
    start_node = arrow[0]
    end_node = arrow[1]
    label = arrow[2] if len(arrow) > 2 else None
    
    x0, y0 = positions[start_node]
    x1, y1 = positions[end_node]
    
    # Special handling for error loop back
    if start_node == 'error' and end_node == 'access':
        fig.add_shape(
            type="path",
            path=f"M {x0},{y0} L {x0},{y0+0.02} L {x1-0.05},{y1-0.02} L {x1-0.05},{y1}",
            line=dict(color="#21808d", width=2),
        )
        fig.add_annotation(
            x=x0-0.05, y=(y0+y1)/2,
            ax=0, ay=0,
            xref="x", yref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#21808d"
        )
    # Special handling for decision branches
    elif label in ['Invalid', 'Valid']:
        if label == 'Invalid':
            mid_x = (x0 + x1) / 2 - 0.05
        else:
            mid_x = (x0 + x1) / 2
        
        fig.add_shape(
            type="line",
            x0=x0, y0=y0-0.03, x1=x1, y1=y1+0.03,
            line=dict(color="#21808d", width=2),
        )
        fig.add_annotation(
            x=x1, y=y1+0.03,
            ax=x0, ay=y0-0.03,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#21808d",
            text=label,
            font=dict(size=10, color="#13343b"),
            bgcolor="#e8f4f5",
            borderpad=2
        )
    else:
        # Regular arrow
        fig.add_annotation(
            x=x1, y=y1+0.03,
            ax=x0, ay=y0-0.03,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#21808d"
        )

# Add nodes with shapes
for node, (x, y) in positions.items():
    if node in ['start', 'end']:
        # Rounded rectangle (terminal)
        fig.add_shape(
            type="rect",
            x0=x-0.08, y0=y-0.025, x1=x+0.08, y1=y+0.025,
            line=dict(color="#21808d", width=2),
            fillcolor="#e8f4f5",
            layer="above"
        )
    elif node == 'validate':
        # Diamond for decision
        fig.add_shape(
            type="path",
            path=f"M {x},{y+0.04} L {x+0.1},{y} L {x},{y-0.04} L {x-0.1},{y} Z",
            line=dict(color="#21808d", width=2),
            fillcolor="#e8f4f5",
            layer="above"
        )
    else:
        # Rectangle for process
        fig.add_shape(
            type="rect",
            x0=x-0.1, y0=y-0.03, x1=x+0.1, y1=y+0.03,
            line=dict(color="#21808d", width=2),
            fillcolor="#e8f4f5",
            layer="above"
        )
    
    # Add text label
    fig.add_annotation(
        x=x, y=y,
        text=labels[node],
        showarrow=False,
        font=dict(size=10, color="#13343b"),
        align="center"
    )

# Update layout
fig.update_layout(
    title="UniHub Student Login & Dashboard Flow",
    showlegend=False,
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.05, 1.05]),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0.05, 1.05]),
    plot_bgcolor='#f3f3ee',
    paper_bgcolor='#f3f3ee'
)

# Save the figure
fig.write_image('unihub_flowchart.png')
fig.write_image('unihub_flowchart.svg', format='svg')

print("Flowchart saved successfully!")
