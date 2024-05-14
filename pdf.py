from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
from datetime import date
from reportlab.lib.utils import ImageReader
import streamlit as st
import base64
import os

width, height = LETTER
# Define colors
color_primary = Color(0, 0.247, 0.455)  # Primary color (Ohka Blue)
color_secondary = Color(0.525, 0.678, 0.792)  # Secondary color (Light Blue)
color_accent = Color(1, 0.647, 0)  # Accent color (Ohka Orange)
color_text = Color(0, 0, 0)  # Text color (Black)
color_background = Color(1, 1, 1)  # Background color (White)

# Function to draw the canvas
def draw_canvas(c, df_transposed, customer_id):
    x = 128
    c.saveState()
    c.setStrokeColor(color_text)
    c.setLineWidth(0.5)

    c.setFont('Times-Roman', 10)
    # Email
    c.drawString(50, 730, "Email: liluboutik@gmail.com")

    # Phone
    c.drawString(width/2 - 20, 730, "Phone: +91 6281 921 240")
    c.setFont('Times-Bold', 10)  # Making Customer Number bold
    c.drawString(width/2 - 40, height-107, f"Customer Number: {customer_id}")
    c.setFont('Times-Roman', 10)

    # Add images
    c.drawImage("Store_image.png", width - inch*8-5, height-50, width=100, height=30, preserveAspectRatio=True)
    c.drawImage("Store_image.png", width - inch * 2, height-50, width=100, height=30, preserveAspectRatio=True, mask='auto')

    # Draw lines
    c.line(40, 740, LETTER[0] - 50, 740)
    c.line(66, 78, LETTER[0] - 66, 78)

    # Call page_header function
    page_header(c)
    tablemaker(c, df_transposed)
    page_footer(c, c.getPageNumber())

    c.restoreState()

# Function to draw the page header
def page_header(c):
    psHeaderText = ParagraphStyle("Heading", fontSize=16, alignment=TA_LEFT, borderWidth=3, textColor=color_accent)
    text = "Measurement Form Data"
    paragraphReportHeader = Paragraph(text, psHeaderText)
    paragraphReportHeader.wrapOn(c, width, height)
    paragraphReportHeader.drawOn(c, width/2 - 80, height-85)

    # Date
    today = date.today().strftime("%d-%m-%Y")
    date_style = ParagraphStyle("DateStyle", fontSize=10, alignment=TA_RIGHT, textColor=color_text)
    date_text = f"Date: {today}"
    date_paragraph = Paragraph(date_text, date_style)
    date_paragraph.wrapOn(c, width, height)
    date_paragraph.drawOn(c, -50, height - 65)

    # Draw decorative lines
    draw_decorative_lines(c)

# Function to draw decorative lines
def draw_decorative_lines(c):
    # Draw first decorative line
    d = Drawing(500, 1)
    line = Line(20, 0, 500, 0)
    line.strokeColor = color_accent
    line.strokeWidth = 2
    d.add(line)
    d.wrapOn(c, width, height)
    d.drawOn(c, 40, height-95)

    # Draw second decorative line
    d = Drawing(500, 1)
    line = Line(20, 0, 500, 0)
    line.strokeColor = color_accent
    line.strokeWidth = 0.5
    d.add(line)
    d.wrapOn(c, width-50, height)
    d.drawOn(c, 40, height-97)

# Function to create the table
def tablemaker(c, df_transposed):
    spacer = Spacer(10, 22)
    spacer.wrapOn(c, width, height)
    spacer.drawOn(c, 0, height-100)

    # Initialize data list
    d = []
    textData = ["No.", "Fields", "Values"]
    fontSize = 8
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    for text in textData:
        ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
        titlesTable = Paragraph(ptext, centered)
        d.append(titlesTable)

    data = [d]

    # Initialize formattedLineData list
    formattedLineData = []

    # Define font size and alignment styles
    fontSize = 8
    alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                  ParagraphStyle(name="02", alignment=TA_CENTER),
                  ParagraphStyle(name="03", alignment=TA_CENTER)]

    # Iterate over the transposed dataframe and construct table rows
    for index, row in df_transposed.iterrows():
        lineData = [str(index+1)] + list(row)
        columnNumber = 0
        for item in lineData:
            # Make numbers bold
            if columnNumber == 0 or columnNumber == 3:
                ptext = "<font size='%s'><b>%s</b></font>" % (fontSize-1, item)
            else:
                ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
            p = Paragraph(ptext, alignStyle[columnNumber])
            formattedLineData.append(p)
            columnNumber += 1
        data.append(formattedLineData)
        formattedLineData = []

    # Last Row
    totalRow = ["----", "-", "-"]
    for item in totalRow:
        ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
        p = Paragraph(ptext, alignStyle[1])
        formattedLineData.append(p)
    data.append(formattedLineData)

    # Create table
    table = Table(data, colWidths=[50, 200, 200])
    tStyle = TableStyle([
        ('LINEBEFORE', (0, 0), (0, -1), 1, color_accent),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, color_accent),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
        ('LINEABOVE', (0, 0), (-1, -1), 1, color_accent),
        ('BACKGROUND', (0, 0), (-1, 0), color_primary),
        ('BACKGROUND', (0, -1), (-1, -1), color_secondary),
        ('SPAN', (0, -1), (-2, -1))
    ])

    table.setStyle(tStyle)
    table.wrapOn(c, width, height)
    table.drawOn(c, (width-450)/2, height-680)

# Function to draw the page footer
def page_footer(c, page_number):
    # Footer
    footer_style = ParagraphStyle("FooterStyle", fontSize=10, alignment=TA_LEFT, textColor=color_text)
    footer_text = f"<b>Address</b>: Opp. Satya Enclave, Shirdi Saibaba Colony, Abhyudaya Nagar, Abhudaya Nagar Colony,  <br/> Bandlaguda Jagir, Hyderabad, Telangana 500086 <br/> <b>Business Hours</b>: Monday to Saturday: 11:00 AM – 08:30 PM Sunday: 11:00 AM – 02:00 PM"
    footer_paragraph = Paragraph(footer_text, footer_style)
    footer_paragraph.wrapOn(c, width - 100, height)
    footer_paragraph.drawOn(c, 80, 25)

    # Page number
    page_number_style = ParagraphStyle("PageNumberStyle", fontSize=10, alignment=TA_RIGHT, textColor=color_text)
    page_number_text = f"Page {page_number}"
    page_number_paragraph = Paragraph(page_number_text, page_number_style)
    page_number_paragraph.wrapOn(c, width, height)
    page_number_paragraph.drawOn(c, width - 60, 40)

# Function to add watermark to the PDF
def add_watermark(canvas, watermark_path, opacity=0.3):
    watermark = ImageReader(watermark_path)
    watermark_width = 400  # Adjust the width of the watermark as needed
    watermark_height = 300  # Adjust the height of the watermark as needed
    x = (width - watermark_width) / 2  # Calculate the x-coordinate for centering
    y = (height - watermark_height) / 2  # Calculate the y-coordinate for centering
    canvas.setFillColor(Color(0, 0, 0, alpha=opacity))  # Set the fill color with reduced opacity
    canvas.drawImage(watermark, x, y, width=watermark_width, height=watermark_height, mask='auto', preserveAspectRatio=True)
    canvas.setFillColor(Color(0, 0, 0, alpha=1))

# Function to generate PDF
def generate_pdf(df_transposed, filename, customer_id):
    my_path = f"{filename}.pdf"
    c = canvas.Canvas(my_path, pagesize=LETTER)
    c.setStrokeColor(color_accent)
    c.rect(0, 0, width, height, stroke=1, fill=0)
    # Get the current directory
    current_dir = os.getcwd()
    
    # Concatenate the current directory with the watermark filename
    watermark_path = os.path.join(current_dir, "boutique_flower2.png")
    
    add_watermark(c, watermark_path, opacity=0.3)
    draw_canvas(c, df_transposed, customer_id)
    c.showPage()
    c.save()
    print("saved")
    return my_path

# Function to display PDF in Streamlit
def display_pdf(pdf_filename):
    with open(pdf_filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_filename}">Download PDF file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Example usage
# df_transposed = ...  # Your transposed DataFrame
# filename = "example"
# customer_id = "123456"
# pdf_filename = generate_pdf(df_transposed, filename, customer_id)
# display_pdf(pdf_filename)
