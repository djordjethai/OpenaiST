import re
from datetime import date, datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, 'sr_RS.utf8')

pattern = r'\d{1,2}\.\s\w+\s\d{4}'
match = re.search(pattern, "26. novembar 2023.")
date_str = "01. Januar 2020."
if match:
    date_str = match.group(0)  # Get the matched date string
    try: 
        date_obj = datetime.strptime(date_str, "%d. %B %Y").date()  # Convert it to a date object
    except ValueError:
        pass
print(date_obj)
print(date.today())
