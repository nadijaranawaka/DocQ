import logging
from app.config.cleaning_rules import PAGE_NUMBER_PATTERNS,MULTIPLE_NEWLINES,MULTIPLE_SPACES,CONTROL_CHARACTERS,REPEATED_SYMBOLS,JOINED_WORDS,BULLET_PATTERN

#logger object
logger = logging.getLogger(__name__)

#cleaning rules for the tes file
# PAGE_PATTERN = re.compile(r"Page \d+ of \d+")
# MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
# HEADER = """CM 1606: Computational Mathematics
# (Sem 02: Prob. & Stat.)"""


# Cleaning Functions
def remove_page_numbers(text:str) -> str:
    for pattern in PAGE_NUMBER_PATTERNS:
        text = pattern.sub("",text)
    return text

def normalize_spaces(text:str) -> str:
    return MULTIPLE_SPACES.sub(" ",text)

def normalize_newlines(text:str) -> str:
    return MULTIPLE_NEWLINES.sub("\n\n",text)

def remove_control_characters(text:str) -> str:
    return CONTROL_CHARACTERS.sub("",text)

def remove_repeated_symbols(text:str)->str:
    return REPEATED_SYMBOLS.sub("", text)

def fix_joined_words(text:str) -> str:
    return JOINED_WORDS.sub(r"\1 \2", text)

def normalize_bullets(text:str)->str:
    return BULLET_PATTERN.sub("• ", text)

def trim_text(text:str) -> str:
    return text.strip()

# Cleaning Pipeline
CLEANING_PIPELINE = [
                remove_page_numbers,
                normalize_newlines,
                normalize_spaces,
                remove_control_characters,
                remove_repeated_symbols,
                fix_joined_words,
                normalize_bullets,
                trim_text
            ]

# Validation
def validate_document(pages:list[dict]) -> None:
    if not isinstance(pages,list):
        raise TypeError(
            f"Expected List, got {type(pages).__name__}"
        )
    if not pages:
        raise ValueError("Document contains no pages.")
    
def validate_page(page:dict) -> None:
    if not isinstance(page, dict):
        raise TypeError(
            "Each page must be a dictionary."
        )
    if "page" not in page:
        raise KeyError("Missing 'page' key")

    if "text" not in page:
        raise KeyError("Missing 'text' key")

    if not isinstance(page["text"], str):
        raise TypeError(
            f"Page {page['page']} does not contain valid text."
        )


# Main function
def clean_pages(pages: list[dict]) -> list[dict]:
    try:
        cleaned_pages = []
        validate_document(pages)
        for page in pages:
            validate_page(page)
            page_number = page["page"]
            text = page["text"]
            original_length = len(text)

            for cleaner in CLEANING_PIPELINE:
                text = cleaner(text)

            cleaned_pages.append({
                "page": page_number,
                "text": text
            })

            logger.debug(
                f"Page {page_number}: "
                f"{original_length} -> {len(text)} characters"
            )

        logger.info(
            "Successfully cleaned %d pages.",
            len(cleaned_pages)
        )

        return cleaned_pages
    except Exception:
        logger.exception("Failed to clean extracted pages.")
        raise