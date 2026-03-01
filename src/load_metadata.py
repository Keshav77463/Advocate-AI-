from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from metadata_cleaning import clean_bns_metadata

# Constants
OUTPUT_DIR = r"C:\Users\Keshav Sachdeva\PycharmProjects\Advocate-AI-\data"
SECTIONS = 358
MAX_THREADS = 10


def fetch_metadata(section):
    try:
        url = f"https://devgan.in/bns/section/{section}/"
        doc = WebBaseLoader(url).load()[0]
        cleaned_metadata = clean_bns_metadata(doc.metadata, section)
        return cleaned_metadata, f"✅ Section {section} metadata collected."
    except Exception as e:
        return None, f"❌ Section {section} failed: {e}"


# Run in parallel
all_metadata = []
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(fetch_metadata, sec): sec for sec in range(1, SECTIONS + 1)}
    for future in as_completed(futures):
        metadata, message = future.result()
        print(message)
        if metadata:
            all_metadata.append(metadata)

df = pd.DataFrame(all_metadata).sort_values("section").reset_index(drop=True)
df = df.drop(columns=['source', 'language'], errors='ignore')  # errors='ignore' won't crash if columns are missing
df.to_csv(os.path.join(OUTPUT_DIR, "bns_metadata.csv"), index=False, encoding="utf-8")
print("\n✅ Metadata saved!")
print(df.head())