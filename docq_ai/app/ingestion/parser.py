import re
import logging

#logger object
logger = logging.getLogger(__name__)

#cleaning rules for the tes file
PAGE_PATTERN = re.compile(r"Page \d+ of \d+")
MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
HEADER = """CM 1606: Computational Mathematics
(Sem 02: Prob. & Stat.)"""

def clean_pages(pages: list[dict]) -> list[dict]:
    try:
        #Text Error handling
        if not isinstance(pages,list):
            raise TypeError(
                f"Expected List, got {type(pages).__name__}"
            )
        cleaned_pages = []
        for page in pages:

            if not isinstance(page, dict):
                raise TypeError(
                    "Each page must be a dictionary."
                )

            page_number = page["page"]
            text = page["text"]

            if not isinstance(text, str):
                raise TypeError(
                    f"Page {page_number} does not contain valid text."
                )

            original_length = len(text)

            text = text.replace(HEADER, "")
            text = PAGE_PATTERN.sub("", text)
            text = MULTIPLE_NEWLINES.sub("\n\n", text)
            text = text.strip()

            cleaned_pages.append({
                "page": page_number,
                "text": text
            })

            logger.debug(
                f"Page {page_number}: "
                f"{original_length} -> {len(text)} characters"
            )

        logger.info(
            f"Successfully cleaned {len(cleaned_pages)} pages."
        )

        return cleaned_pages
    except Exception:
        logger.exception("Failed to clean extracted pages.")
        raise