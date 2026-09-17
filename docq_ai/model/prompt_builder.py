import logging
logger = logging.getLogger("docq")

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
    
def build_summary_prompt(text: str) -> str:
    try:
        if not isinstance(text, str):
            raise TypeError(
                f"Expected text to be str, got {type(text).__name__}"
            )

        if not text.strip():
            raise ValueError("Text cannot be empty")

        prompt = f"""
        You are summarizing a PDF document.
        Start the summary with the line : 'This document is about'
        End the summary with the line : 'This is a simple summary of the document'

        Create a short summary that explains:
        - what the document is about
        - its main topics
        - the main purpose or focus of the document

        Keep the summary concise and factual.
        Do not add information that is not present in the text.

        Document text:
        {text}

        Summary:
        """

        return prompt

    except Exception:
        logger.exception("Summary prompt building failed")
        raise