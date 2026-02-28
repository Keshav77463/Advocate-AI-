import requests
from bs4 import BeautifulSoup
from data_cleaning import clean_bns_page_content
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
OUTPUT_DIR = r"C:\Users\Keshav Sachdeva\PycharmProjects\Advocate-AI-\data"
SECTIONS = 358
MAX_THREADS = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create folder if it doesn't exist


def fetch_bns_section(section: int) -> str:
    url = f"https://devgan.in/bns/section/{section}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", {"id": "main"}) or soup.find("div", {"class": "content"})

    return content_div.get_text(separator="\n") if content_div else soup.get_text(separator="\n")


def process_section(section):
    try:
        raw_text = fetch_bns_section(section)

        if len(raw_text.strip()) < 50:
            return f"⚠️ Section {section} raw content too short: {repr(raw_text[:100])}"

        cleaned_text = clean_bns_page_content(raw_text)

        if len(cleaned_text.strip()) < 20:
            return f"⚠️ Section {section} cleaned to near-empty. Check regexes."

        file_path = os.path.join(OUTPUT_DIR, f"bns_section_{section}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        return f"✅ Section {section} saved ({len(cleaned_text)} chars)."
    except Exception as e:
        return f"❌ Section {section} failed: {e}"


# Run in parallel
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(process_section, sec): sec for sec in range(1, SECTIONS + 1)}
    for future in as_completed(futures):
        print(future.result())