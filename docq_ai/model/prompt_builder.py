import logging
logger = logging.getLogger(__name__)

def build_prompt(question:str, chunks:list) -> str:
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
        
        # Need more prompt engineering
        context = ""
        for ctx in chunks:
            context += f"""
            Source: {ctx["source"]}
            Page: {ctx["page"]}

            {ctx["text"]}

            -----------------------"""
            
        logger.info(f"Context length: {len(context)} characters")
        logger.info(f"Building prompt using {len(chunks)} chunks")

        prompt = f"""
        You are answering questions about a PDF.

        Each context section contains a Source and Page.

        Whenever you use information from a context section,
        cite the page at the end of the sentence like:

        (Page 3)

        If information comes from multiple pages, cite all of them:

        (Pages 3, 5)

        Only use the provided context.

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