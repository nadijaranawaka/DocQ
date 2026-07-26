from collections import Counter

def get_start_line(pages:list[dict]) -> list:
    starts = []

    for page in pages:
        lines = page["text"].split("\n")
        for line in lines:
            line.strip()

            if line:
                starts.append(line)
                break
    
    return starts

def find_headers(pages,threshold=0.7):
    if not pages:
        raise ValueError("No pages provided")
    starts = get_start_line(pages)
    counts = Counter(starts)
    headers = []

    for line,count in counts.items():
        frequency = count / len(pages)
        if  frequency >= threshold:
            headers.append(line)
    return headers

def remove_headers(pages, headers):
    cleaned_pages = []
    for page in pages:
        lines = page["text"].split("\n")
        lines = [
            line 
            for line in lines 
            if line.strip() not in headers
        ]
        cleaned_pages.append({
            "page": page["page"],
            "text": "\n".join(lines)
        })
    return cleaned_pages