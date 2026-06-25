import re
import logging

#logger object
logger = logging.getLogger(__name__)
PAGE_PATTERN = re.compile(r"Page \d+ of \d+")

def clean_text(text: str) -> str:
    try:
        #Text Error handling
        if not isinstance(text,str):
            raise TypeError(
                f"Expected Type String, got {type(text).__name__}"
            )
        if not text.strip():
            raise ValueError("Input text is empty")
        original_len = len(text)
        #Clean the headers
        #move this into a config file named cleaning rules
        text = text.replace(
            """CM 1606: Computational Mathematics
    (Sem 02: Prob. & Stat.)""",""
        )

        #Clean the page numbers
        text = PAGE_PATTERN.sub("", text)

        #Clean accidental newlines
        text = re.sub(r"\n{3,}","\n\n",text)
        text = text.strip()
        cleaned_len = len(text)
        logger.info(f"Text Cleaned. Length: {original_len} -> {cleaned_len}")
        return text
    except Exception:
        logger.exception("Text Cleaning Failed")
        raise