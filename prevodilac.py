# funkcije vezane za openai vision i gpt-4-turbo
# cita mp3, prikazije mp3, downloaduje mp3, cita sa slike, cita sa slike sa url, downloaduje opis slike
# cita iz txt, pdf i worda, cuva u txt, pdf i word i downloaduje plus mp3 preview i downloaduje mp3
# prevod sa raznih na razne jezike 

from openai import OpenAI
import streamlit as st
import os
import requests
import base64
import io
from PIL import Image
from myfunc.mojafunkcija import (
    st_style,
    positive_login,
   )
from html2docx import html2docx
import markdown
import pdfkit
import PyPDF2
from langchain.document_loaders import UnstructuredFileLoader
import re
from pydub import AudioSegment


st_style()
client = OpenAI()
version = "29.11.23."

# glavni program odredjuje ulazni dokument i jezike za prevodjenje
def main():
    st.markdown(
            f"<p style='font-size: 10px; color: grey;'>{version}</p>",
            unsafe_allow_html=True,
        )
    st.subheader("Prevodilac")  # Setting the title for Streamlit application
    with st.expander("Pročitajte uputstvo"):
         st.caption(
                """
                       ### Korisničko Uputstvo za Prevodioca


    1. **Ulazni dokument**
       - Odaberite jezik ulaznog dokumenta.
       - Odaberite tip ulaznog dokumenta (tekst, audio, slika iz fajla, slika sa weba).
       - Odaberije jezik izlaznog dokumenta
       - Pritisnite Submit
       - Učitajte fajl u odabranom formatu koji želite da prevedete. Za sliku i audio videćete i preview.
       - Unesite uputstvo za prevodjenje ili prihvatite default opciju.
       - Odaberite opciju "Glasovna naracija" po želji.
       
    2. **Čuvanje**
       - U levoj bočnoj traci možete sačuvati izlaz u txt, pdf ili docx formatu.
       - Tonski zapis možete sačuvati na samom playeru, desno, tri tačke, download.
       
    **Napomena:**
    - Za transkribovanje zvučnih zapisa koristi se OpenAI Whisper model. Zvučni zapis mora biti u .MP3 formatu i ne veći od 25Mb.
    - Za prevod teksta i citanje sa slika koristi se odgovarajući OpenAI GPT-4 model.
    

    Srećno sa korišćenjem alata za prevodjenje!  
                       """
            )
    

   
    if "final_content" not in st.session_state:
        st.session_state["final_content"] = ""
        
    st.subheader("Ulazni dokument")
    izbor_ulaza = ''
    with st.form(key="ulaz", clear_on_submit=False):
        jezik_ulaza = st.selectbox("izaberite jezik ulaznog dokumenta", ("sr", "en", "fr", "de", "hu", "it", "es"))
        izbor_ulaza = st.selectbox("Odaberite tip ulaznog dokumenta", ("Tekst", "Audio", "Slika iz fajla", "Slika sa weba" ))
        jezik_izlaza = st.selectbox("izaberite jezik izlaznog dokumenta", ("srpski", "english", "french", "german", "hungarian", "italian", "spanish"))    
        submit_button = st.form_submit_button(label="Submit")
            
    if izbor_ulaza == "Slika iz fajla":
        read_local_image(jezik_izlaza)
    elif izbor_ulaza == "Slika sa weba":
        read_url_image(jezik_izlaza)
    elif izbor_ulaza == "Tekst":
        citaj_tekst(jezik_izlaza)
    elif izbor_ulaza == "Audio":
        cita_audio(jezik_ulaza, jezik_izlaza)
         
   
        
        
# cita sa slike sa url i prima jezik izlaza
def read_url_image(jezik_izlaza):
    # version url
    
    st.info("Čita sa slike sa URL")
    content = ""
    img_url = st.text_input("Unesite URL slike ")
    
    image_f = os.path.basename(img_url)   
    if img_url !="":
        st.image(img_url, width=150)
        placeholder = st.empty()    
        with placeholder.form(key="my_image_url", clear_on_submit=False):
            default_text = f"What is in this image? Please read and reproduce the text in the {jezik_izlaza} language. Read the text as is, \
                            do not correct any spelling and grammar errors. "
            
            upit = st.text_area("Unesite uputstvo ", default_text)
            audio_i = st.checkbox("Glasovna naracija")
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                with st.spinner("Sačekajte trenutak..."):         
                    response = client.chat.completions.create(
                      model="gpt-4-vision-preview",
                      messages=[
                        {
                          "role": "user",
                          "content": [
                            {"type": "text", "text": upit},
                            {
                              "type": "image_url",
                              "image_url": {
                                "url": img_url,
                              },
                            },
                          ],
                        }
                      ],
                      max_tokens=300,
                    )
                    content = response.choices[0].message.content
                    if audio_i == True:
                            st.write("Glasovna naracija")    
                            audio_izlaz(content)
                    with st.expander("Opis slike"):
                        st.write(content)
                        
                    st.session_state["final_content"] = content
        with st.sidebar:      
            if st.session_state.final_content !="":
                sacuvaj_dokument(st.session_state.final_content, image_f.name)
    
# cita sa slike iz fajla i prima jezik izlaza
def read_local_image(jezik_izlaza):
    # version local file
    
    st.info("Čita sa slike")
    image_f = st.file_uploader(
        "Odaberite sliku",
        type="jpg",
        key="slika_",
        help="Odabir dokumenta",
    )
    content = ""
  
    
    if image_f is not None:
        base64_image = base64.b64encode(image_f.getvalue()).decode('utf-8')
        # Decode the base64 image
        image_bytes = base64.b64decode(base64_image)
        # Create a PIL Image object
        image = Image.open(io.BytesIO(image_bytes))
        # Display the image using st.image
        st.image(image, width=150)
        placeholder = st.empty()
        # st.session_state["question"] = ""

        with placeholder.form(key="my_image", clear_on_submit=False):
            default_text = f"What is in this image? Please read and reproduce the text in the {jezik_izlaza} language. Read the text as is, \
do not correct any spelling and grammar errors. "
            
            upit = st.text_area("Unesite uputstvo ", default_text)  
            audio_i = st.checkbox("Glasovna naracija")
            submit_button = st.form_submit_button(label="Submit")
            
            if submit_button:
                with st.spinner("Sačekajte trenutak..."):            
                    # Path to your image
                    api_key = os.getenv("OPENAI_API_KEY")
                    # Getting the base64 string
                    headers = {
                      "Content-Type": "application/json",
                      "Authorization": f"Bearer {api_key}"
                    }

                    payload = {
                      "model": "gpt-4-vision-preview",
                      "messages": [
                        {
                          "role": "user",
                          "content": [
                            {
                              "type": "text",
                              "text": upit
                            },
                            {
                              "type": "image_url",
                              "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                              }
                            }
                          ]
                        }
                      ],
                      "max_tokens": 300
                    }

                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

                    json_data = response.json()
                    content = json_data['choices'][0]['message']['content']
                    if audio_i == True:
                        st.write("Glasovna naracija")
                        audio_izlaz(content)
                    with st.expander("Opis slike"):
                        st.write(content)
                    
                    st.session_state["final_content"] = content        
        with st.sidebar:      
            if st.session_state.final_content !="":
                
                sacuvaj_dokument(st.session_state.final_content, image_f.name)
                
# cita sa audio fajla i prima jezik ulaza i jezik izlaza
def cita_audio(jezik_ulaza, jezik_izlaza):
    # Read OpenAI API key from env
    st.info("Čita sa audio zapisa")
    audio_file = st.file_uploader(
        "Max 25Mb",
        type="mp3",
        key="audio_",
        help="Odabir dokumenta",
    )
    content = ""
        
       
    if audio_file is not None:
        placeholder = st.empty()
        # st.session_state["question"] = ""
        with placeholder.form(key="my_image", clear_on_submit=False):
            st.write("Ulazni audio fajl")
            st.audio(audio_file.getvalue(), format="audio/mp3")
            st.session_state["question"] = ""
            st.write("Izlazni dokument")
            default_text=f""" You are the {jezik_izlaza} language expert. You must translate the text to the {jezik_izlaza} language and fix grammar and spelling errors but otherwise keep the text as is, in the Serbian language. \
Your task is to correct any spelling discrepancies in the transcribed text. \
Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided. 
"""
            upit = st.text_area("Unesite uputstvo ", default_text)
            audio_i = st.checkbox("Glasovna naracija")   
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                with st.spinner("Sačekajte trenutak..."):
                # does transcription of the audio file and then corrects the transcript
                    content = generate_corrected_transcript(upit, audio_file, jezik_ulaza)
                    if audio_i == True:
                        st.write("Glasovna naracija")
                        audio_izlaz(content)
                    with st.expander("Procitajte prevod", expanded = True):
                        st.write(content)
                        
                    st.session_state["final_content"] = content
                with st.sidebar:      
                    if st.session_state.final_content !="":
                        sacuvaj_dokument(st.session_state.final_content, audio_file.name)            
 
                          
# transkribije audio fajl, prima ime fajla i jezik ulaza i vraca tekst
def transcribe(audio_file, jezik):
    transcript = client.audio.transcriptions.create(
                            model="whisper-1", 
                            file=audio_file, 
                            language=jezik, 
                            response_format="text"
    )
    return transcript

# koriguje sirovi transkript, prima sistemski prompt, audio fajl i jezik ulaza i vraca tekst
def generate_corrected_transcript(system_prompt, audio_file, jezik):
        
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcribe(audio_file, jezik) # does transcription of the audio file
            }
        ]
    )

    return response.choices[0].message.content

# cuvaj dokument, prima tekst, ime fajla i cuva za download u txt, docx i pdf formatu
def sacuvaj_dokument(content, file_name):
    st.info("Čuva dokument")
    options = {
        "encoding": "UTF-8",  # Set the encoding to UTF-8
        "no-outline": None,
        "quiet": "",
    }
    html = markdown.markdown(content)
    buf = html2docx(html, title="Zapisnik")
    word_data = buf.getvalue()
    pdf_data = pdfkit.from_string(html, False, options=options)
    
    st.download_button(
        "Download Prevod .txt",
        content,
        file_name=f"{file_name}.txt",
        help="Čuvanje dokumenta",
    )
            
    st.download_button(
        label="Download Prevod .docx",
        data=word_data,
        file_name=f"{file_name}.docx",
        mime="docx",
        help= "Čuvanje dokumenta",
    )
            
    st.download_button(
        label="Download Prevod .pdf",
        data=pdf_data,
        file_name=f"{file_name}.pdf",
        mime="application/octet-stream",
        help= "Čuvanje dokumenta",
    )


# cita tekst i prima jezik izlaza izlaz je mp3 player
def audio_izlaz(content):
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        json={
            "model" : "tts-1-hd",
            "voice" : "alloy",
            "input": content,
        
        },
    )    
    audio = b""
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        audio += chunk

    # Convert the byte array to AudioSegment
    audio_segment = AudioSegment.from_file(io.BytesIO(audio))

    # Save AudioSegment as MP3 file
    mp3_data = io.BytesIO()
    audio_segment.export(mp3_data, format="mp3")
    mp3_data.seek(0)

    # Display the audio using st.audio
    st.caption("mp3 fajl možete download-ovati odabirom tri tačke ne desoj strani audio plejera")
    st.audio(mp3_data.read(), format="audio/mp3")    

# cita tekst i prevodi. Prima jezik izlaza i izlaz je prevedeni tekst
def citaj_tekst(jezik_izlaza):
    
    st.info("Čita tekst")
    uploaded_file = st.file_uploader(
        "Izaberite tekst za sumarizaciju",
        key="upload_file",
        type=["txt", "pdf", "docx"],
        help = "Odabir dokumenta",
    )

    if uploaded_file is not None:
        
        with io.open(uploaded_file.name, "wb") as file:
            file.write(uploaded_file.getbuffer())

        if ".pdf" in uploaded_file.name:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            num_pages = len(pdf_reader.pages)
            text_content = ""

            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                text_content += page_obj.extract_text()
            text_content = text_content.replace("•", "")
            text_content = re.sub(r"(?<=\b\w) (?=\w\b)", "", text_content)
            with io.open("temp.txt", "w", encoding="utf-8") as f:
                f.write(text_content)

            loader = UnstructuredFileLoader("temp.txt", encoding="utf-8")
        else:
            # Creating a file loader object
            loader = UnstructuredFileLoader(file_path=uploaded_file.name, encoding="utf-8")

        result = loader.load()
                
        content = "Zapisnik"   
        with st.form(key="my_form", clear_on_submit=False):
            system_prompt=f"""You are a multi-lingual language expert. You must translate the text to the {jezik_izlaza} language and fix grammar \
and spelling errors but otherwise keep the text as is. 
"""
            opis = st.text_area(
                "Unesite instrukcije za sumarizaciju : ",
                system_prompt,
                key="prompt_prva",
                height=150,
                help = "Unos prompta."
            )
            audio_i = st.checkbox("Glasovna naracija")
            opis = f"{opis} {result[0].page_content}" 
            submit_button = st.form_submit_button(label="Submit")
            
            if submit_button:
                with st.spinner("Sačekajte trenutak..."):
                    response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    temperature=0,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": opis 
                        }
                    ]
                )

                content =  response.choices[0].message.content
                st.session_state["final_content"] = content
            if st.session_state.final_content != "Zapisnik":
                if audio_i == True:
                    st.write("Glasovna naracija")
                    audio_izlaz(content)    
                with st.expander("Sažetak", True):
                    st.write(content)  # Displaying the summary
        with st.sidebar:      
            if st.session_state.final_content !="":
                st.session_state["final_content"] = content
                sacuvaj_dokument(st.session_state.final_content, uploaded_file.name)
                
                    

# Deployment on Stremalit Login functionality
deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")

if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main, " ")
else:
    if __name__ == "__main__":
        main()