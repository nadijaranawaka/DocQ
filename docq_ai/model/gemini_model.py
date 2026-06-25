from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import logging

#logger object
logger = logging.getLogger(__name__)

load_dotenv()

class GeminiModel:
    def __init__(self,modelName,temperature):
        API_KEY = os.getenv("GEM_API_KEY")
        if not API_KEY:
            raise ValueError("API KEY not found")

        self.client = genai.Client(
            api_key=API_KEY
        )
        if not modelName:
            raise ValueError(
                "Model name cannot be empty"
            )
        if not 0 <= temperature <= 2:
            raise ValueError(
                "Temperature must be between 0 and 2"
            )
        self.model = modelName
        self.temperature = temperature
        logger.info(f"Gemini Initialization Complete with model={modelName}")
    
    #Later on have a default system prompt for this section
    def generate(self,prompt:str,systemprompt:str = "") -> str:
        if not isinstance(prompt, str):
            raise TypeError(
                f"Expected str, got {type(prompt).__name__}"
            )
        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty"
            )
        if not isinstance(systemprompt, str):
            raise TypeError(
                "System prompt must be a string"
            )
        logger.info(f"Sending prompt length of {len(prompt)}")
        try:
            response = self.client.models.generate_content(
                model = self.model,
                contents = prompt,
                config = types.GenerateContentConfig(
                    temperature = self.temperature,
                    system_instruction=systemprompt
                )
            )
        except Exception:
            logger.exception("Gemini requests failed")
            raise
        logger.info(f"Received Response of length {len(response.text)}")
        if not response.text:
            raise ValueError("Gemini returned an empty String")
        return response.text