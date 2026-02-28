import requests
import re
from bs4 import BeautifulSoup

url = "https://devgan.in/bns/section/18/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text,"html.parser")

# Extract visible text
text = soup.get_text(separator=" ", strip=True)

text = re.sub(r"No Javascript.*?Reload this page!", "", text)
text = re.sub(r"HomePrevIndexNextMessages", "", text)
text = re.sub(r"TopPrevIndexNext", "", text)
text = re.sub(r"©.*", "", text)
text = re.sub(r"Updated:.*?\d{4}", "", text)
text = re.sub(r"\s+", " ", text).strip()

print("Cleaned Text:\n")
print(text)