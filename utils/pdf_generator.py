import io
import re
from fpdf import FPDF

class RecipePDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(220, 20, 60) # Crimson red
        self.cell(0, 15, 'SmartChef AI Recipe', border=0, align='C', ln=1)
        self.set_draw_color(200, 200, 200)
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_recipe_pdf(recipe_text, recipe_name):
    """
    Parses recipe markdown text and generates a highly formatted clean PDF buffer.
    """
    pdf = RecipePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Strip markdown bolding and asterisks to make parsing cleaner
    clean_text = recipe_text.replace('**', '')
    
    lines = clean_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        # Section Headers (Cooking Time:, Ingredients Required:, etc.)
        if line.endswith(':'):
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 10, line, ln=1)
        # Bullet points
        elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
            pdf.set_font('helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 7, '-')
            
            # Clean non-latin1 chars from remaining line content
            content = line[1:].strip()
            content = content.replace('\u2022', '-')
            content = content.replace('\u2013', '-')
            content = content.replace('\u2014', '-')
            content = content.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(0, 7, content)
        # Numbered lists (1. 2. 3.)
        elif re.match(r'^\d+\.', line):
            pdf.set_font('helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            
            # Clean non-latin1 chars
            content = line
            content = content.replace('\u2022', '-')
            content = content.replace('\u2013', '-')
            content = content.replace('\u2014', '-')
            content = content.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(0, 7, content)
        # Normal Text
        else:
            pdf.set_font('helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            
            # Clean non-latin1 chars
            content = line
            content = content.replace('\u2022', '-')
            content = content.replace('\u2013', '-')
            content = content.replace('\u2014', '-')
            content = content.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(0, 7, content)
            
    # Output to a BytesIO buffer instead of a file
    pdf_buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin-1')
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
    
    return pdf_buffer
