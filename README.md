# Google Search and Serper API Wrapper with Streamlit

This Python code is a simple application that allows users to perform web searches using either the Google Search API or the Google Serper API. It uses the Streamlit library for creating a user-friendly interface. Let's break down the key components and functionalities of this code:

## Import Statements

The code begins with import statements to bring in the necessary libraries and modules:

- `streamlit as st`: The Streamlit library is used for creating the user interface.
- `GoogleSearchAPIWrapper` and `GoogleSerperAPIWrapper`: These are utility modules for interfacing with the Google Search and Google Serper APIs, respectively.
- `os`: The `os` module is used for retrieving environment variables.

## Environment Variables

The code fetches three environment variables:

- `SERPER_API_KEY`: An API key required for using the Google Serper API.
- `GOOGLE_API_KEY`: An API key required for using the Google Search API.
- `GOOGLE_CSE_ID`: A custom search engine ID needed for custom Google searches.

## User Interface googlesearchw.py

The code creates a simple user interface using Streamlit:

- `st.radio`: This UI element allows users to choose between two methods: "Google Search" and "Google Serper."

- Depending on the user's choice, it assigns either the `GoogleSearchAPIWrapper` or `GoogleSerperAPIWrapper` to the `search` variable.

- `st.text_input`: This input field allows users to enter their search query.

## Performing the Search

The code performs the web search when the user enters a search query:

- If the user provides a search query (`mysearch` is not empty), it calls the `results` method on the `search` object to perform the search and retrieve results.

- The code specifies `num_results=3`, which indicates that it wants to retrieve three search results.

- The search results are displayed using `st.write`.

In summary, this code creates a straightforward web search application using Streamlit, allowing users to choose between Google Search and Google Serper as the search method. Users can enter search queries, and the code fetches and displays the search results based on their choice. It relies on environment variables for API keys and a custom search engine ID.

## Streamlit Application with Data Visualization

This Python code is a Streamlit application that creates a user interface for visualizing data and providing user instructions. It utilizes several Streamlit components and functions to achieve this. Let's break down the key components and functionalities of this code:

## Import Statements uputstvo.py

The code begins with import statements to bring in the necessary libraries and modules:

- `streamlit as st`: The Streamlit library is used for creating the user interface.
- `pandas as pd` and `numpy as np`: These libraries are used for data manipulation and generation.
  
## Data Generation

The code generates random data for demonstration purposes. It creates a DataFrame named `chart_data` with 20 rows and 3 columns ("a," "b," and "c"). This DataFrame is used for generating charts later in the code.

## User Interface uputstvo.py

The user interface is constructed using Streamlit components:

- `st.title`: Sets the title of the application.
- `st.subheader`: Adds a subheading.
- `st.columns`: Splits the interface into two columns (`col1` and `col2`) to display different content side by side.
  
### Column 1 (`col1`)

- `with st.expander`: An expander widget that can be clicked to reveal more content. It contains various Streamlit components:
  - `st.write`: Displays text.
  - `st.info`, `st.success`, `st.warning`, `st.error`: Displays different types of informative messages.
  - `st.image`: Embeds an image.
  - `st.video`: Embeds a video.
  - `st.markdown`: Renders markdown-formatted text.
  - `st.latex`: Renders LaTeX equations.
  
- `st.map`: Displays a map with markers based on latitude and longitude data from a DataFrame.

### Column 2 (`col2`)

- `st.date_input`, `st.time_input`, `st.color_picker`, `st.json`: These components allow users to input a date, time, color, and JSON data, respectively.
- `st.caption`: Adds a caption to describe the purpose of a table.
- `st.data_editor`: Displays an editable table for data input.

## Data Visualization

- `st.divider`: Adds a visual divider between sections.
- `st.bar_chart`, `st.line_chart`, `st.area_chart`: These functions generate and display bar, line, and area charts based on the `chart_data` DataFrame.

In summary, this code creates a Streamlit application with a user-friendly interface that allows users to visualize data using various charts and provides user instructions through text, messages, images, videos, and editable tables. It's a versatile tool for data exploration and communication.

## License MIT
