import streamlit as st
from pdfquery import PDFQuery
import docx

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        pdf = PDFQuery(uploaded_file.name)
        pdf.load()
        text_elements = pdf.pq('LTTextLineHorizontal')
        text = [t.text for t in text_elements]
        return text
    elif uploaded_file.name.endswith('.docx'):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
            document = docx.Document(uploaded_file.name)
            text = []
            for paragraph in document.paragraphs:
                text.append(paragraph.text)
            whole_text = '\n'.join(text)
            return whole_text
    else:
        return uploaded_file.getvalue().decode("utf-8")
