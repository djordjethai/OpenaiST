# AI Asistent Pravnik - Pracenje zakona
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import streamlit as st
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
import requests
from bs4 import BeautifulSoup
from pravnik_fukncije import dl_paragraf, dl_parlament, lista_zakona, sumiraj_zakone
from myfunc.mojafunkcija import positive_login
import os


# prikuplja podatke o zakonima sa sajtova i salje mail obavestenja sa linkovima na izmene i dopune zakona
#	https://www.paragraf.rs/izmene_i_dopune/
#	http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html  


# salje mail sa gmail accounta, unosi se uputsvo, moze da se automatizuje da cita iz fajla, preraditi na Outlook
def posalji_mail(uputstvo):
        
    toolkit = GmailToolkit()
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    # mora se definisati prompt template da bismo prosledili sve linkove i sazetke
    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )
    
    agent.run(uputstvo)
    

# skida zakone sa sajta paragraf.rs
def procitaj_paragraf():
    # URL of the webpage to scrape
    url = 'https://www.paragraf.rs/izmene_i_dopune/'  
    suma = ""
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the <li> elements with class "pl-20"
        li_elements = soup.find_all('li', class_='pl-20')
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link.get('href')
                description = link.get_text().strip().replace("\n", " ").replace("\t", " ").replace("Ä", "Ć").replace("Ä", "Č").replace("Ä", "Đ").replace("Å ", "Š").replace("Å½", "Ž")
                if href and description:
                    mojalista_zakona = lista_zakona()
                    # samo relevantni zakoni
                    for zakon in mojalista_zakona:
                        if zakon.lower() in description.lower():
                            # privremeno samo da vidim da li radi
                            i = 0
                            for i  in range(2): 
                                i +=1 
                               
                                link = "https://www.paragraf.rs/izmene_i_dopune/" + href.replace(" ", "%20")
                                full_text = dl_paragraf(link)
                                suma = sumiraj_zakone(full_text, description)
                                izvestaj = f"Sa sajta {url} sumiram zakon sa linka {link} \n\n Evo i krakog pregleda zakona: \n\n {suma}" 
                                return izvestaj
                             

# skida zakone sa sajta parlament.gov.rs                                                                                                                         
def procitaj_parlament():
    
    # URL of the webpage you want to scrape
    url = 'http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html' 
    suma = ""
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
        # Find all the <li> elements with class "td"
        li_elements = soup.find_all('td')
        # Iterate through the <li> elements and extract the href attribute from the <a> tags within them
        for li in li_elements:
            link = li.find('a')
            if link:
                href = link.get('href')
                description = link.get_text()
                if href and description:
                    mojalista_zakona = lista_zakona()
                    # samo relevantni zakoni
                    for zakon in mojalista_zakona:
                        if zakon.lower() in description.lower():
                            # privremeno samo da vidim da li radi
                            i = 0
                            for i  in range(2): 
                                i +=1
                                
                                link = "http://www.parlament.gov.rs" + href.replace(" ", "%20") 
                                ime_fajla = dl_parlament(link)
                                suma = sumiraj_zakone(ime_fajla, description)
                                izvestaj = f"Sa sajta {url} sumiram zakon sa linka {link} \n\n Evo i krakog pregleda zakona: \n\n {suma}" 
                                return izvestaj
    
# prima ceo tekst maila, sa sve linkovima i sa sezecima
def main():

    st.title("AI Asistent Pravnik - Praćenje zakona")
    st.caption("Ver 29.10.23")
    with st.expander("Pročitajte uputstvo:", expanded=True):
            st.caption(
                """
                    Program prikuplja nove zakone ili izmene zakona sa sajtova Paragraf i Parlament, a iz liste zakona koji su objavljeni u željenom periodu i pripadaju listi zakona od interesa radi sažetak. Zatim linkove sa zakonima i sažetke šalje na email po izboru.
                    Treba rešiti: Zašto se čitaju dva sajta, tj šta ako su isti zakoni?
                    Treba rešiti: Koji period ili broj zakona se čita?
                    Tehničko pitanje: Da se email šalje sa positive.rs naloga tj da se koristi Outlook i office365
                    Tehničko pitanje: Kako postaviti filtere?
                    """
            )
    with st.form("mail_form"):
        
        placeholder = st.empty()
        submit_button = st.form_submit_button(label='Počni program')        

        # Every form must have a submit button.
        if submit_button:
            with st.spinner("Obradjujem ..."):
                with placeholder:
                    st.info("Prikupljam zakone")
                    suma_paragraf = procitaj_paragraf()
                    suma_parlament = procitaj_parlament()
                    text_maila = suma_paragraf + "\n\n" + suma_parlament
                    # ovde treba lepo uobliciti email ono gore moze samo statruj program
                    uputstvo = f"""
                    Create a draft email to djordje.medakovic@gmail.com with a subject Novi Zakoni. Do not send it. Tekst maila mora da bude tačno ovakav bez ikakvih promena: 
                    
                    Evo izveštaja o novim zakonima: 

                        {text_maila} 
                        
                    Srdačan pozdrav,             
                    """             
               
                    st.info("Šaljem mail")    
                    posalji_mail(uputstvo)
                    st.success("Poslat email, obrada je završena")

# Deployment on Stremalit Login functionality
deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")

if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main, " ")
else:
    if __name__ == "__main__":
        main()
