from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

print("----BASIC PROMPT----\n")

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Write a bash script to backup a folder.",
    config=types.GenerateContentConfig(
        max_output_tokens=10000000,
        temperature=0.5,
    )
)

print(response.text)

print("\n\n----IMPROVED PROMPT----\n")

response2 = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Write a bash script that takes a source folder as input and creates a compressed tar backup of it in a destination folder, appending the current date to the filename.",
    config=types.GenerateContentConfig(
        max_output_tokens=10000000,
        temperature=0.5,
    )
)

print(response2.text)

print("\n\n----DETAILED PROMPT----\n")

response3 = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="You are a DevOps engineer creating an automated backup solution. Write a bash script that accepts three command-line arguments: a source directory, a destination directory, and the maximum number of old backups to retain. Include error handling to check if the source exists before running, and add comments explaining the logic for deleting older backups.",
    config=types.GenerateContentConfig(
        max_output_tokens=10000000,
        temperature=0.5,
    )
)

print(response3.text)

print("\n\n----CREATIVE PROMPT----\n")

response4 = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Act as a strict system administrator designing a secure compliance backup utility. Write a bash script that creates a rotating tar backup of a source folder to a destination folder, keeping a specified number of old backups. The script must also generate a SHA-256 checksum of the newly created archive for integrity verification and append a timestamped record of the operation, including the checksum and backup size, to a log file.",
    config=types.GenerateContentConfig(
        max_output_tokens=10000000,
        temperature=0.5,
    )
)

print(response4.text)

print("\n\n----CLEAR CONSTRAINTS PROMPT----\n")

response5 = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Write a bash script that backs up a source directory to a destination, manages a retention policy for old backups, generates a SHA-256 checksum, and writes to a log file. You must adhere to the following constraints: The script must accept exactly three arguments (source, destination, retention limit). Use only standard GNU utilities. If the source directory is missing, the script must exit immediately with code 1. Limit your text explanation outside the code block to exactly three bullet points.",
    config=types.GenerateContentConfig(
        max_output_tokens=10000000,
        temperature=0.5,
    )
)

print(response5.text)