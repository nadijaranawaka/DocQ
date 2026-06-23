from model.gemini_model import GeminiModel
from app.config.settings import MODEL_GEM,TEMP
from app.retrieval.retrieval import search_doc
from model.prompt_builder import build_prompt


gemini = GeminiModel(MODEL_GEM,TEMP)

class Pipeline:
    def ask_docq(self,question):
        results = search_doc(question)
        chunks = results['documents'][0]
        prompt = build_prompt(question=question,chunks=chunks)
        answer = gemini.get_response(prompt=prompt)
        return answer