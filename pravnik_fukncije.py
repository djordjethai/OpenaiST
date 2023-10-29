import requests
import streamlit as st
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def dl_paragraf(url):
   
    # URL of the webpage you want to scrape se prosledkjuje kao parametar
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)

        # Find all <p> elements with a class that matches "normal" (e.g., "normal", "normal1", "normal2", etc.)
        normal_paragraphs = soup.find_all('p')

        # Create a list to store the extracted text
        text_content = []

        # Iterate through the selected paragraphs, strip HTML tags, and append the text to the list
        for paragraph in normal_paragraphs:
            text = paragraph.get_text(strip=True)
            text_content.append(text)

        # Join the list of text into a single string, separating paragraphs with newlines
        full_text = '\n'.join(text_content)
        with open("temp.txt", "w", encoding="utf-8") as file:
    # Write the string to the file
            file.write(full_text)
    else:
        st.error("Failed to retrieve the web page.")
        full_text = " "

    return "temp.txt"

def dl_parlament(url):
     
    response = requests.get(url)

    if response.status_code == 200:
        ime_fajla = url.rsplit('/', 1)[-1]
        
        # ovo zameniti sa ucitavanjem fajla u varijablu
        with open(ime_fajla, "wb") as pdf_file:
            pdf_file.write(response.content)
        return ime_fajla
    else:
        st.error(f"Failed to download the file {ime_fajla}")


# izradjuje sumarizaciju zakona
def sumiraj_zakone(ime_fajla, zakon):

    st.info("Sumiram zakon: " + zakon)
    # Loading the text document
    loader = UnstructuredFileLoader(ime_fajla, encoding="utf-8")    
    text_doc = loader.load()
    
    # Initializing ChatOpenAI model
    llm = ChatOpenAI(
          model_name="gpt-3.5-turbo-16k", temperature=0
         )

    chunk_size = 3000
    chunk_overlap = 0
    text_splitter = RecursiveCharacterTextSplitter(
         chunk_size=chunk_size, chunk_overlap=chunk_overlap
      ) 
    
    # Splitting the loaded text into smaller chunks
    docs = text_splitter.split_documents(text_doc)
   
    # promptovi za prvu i drugu fazu sumarizacije
    prompt_string_pocetak = """
        Uradi kratki summary na srpskom jeziku. Posebno istakni delove vezane za IT i računare

        {text}

        SUMMARY:
    """
    
    prompt_string_kraj = """
        Sumiraj na oko 200 reči na srpskom jeziku. 

        {text}

        SUMMARY:
    """
    
    PROMPT = PromptTemplate(
            template=prompt_string_pocetak, input_variables=["text"]
        )  # Creating a prompt template object
    PROMPT_pam = PromptTemplate(
            template=prompt_string_kraj, input_variables=["text"]
        )  # Creating a prompt template object

    
    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        verbose=True,
        map_prompt=PROMPT,
        combine_prompt=PROMPT_pam,
        token_max=4000,
    )

    # Run the summarization chain
    sumarizacija = chain.run(docs)
       
    return sumarizacija


# lista zakona od interesa
def lista_zakona():
    search_strings = [
        " O PENZIJSKOM I INVALIDSKOM OSIGURANJU",
        " O ELEKTRONSKOM FAKTURISANJU",
        " O ROKOVIMA IZMIRENJA NOVČANIH OBAVEZA U KOMERCIJALNIM TRANSAKCIJAMA",
        " O POREZU NA DOBIT PRAVNIH LICA",
        " O PRIVREDNIM DRUŠTVIMA",
        " O ZAPOŠLJAVANJU I OSIGURANJU ZA SLUČAJ NEZAPOSLENOSTI",
        " O OBLIGACIONIM ODNOSIMA",
        " O RADU",
        " O CENTRALNOM REGISTRU OBAVEZNOG SOCIJALNOG OSIGURANJA",
        " O JAVNIM NABAVKAMA",
        " O INFORMACIONOJ BEZBEDNOSTI",
        " O MIRNOM REŠAVANJU RADNIH SPOROVA",
        " O UPRAVLJANJU OTPADOM",
        " O ZAPOŠLJAVANJU STRANACA",
        " O CENTRALNOJ EVIDENCIJI STVARNIH VLASNIKA",
        " CARINSKI ",
        " CARINSKOM ",
        " O FISKALIZACIJI",
        " O PORESKOM POSTUPKU I PORESKOJ ADMINISTRACIJI",
        " O PATENTIMA",
        " O POSTUPKU REGISTRACIJE U AGENCIJI ZA PRIVREDNE REGISTRE",
        " O ELEKTRONSKOM DOKUMENTU, ELEKTRONSKOJ IDENTIFIKACIJI I USLUGAMA OD POVERENJA U ELEKTRONSKOM POSLOVANJU",
        " O OSIGURANJU",
        " O SPREČAVANJU PRANJA NOVCA I FINANSIRANJA TERORIZMA",
        " O PARNIČNOM POSTUPKU",
        " O JAVNIM PREDUZEĆIMA",
        " O ELEKTRONSKOJ TRGOVINI",
        " O ZALOŽNOM PRAVU NA POKRETNIM STVARIMA UPISANIM U REGISTAR",
        " O STEČAJU",
        " O INSPEKCIJSKOM NADZORU",
        " O KOLIČINI RASHODA (KALO, RASTUR, KVAR I LOM) NA KOJI SE NE PLAĆA AKCIZA",
        " O OBRAZOVANJU SAVETA ZA MALA I SREDNJA PREDUZEĆA, PREDUZETNIŠTVO I KONKURENTNOST",
        
    ]

    return search_strings