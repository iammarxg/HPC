from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        max_output_tokens=100,
        temperature=0.5,
    )
)

prompt_1 = "Explain Saudi Arabia in 10 words."
print(f"You: {prompt_1}")

response_1 = chat.send_message(prompt_1)
print(f"Gemini: {response_1.text}\n")

prompt_2 = "What is the capital ?"
print(f"You: {prompt_2}")

response_2 = chat.send_message(prompt_2)
print(f"Gemini: {response_2.text}\n")