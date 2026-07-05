from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="What is Saudi Arabia",
    config=types.GenerateContentConfig(
        max_output_tokens=100,
        temperature=0.5,
    )
)

print(response.text)