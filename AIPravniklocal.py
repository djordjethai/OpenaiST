# AI Asistent Pravnik - Pracenje zakona
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
import requests
from bs4 import BeautifulSoup
from pravnik_fukncije import dl_paragraf, dl_parlament, lista_zakona, sumiraj_zakone, parse_serbian_date
from myfunc.mojafunkcija import positive_login
import re
from datetime import date, datetime, timedelta
import locale

# Set the locale to Serbian
locale.setlocale(locale.LC_TIME, 'sr_RS.utf8')


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
    llm = ChatOpenAI(model_name = "gpt-3.5-turbo-16k", temperature=0)
    agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )
    
    agent.run(uputstvo)
    


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
        tr_elements = soup.find_all('tr')
        # Iterate through the <li> elements and extract the href attribute from the <a> tags within them
        izvestaj = ""
        
        for tr in tr_elements:
            link = tr.find('a')
            datum = ""
            date_str = "01. Januar 2020."
            date_obj = date.today()
            if link:
                    # Find the <td nowrap> element within the current <tr>
                    td_nowrap = tr.find('td', {"nowrap": True})
        
                    if td_nowrap:
                        # Extract and print the text from the <td nowrap> element
                        datum = td_nowrap.get_text()

            pattern = r'\d{1,2}\.\s\w+\s\d{4}'
            match = re.search(pattern, datum)

            if match:
                date_str = match.group(0)  # Get the matched date string
                try: 
                    date_obj = datetime.strptime(date_str, "%d. %B %Y").date()  # Convert it to a date object
                except ValueError:
                    pass
            
            target_date = date.today() - timedelta(days=7)
            
            if link and date_obj > target_date:

            # if link and "decembar 2023" in datum:
                href = link.get('href')
                description = link.get_text()
                print("Proveravam: ", description)
                if href and description:
                    mojalista_zakona = lista_zakona()
                    # samo relevantni zakoni
                    
                    for zakon in mojalista_zakona:
                        if zakon.lower() in description.lower():
                            link = "http://www.parlament.gov.rs" + href.replace(" ", "%20")
                            print(" ")
                            print("------------------------------------------------------------------------------------------------")
                            print("Obradjujem: ", description)
                            print("------------------------------------------------------------------------------------------------")
                            print(" ")
                            # Perform your desired action with the matching link
                            ime_fajla = dl_parlament(link)
                            suma = sumiraj_zakone(ime_fajla, description)
                            izvestaj += f"Sa sajta {url} sumiram zakon sa linka {link} \n\n Evo i krakog pregleda zakona: \n\n {suma} \n\n"

        return izvestaj




    
# prima ceo tekst maila, sa sve linkovima i sa sezecima
def main():

    print("Ver 01.11.23 - local")
    print("Prikupljam zakone")
    text_maila = procitaj_parlament()
    if len(text_maila ) > 3:
        uputstvo = f"""
        Create a draft email to vladimir.siska@positive.rs with a subject Novi Zakoni. Do not send it. Tekst maila mora da bude tačno ovakav bez ikakvih promena: 
                    
        Evo izveštaja o novim zakonima: 

            {text_maila} 
                        
        Srdačan pozdrav,             
        """             
               
        print(" ")
        print("------------------------------------------------------------------------------------------------")
        print(" ")
        print("ZAVRSENA OBRADA, SALJEM MAIL")
        print(" ")
        print("------------------------------------------------------------------------------------------------")
        posalji_mail(uputstvo)
        print(" ")
        print("------------------------------------------------------------------------------------------------")
        print(" ")
        print("POSLAT MAIL")
        print(" ")
        print("------------------------------------------------------------------------------------------------")
    else:

        print("NEMA NOVIH ZAKONA")
            
if __name__ == "__main__":
    main()
