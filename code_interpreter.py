from langchain.llms import OpenAI
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
# Create an instance of the OpenAI code interpreter
code_interpreter = OpenAI()

# Define the code to be executed
code = """
x = 5
y = 10
z = x + y
z
"""

# Execute the code using the code interpreter
result = code_interpreter.execute(code)

# Print the result
print(result)