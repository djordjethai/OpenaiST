from xhtml2pdf import pisa

# Ovo vec imamo u zapisniku uradjeno
source_html = "<html><body><h1>Hello, world!</h1></body></html>"
output_filename = "output.pdf"


# ovo treba zameniti u nasem zapisniku
# Utility function to convert HTML to PDF
def convert_html_to_pdf(source_html, output_filename):
    # Open the output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)

    # Close the output file
    result_file.close()

    # Return False on success and True on errors
    return pisa_status.err

# naravno, ovo ne treba ovako, nego da se pozove funkcija
# Main program
if __name__ == "__main__":
    # Show logging information (optional)
    pisa.showLogging()

    # Call the utility function to convert HTML to PDF
    convert_html_to_pdf(source_html, output_filename)
