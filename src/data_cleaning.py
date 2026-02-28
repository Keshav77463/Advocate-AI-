import re
def clean_bns_page_content(text: str) -> str:
    # Remove navigation noise
    text = re.sub(r'(Top|Prev|Index|Next)\s*', '', text)
    text = re.sub(r'No Javascript.*?Reload this page!', '', text, flags=re.DOTALL)

    # Remove footer/attribution
    text = re.sub(r'©.*', '', text, flags=re.DOTALL)
    text = re.sub(r'(By Raman Devgan|Devgan\.in|Bharatiya Nyaya Sanhita Home)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Updated:.*?\d{4}', '', text)

    # Normalize whitespace LAST
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()

    return text