# AI Asistent Pravnik - Pracenje zakona
import streamlit as st
from requests import get
from bs4 import BeautifulSoup
from pravnik_fukncije import dl_paragraf, dl_parlament, lista_zakona, sumiraj_zakone
from myfunc.mojafunkcija import positive_login
import os
from datetime import date
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# prikuplja podatke o zakonima sa sajtova i salje mail obavestenja sa linkovima na izmene i dopune zakona
#	https://www.paragraf.rs/izmene_i_dopune/
#	http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html  


def posalji_mail(uputstvo):
    def send_email(subject, message, from_addr, to_addr, smtp_server, smtp_port, username, password):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()

    send_email(
        subject=f"Izveštaj o novim zakonima - {date.today()}",
        message=uputstvo,
        from_addr="nemanja.perunicic@positive.rs",
        to_addr="nemanja.perunicic@positive.rs",
        smtp_server="smtp.office365.com",
        smtp_port=587,
        username="nemanja.perunicic@positive.rs",
        password="CrimsonRed_1"
        )
    

# skida zakone sa sajta paragraf.rs
def procitaj_paragraf():
    # URL of the webpage to scrape
    url = 'https://www.paragraf.rs/izmene_i_dopune/'  
    suma = ""
    # Send a GET request to the webpage
    response = get(url)
    
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
                        
                                link = "https://www.paragraf.rs/izmene_i_dopune/" + href.replace(" ", "%20")
                                full_text = dl_paragraf(link)
                                suma = sumiraj_zakone(full_text, description)
                                izvestaj = f"Sa sajta {url} sumiram zakon sa linka {link} \n\n Evo i krakog pregleda zakona {description}: \n\n {suma} \n\n" 
                                return izvestaj
                             

# skida zakone sa sajta parlament.gov.rs                                                                                                                         
def procitaj_parlament():
    
    # URL of the webpage you want to scrape
    url = 'http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html' 
    suma = ""
    # Send a GET request to the webpage
    response = get(url)

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
            datum = tr.get_text()  # Assuming the date is in the <tr> element text
            
            # ovde cemo prvo da konvertujemo datum u date format i onda da proverimo da li je today()-2
            # datum_zakona = parse_serbian_date(datum) # mora da se pretvori format datuma i izvadi iz strringa koji sadrzi svasta
            #if link and datum_zakona >= date.today()-2:

            if link and "oktobar 2023" in datum:
                href = link.get('href')
                description = link.get_text()

                if href and description:
                    mojalista_zakona = lista_zakona()
                    # samo relevantni zakoni
                    
                    for zakon in mojalista_zakona:
                        if zakon.lower() in description.lower():
                            link = "http://www.parlament.gov.rs" + href.replace(" ", "%20")

                            # Perform your desired action with the matching link
                            ime_fajla = dl_parlament(link)
                            suma = sumiraj_zakone(ime_fajla, description)
                            izvestaj += f"Sa sajta {url} sumiram zakon sa linka {link} \n\n Evo i krakog pregleda zakona: \n\n {suma} \n\n"

        return izvestaj




    
# prima ceo tekst maila, sa sve linkovima i sa sezecima
def main():

    st.title("AI Asistent Pravnik - Praćenje zakona")
    st.caption("Ver 31.10.23")
    with st.expander("Pročitajte uputstvo:", expanded=True):
            st.caption(
                """
                    Program prikuplja nove zakone ili izmene zakona sa sajtova Paragraf i Parlament, a iz liste zakona koji su objavljeni u željenom periodu i pripadaju listi zakona od interesa radi sažetak. Zatim linkove sa zakonima i sažetke šalje na email po izboru.
                    Tehničko pitanje: Da se email šalje sa positive.rs naloga tj da se koristi Outlook i office365
                    Za kasnije: Kako postaviti filtere i cron job?
                    """
            )
    with st.form("mail_form"):
        
        placeholder = st.empty()
        submit_button = st.form_submit_button(label='Počni program')        

        # Every form must have a submit button.
        suma_parlament = ""
        if submit_button:
            with st.spinner("Obradjujem ..."):
                 with placeholder:
                    st.info("Prikupljam zakone")
                    text_maila = procitaj_parlament()
                    if len(text_maila ) > 3:
                        uputstvo = f"""
Poštovani,
Evo izveštaja o novim zakonima: 

{text_maila} 
                        
Srdačan pozdrav,             
"""             
               
                        st.info("Šaljem mail")    
                        posalji_mail(uputstvo)
                        # st.write (text_maila)
                        st.success("Poslat email, obrada je završena")
                    else:
                        st.error("Nema novih zakona")
            
# Deployment on Stremalit Login functionality
deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")

if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main, " ")
else:
    if __name__ == "__main__":
        main()
