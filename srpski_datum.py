from datetime import datetime

def parse_serbian_date(date_string):
    serbian_month_names = {
        "januar": "January",
        "februar": "February",
        "mart": "March",
        "april": "April",
        "maj": "May",
        "jun": "June",
        "jul": "July",
        "avgust": "August",
        "septembar": "September",
        "oktobar": "October",
        "novembar": "November",
        "decembar": "December"
    }

    date_string = date_string.lower()

    for serbian_month, english_month in serbian_month_names.items():
        date_string = date_string.replace(serbian_month, english_month)

    date_string = date_string.strip()

    date_obj = datetime.strptime(date_string, "%d. %B %Y")
    return date_obj

def convert_input_to_date(ulazni_datum):
    try:
        date_obj = datetime.strptime(ulazni_datum, "%d.%m.%Y.")
        return date_obj
    except ValueError:
        print("Invalid date format. Please enter a date in the format 'dd.mm.yyyy.'")
        return None

def main():
    ulazni_datum = input("Enter a date in the format 'dd.mm.yyyy.' to compare: ")
    date_obj = convert_input_to_date(ulazni_datum)

    if date_obj:
        serbian_date_string = "6. septembar 2023"  # Ovde se preuzima datum sa sajta
        parsed_serbian_date = parse_serbian_date(serbian_date_string)

        print("Datum sa sajta:", serbian_date_string)

        if parsed_serbian_date > date_obj:
            print("Datum sa sajta je u buducnosti...")
        elif parsed_serbian_date == date_obj:
            print("Datum sa sajta je danas!")
        else:
            print("Datum sa sajta je u proslosti...")

if __name__ == "__main__":
    main()
