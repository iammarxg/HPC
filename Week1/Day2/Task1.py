from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.5,
    )
)

print("\n---------- The HPC Chatbot ----------\n")
print("Powered by Gemini 3.1 Flash Lite")
print("To exit the session, please type \"quit\"")
print("Start chatting!")
print("\n-------------------------------------\n")

while True:
    user = input("\nYou: ")

    if user.strip().lower() == "quit":
        print("\nExiting the session...")
        break

    try:
        response = chat.send_message(user)
        print(f"\nHPC Chatbot: {response.text}")
    except Exception as e:
        error_str = str(e)

        if "429" and "RESOURCE_EXHAUSTED" in error_str:
            print("\n\nError: You have exceeded your quota limit. Please, try again in 1 minute.")
        elif "503" in error_str:
            print("\n\nError: Server side error. Please check Gemini API Status and try again later.")
        else:
            print(f"\n\nUnhandled Error: {e}")