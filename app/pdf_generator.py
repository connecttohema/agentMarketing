from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
import os

def generate_pdf(customer, letter_content):
    pdf_file_name = f"{customer['CustomerId']}_marketing_letter.pdf"
    c = canvas.Canvas(pdf_file_name, pagesize=letter)
    width, height = letter

    # Add company logo
    logo_path = os.path.join(os.getcwd(), 'static', 'statefarm-logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 1*inch, height - 1*inch, width=2*inch, preserveAspectRatio=True)

    # Add company address below the logo
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 1.5*inch, "State Farm Insurance: Corporate Headquarters")
    c.drawString(1*inch, height - 1.75*inch, "1 State Farm Plaza, Bloomington, IL")

    # Add customer details and letter content
    c.setFont("Helvetica", 12)
    text = c.beginText(1*inch, height - 3*inch)  # Adjust starting point to account for logo and address

    lines = f"""
    
    {letter_content}

    Sincerely,
    Your Insurance Agent
    """.split('\n')

    for line in lines:
        text.textLine(line.strip())  # Remove leading and trailing spaces for each line

    c.drawText(text)
    c.showPage()
    c.save()

    return pdf_file_name
