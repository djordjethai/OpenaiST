
import markdown
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Read the Markdown content from a file
with open("readme.md", "r", encoding="utf-8") as md_file:
    markdown_content = md_file.read()

# Convert Markdown to HTML
html_content = markdown.markdown(markdown_content, extensions=['markdown.extensions.extra'])

# Create a PDF file
output_filename = "output.pdf"

# Define a font that supports Serbian Latin characters (DejaVu Serif)
#pdfmetrics.registerFont(TTFont("SansSerif", "SansSerif.ttf"))

# Create a canvas and set the font
c = canvas.Canvas(output_filename, pagesize=letter)
#c.setFont("DejaVuSerif", 12)

# Write the HTML content to the PDF
pisa_status = pisa.CreatePDF(html_content, dest=c)

# Close the canvas
c.save()

if not pisa_status.err:
    print("Markdown to PDF conversion successful.")
else:
    print(f"Markdown to PDF conversion failed with error: {pisa_status.err}")
