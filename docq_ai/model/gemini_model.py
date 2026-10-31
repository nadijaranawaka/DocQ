from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import logging
from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_attempt,
    retry_if_exception_type,
    before_sleep_log
)

#logger object
logger = logging.getLogger("docq")

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
    @retry(
    retry=retry_if_exception_type(Exception),
    wait=wait_random_exponential(min=2, max=15),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
    def _generate_response(self, prompt: str, systemprompt: str = ""):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if not isinstance(systemprompt, str):
            raise TypeError("System prompt must be a string")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                system_instruction=systemprompt
            )
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response")

        return response


    def generate(self, prompt: str, systemprompt: str = "") -> str:
        response = self._generate_response(prompt, systemprompt)
        return response.text


    def generate_with_usage(self, prompt: str, systemprompt: str = "") -> dict:
        response = self._generate_response(prompt, systemprompt)

        usage = response.usage_metadata

        return {
            "answer": response.text,
            "usage": {
                "prompt_tokens": usage.prompt_token_count or 0,
                "completion_tokens": usage.candidates_token_count or 0,
                "total_tokens": usage.total_token_count or 0
            }
        }   