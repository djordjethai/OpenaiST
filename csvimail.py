from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import streamlit as st
from langchain.agents import create_csv_agent
import io 
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials

# salje mail sa gmail accounta, unosi se uputsvo, moze da se automatizuje da cita iz fajla
def posalji_mail():

    toolkit = GmailToolkit()
    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )
    uputstvo = ""
    uputstvo = st.text_area("Uputstvo za slanje e maila: ")
    if uputstvo:
        st.info(agent.run(uputstvo))

    
    
# prikuplja podatke o zakonima sa sajtova
#	https://www.paragraf.rs/izmene_i_dopune/
#	http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html  
#
# i potom salje mail obavestenja sa linkovima na izmene i dopune zakona

def procitaj_paragraf():
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    # URL of the webpage you want to scrape
    url = 'https://www.paragraf.rs/izmene_i_dopune/'  # Replace with your desired URL

    # Define the start and end dates (in ddmmyy format) to filter the links
    start_date = input("unesti pocetni datum kao ddmmyy: ")  # Replace with your desired start date
    end_date = input("unesti krajnji datum kao ddmmyy: ")  # Replace with your desired start date
    start_date = datetime.strptime(start_date, '%d%m%y')
    end_date = datetime.strptime(end_date, '%d%m%y')
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the <li> elements with class "pl-20"
        li_elements = soup.find_all('li', class_='pl-20')

        # Create a list to store the links
        link_list = []

        # Iterate through the <li> elements and extract the href attribute from the <a> tags within them
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link.get('href')
                if href is not None:
                    # Extract the ddmmyy portion of the href
                    date_string = href[:6]
                    link_date = datetime.strptime(date_string, '%d%m%y')
                    # Check if the link's date falls within the desired range
                    if start_date <= link_date <= end_date:
                        link_list.append(href)
                    print(link_list)
        # Save the filtered list of links to a text file
        with open('filtered_PARAGRAF.txt', 'w', encoding="utf-8") as file:
            for link in link_list:
                file.write(url + link + '\n')


    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# sledeci korak je da uradi summary svakog linka i da posalje email sa summary-jem i linkom
def sumiraj_paragraf():

    import requests
    from bs4 import BeautifulSoup
    import re

    # URL of the webpage you want to scrape ovaj deo se se automatizovati da cita iz fajla
    #url = 'https://www.paragraf.rs/izmene_i_dopune/070923-zakon-o-izmenama-i-dopunama-zakona-o-bezbednosti-saobracaja-na-putevima.html'  # Replace with your desired URL
    url = "https://www.paragraf.rs/izmene_i_dopune/290423-zakon-o-izmenama-i-dopunama-zakona-o-upravljanju-otpadom.html"
    
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

        # Save the extracted content to a text file with UTF-8 encoding
        with open('extracted_content.txt', 'w', encoding='utf-8-sig') as file:
            file.write(full_text)


        print("Content has been extracted and saved to 'extracted_content.txt'.")
    else:
        print("Failed to retrieve the web page.")



# skida zakone iz parlamenta
# import pandas as pd

def procitaj_parlament():
    from datetime import datetime
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse

    # URL of the webpage you want to scrape
    url = 'http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html'  # Replace with your desired URL
    
    # Define the start and end dates (in ddmmyy format) to filter the links
    start_date = input("unesti pocetni datum kao ddByy: ")  # Replace with your desired start date
    end_date = input("unesti krajnji datum kao ddByy: ")  # Replace with your desired start date
    start_date = datetime.strptime(start_date, '%d%m%y')
    end_date = datetime.strptime(end_date, '%d%m%y')
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
        # Find all the <li> elements with class "pl-20"
        li_elements = soup.find_all('td')

        # Create a list to store the links
        link_description_list = []

        # Iterate through the <li> elements and extract the href attribute from the <a> tags within them
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link.get('href')
                description = link.get_text()
                if href and description:
                    link_description_list.append({'Link': href, 'Description': description})

        for link_info in link_description_list:
            link_info['Link'] = "http://www.parlament.gov.rs" + link_info['Link'].replace(" ", "%20")            
        # Save the filtered list of links to a text file
        with open('filtered_PARLAMENT.txt', 'w', encoding="utf-8") as file:
            for link_info in link_description_list:
                if link_info['Description'][-3:] == 'PDF' or link_info['Description'][-3:] == 'DOC':
                    pass
                else:
                    file.write(f"opis: {link_info['Description']} websajt: {link_info['Link']}\n")
    
    # Function to check if a string is a valid date in the format d. month yyyy
    # def is_valid_date(date_str):
    #     try:
    #         datetime.strptime(date_str, '%d. %B %Y.')
    #         return True
    #     except ValueError:
    #         return False
    # td_elements = soup.find_all('td', nowrap=True)
    # dates = [td.text.strip() for td in td_elements if is_valid_date(td.text.strip())]
    # Find all <td> elements and check for valid dates
    

    # Create a new DataFrame containing the filtered dates
   

    # Convert the extracted dates to datetime objects for comparison
   

# download pdf from website link
def dl_pdf():

    import requests

    url = "http://www.parlament.gov.rs/upload/archive/files/lat/pdf/zakoni/13_saziv/416-23%20-%20lat..pdf"
    response = requests.get(url)

    if response.status_code == 200:
        with open("myfile.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        print("File downloaded successfully as 'myfile.pdf'")
    else:
        print("Failed to download the file")



# # spisak zakona od interesa
# #
# # 	Direktni uticaj
# # •	ZAKON O PENZIJSKOM I INVALIDSKOM OSIGURANJU
# # •	ZAKON O ELEKTRONSKOM FAKTURISANJU
# # •	ZAKON O ROKOVIMA IZMIRENJA NOVČANIH OBAVEZA U KOMERCIJALNIM TRANSAKCIJAMA
# # •	ZAKON O POREZU NA DOBIT PRAVNIH LICA
# # •	ZAKON O PRIVREDNIM DRUŠTVIMA
# # •	ZAKON O ZAPOŠLJAVANJU I OSIGURANJU ZA SLUČAJ NEZAPOSLENOSTI
# # •	ZAKON O OBLIGACIONIM ODNOSIMA
# # •	ZAKON O RADU
# # •	ZAKON O CENTRALNOM REGISTRU OBAVEZNOG SOCIJALNOG OSIGURANJA
# # •	ZAKON O JAVNIM NABAVKAMA
# # •	ZAKON O INFORMACIONOJ BEZBEDNOSTI
# # •	ZAKON O MIRNOM REŠAVANJU RADNIH SPOROVA
# #
# # 	Indirektni uticaj
# # •	ZAKON O UPRAVLJANJU OTPADOM
# # •	ZAKON O ZAPOŠLJAVANJU STRANACA
# # •	ZAKON O CENTRALNOJ EVIDENCIJI STVARNIH VLASNIKA
# # •	CARINSKI ZAKON
# # •	ZAKON O FISKALIZACIJI
# # •	ZAKON O PORESKOM POSTUPKU I PORESKOJ ADMINISTRACIJI
# # •	ZAKON O PATENTIMA
# # •	ZAKON O POSTUPKU REGISTRACIJE U AGENCIJI ZA PRIVREDNE REGISTRE
# # •	ZAKON O ELEKTRONSKOM DOKUMENTU, ELEKTRONSKOJ IDENTIFIKACIJI I USLUGAMA OD POVERENJA U ELEKTRONSKOM POSLOVANJU
# # •	ZAKON O OSIGURANJU
# # •	ZAKON O SPREČAVANJU PRANJA NOVCA I FINANSIRANJA TERORIZMA
# # •	ZAKON O PARNIČNOM POSTUPKU
# # •	ZAKON O JAVNIM PREDUZEĆIMA
# # •	ZAKON O ELEKTRONSKOJ TRGOVINI
# # •	ZAKON O ZALOŽNOM PRAVU NA POKRETNIM STVARIMA UPISANIM U REGISTAR
# # •	ZAKON O STEČAJU
# # •	ZAKON O INSPEKCIJSKOM NADZORU
# # •	UREDBA O KOLIČINI RASHODA (KALO, RASTUR, KVAR I LOM) NA KOJI SE NE PLAĆA AKCIZA
# # •	ODLUKA O OBRAZOVANJU SAVETA ZA MALA I SREDNJA PREDUZEĆA, PREDUZETNIŠTVO I KONKURENTNOST
# #

def relevantni_zakoni():
    import re
    # List of strings to search for in the 'opis' field
    search_strings = [
        "O ELEKTRONSKOM FAKTURISANJU",
        "O ROKOVIMA IZMIRENJA NOVČANIH OBAVEZA U KOMERCIJALNIM TRANSAKCIJAMA",
        "O POREZU NA DOBIT PRAVNIH LICA",
        "O PRIVREDNIM DRUŠTVIMA",
        "O ZAPOŠLJAVANJU I OSIGURANJU ZA SLUČAJ NEZAPOSLENOSTI",
        "O OBLIGACIONIM ODNOSIMA",
        "O Privremenom registru majki i drugih lica",
    ]

    opis = None
    websajt = None

    extracted_data = []

    # Open and read the text file
    with open('filtered_PARLAMENT.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Iterate through the lines and extract website links if the search strings are found
    # Iterate through the lines and extract website links
    for line in lines:
        if "opis:" in line:
            parts = line.strip().split("websajt:")
            if len(parts) == 2:
                opis = parts[0].strip()[5:]  # Extract 'opis' field
                websajt = parts[1].strip()  # Extract 'websajt' field

                # Check if any search string is present in the 'opis' field (case-insensitive)
                if any(search_string.lower() in opis.lower() for search_string in search_strings):
                    extracted_data.append((opis, websajt))

    # Print the extracted website links
    with open('extracted_filter.txt', 'w', encoding='utf-8') as output_file:
        for opis, websajt in extracted_data:
            output_file.write(f'opis: {opis} websajt: {websajt}\n')















relevantni_zakoni()