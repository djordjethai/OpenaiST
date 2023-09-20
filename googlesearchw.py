from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
import pprint
import os

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

izbor = int(
    input("Enter 1 for GoogleSearchAPIWrapper or 2 for GoogleSerperAPIWrapper: ")
)
if izbor == 1:
    search = GoogleSearchAPIWrapper()
elif izbor == 2:
    search = GoogleSerperAPIWrapper()
mysearch = input("Enter your search query: ")
results = search.results(mysearch, num_results=3)

pprint.pp(results)
