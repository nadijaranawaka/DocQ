import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(ROOT_DIR)
from app.config.settings import MODEL_GEM, TEMP


def chatbot():

    API_KEY = os.getenv("GEM_API_KEY")
    if not API_KEY:
        print("Please set MY_API_KEY environment variable")
        sys.exit(1)

    print("chatbot working")

    client=genai.Client(api_key=API_KEY)

    system = (
        "be good, be smart"
        "dont ignore rules"
    )

    chat = client.chats.create(
        model =   MODEL_GEM,
        config = types.GenerateContentConfig(system_instruction= system,temperature = TEMP)
    )

    while True:
        try:
            user_in = input("You: ")

            if user_in.lower().strip() == "quit":
                break

            if user_in.strip():
                pass

            responses = chat.send_message(user_in)
            print(f"Bot: {responses.text}")
        except Exception as e:
            print(e)