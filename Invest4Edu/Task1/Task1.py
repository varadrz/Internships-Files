import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


#Mentioning all the work done accordingly in comments starting with '#'


# Step 1: Read the data from the Excel file
try:
    df = pd.read_excel('P:\\Internships\\Invest4Edu\\student_scores.xlsx')
    print("Excel file loaded successfully!")
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Step 2: Group data by Student ID and Name, calculate total and average scores
student_group = df.groupby(['Student ID', 'Name']).agg(
    total_score=('Subject Score', 'sum'),
    average_score=('Subject Score', 'mean')
).reset_index()

# Step 3: Generate PDF report cards
def generate_report_card(student_data, filename):
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Header data
    data = [
        ["Student Name", student_data['Name']],
        ["Student ID", student_data['Student ID']],
        ["Total Score", student_data['total_score']],
        ["Average Score", f"{student_data['average_score']:.2f}"],
    ]

    # Subject-wise scores
    subject_scores = [["Subject", "Score"]]
    subject_scores += student_data['subject_scores']

    # Create the table for the header
    table = Table(data + [["", ""]])  
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(table)

    # Create a table for subject-wise scores
    subject_table = Table(subject_scores)
    subject_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    elements.append(subject_table)

    
    pdf.build(elements)

# Step 4: Loop through the student data and generate PDF for each student
for index, row in student_group.iterrows():
    # Extract subject-wise scores for the student
    subject_scores = df[df['Student ID'] == row['Student ID']][['Subject', 'Subject Score']].values.tolist()
    
    # Prepare student data for the report
    student_data = {
        'Name': row['Name'],
        'Student ID': row['Student ID'],
        'total_score': row['total_score'],
        'average_score': row['average_score'],
        'subject_scores': subject_scores
    }

    # Generate the report card PDF and save it
    filename = f"report_card_{row['Student ID']}.pdf"
    generate_report_card(student_data, filename)

    print(f"Report card generated for {row['Name']}")

