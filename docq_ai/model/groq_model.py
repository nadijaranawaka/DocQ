import os
import logging
from groq import Groq
from dotenv import load_dotenv

logger = logging.getLogger("docq")
load_dotenv()


class GroqModel:

    def __init__(self, modelName, temperature):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found")

        if not modelName:
            raise ValueError("Model name cannot be empty")

        if not 0 <= temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")

        self.client = Groq(api_key=api_key, max_retries=2)
        self.model = modelName
        self.temperature = temperature

        logger.info(f"Groq initialization complete with model={modelName}")

    def _generate_response(self, prompt: str, systemprompt: str = ""):

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        messages = []

        if systemprompt.strip():
            messages.append({
                "role": "system",
                "content": systemprompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )

        if not response.choices:
            raise ValueError("Groq returned no response choices")

        if not response.choices[0].message.content:
            raise ValueError("Groq returned an empty response")

        return response

    def generate(self, prompt: str, systemprompt: str = "") -> str:

        response = self._generate_response(prompt, systemprompt)

        return response.choices[0].message.content

    def generate_with_usage(self, prompt: str, systemprompt: str = "") -> dict:

        response = self._generate_response(prompt, systemprompt)

        usage = response.usage

        return {
            "answer": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": usage.prompt_tokens or 0,
                "completion_tokens": usage.completion_tokens or 0,
                "total_tokens": usage.total_tokens or 0
            }
        }