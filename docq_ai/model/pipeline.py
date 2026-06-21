from model.gemini_model import GeminiModel
from app.config.settings import MODEL_GEM,TEMP

gemini = GeminiModel(MODEL_GEM,TEMP)

response = gemini.get_response("Hello")
print(response)