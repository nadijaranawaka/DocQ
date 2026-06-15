import re
import logging

#logger object
logger = logging.getLogger(__name__)

def clean_text(text: str):

    #Text Error handling
    if not isinstance(text,str):
        raise TypeError(
            f"Expecterd Type String, got {type(text).__name__}"
        )
    if not text.strip():
        return ""
    
    #Clean the headers
    text = text.replace(
        """CM 1606: Computational Mathematics
(Sem 02: Prob. & Stat.)""",""
    )

    #Clean the page numbers
    text = re.sub(r"Page \d+ of \d+","",text)

    #Clean accidental newlines
    text = re.sub(r"\n{3,}","\n\n",text)

    logger.info("Text Cleaned")
    return text.strip()