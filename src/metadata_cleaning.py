import re

def clean_bns_metadata(metadata: dict, section_number: int) -> dict:
    cleaned = metadata.copy()

    if 'title' in cleaned:
        cleaned['title'] = re.sub(r'\s*\|\s*Devgan\.in\s*$', '', cleaned['title']).strip()

    if 'description' in cleaned:
        cleaned['description'] = re.sub(r'from the Bharatiya Nyaya Sanhita, by Advocate Raman Devgan', '', cleaned['description'], flags=re.IGNORECASE).strip()
        cleaned['description'] = re.sub(r',\s*$', '', cleaned['description'])

    cleaned['section'] = section_number
    return cleaned