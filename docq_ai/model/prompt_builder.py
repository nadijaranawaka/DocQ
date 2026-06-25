import logging
logger = logging.getLogger(__name__)

def build_prompt(question:str, chunks:list[str]) -> str:
    try:
        #validation
        if not isinstance(question, str):
            raise TypeError(
                f"Expected question to be str, got {type(question).__name__}"
            )
        if not question.strip():
            raise ValueError(
                "Question cannot be empty"
        )
        if not isinstance(chunks, list):
            raise TypeError(
                "Chunks must be a list"
            )
        if not chunks:
            raise ValueError(
                "No chunks provided"
            )
        if not all(isinstance(chunk, str) for chunk in chunks):
            raise TypeError(
                "All chunks must be strings"
            )
        # Need more prompt engineering
        context = "\n\n".join(chunks)
        logger.info(f"Context length: {len(context)} characters")
        logger.info(f"Building prompt using {len(chunks)} chunks")

        prompt = f"""
        Answer the following question using ONLY the provided context,

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        return prompt
    except Exception:
        logger.exception("Prompt building failed")
        raise