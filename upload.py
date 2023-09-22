import streamlit as st
from pdfquery import PDFQuery
# must install pdfquery: pip install pdfquery
import docx

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])
# moze da se prebaci u moja funkcija

if uploaded_file is not None:
    
    if uploaded_file.name.endswith('.pdf'):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        pdf = PDFQuery(uploaded_file.name)
        pdf.load()

        # Use CSS-like selectors to locate the elements
        text_elements = pdf.pq('LTTextLineHorizontal')

        # Extract the text from the elements
        text = [t.text for t in text_elements]

        st.write(text)
    elif uploaded_file.name.endswith('.docx'):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
            document = docx.Document(uploaded_file.name)
            text = []
            for paragraph in document.paragraphs:
                text.append(paragraph.text)
            whole_text = '\n'.join(text)
        st.write(whole_text)
    else:
        st.write(uploaded_file.getvalue().decode("utf-8"))