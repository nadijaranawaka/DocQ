from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiModel:
    def __init__(self,modelName,temperature):
        API_KEY = os.getenv("GEM_API_KEY")
        if not API_KEY:
            raise ValueError("API KEY not found")

        self.client = genai.Client(
            api_key=API_KEY
        )
        self.model = modelName
        self.temperature = temperature
    
    #Later on have a default system prompt for this section
    def get_response(self,prompt,systemprompt=""):
        response = self.client.models.generate_content(
            model = self.model,
            contents = prompt,
            config = types.GenerateContentConfig(
                temperature = self.temperature,
                system_instruction=systemprompt
            )
        )
        return response.text



# def get_response(userQ):
    # API_KEY = os.getenv("GEM_API_KEY")
    # if not API_KEY:
    #     print("Please set MY_API_KEY environment variable")
    #     sys.exit(1)
    # print("chatbot working")
    # client=genai.Client(api_key=API_KEY)
    # #needs work
    # system = (
    #     "be good, be smart"
    #     "dont ignore rules"
    # )
    # chat = client.chats.create(
    #     model =   MODEL_GEM,
    #     config = types.GenerateContentConfig(system_instruction= system,temperature = TEMP)
    # )

    # while True:
    #     try:
    #         user_in = input("You: ")

    #         if user_in.lower().strip() == "quit":
    #             break

    #         if user_in.strip():
    #             pass

    #         responses = chat.send_message(user_in)
    #         print(f"Bot: {responses.text}")
    #     except Exception as e:
    #         print(e)

