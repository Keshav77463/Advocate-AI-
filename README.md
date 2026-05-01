# Advocate AI 🏛️⚖️

> An AI-powered legal research and advocacy assistant that scrapes, cleans, and indexes legal data to enable intelligent semantic search and Q&A.

---

## Overview

**Advocate AI** is an end-to-end RAG (Retrieval-Augmented Generation) pipeline designed to help users query legal information — particularly BNS (Bharatiya Nyaya Sanhita) data — through natural language. It combines web scraping, metadata enrichment, vector embeddings, and a conversational interface to make legal research accessible and fast.

---

## Features

- 🌐 **Web Scraping** — Automated scraping of legal documents and case data
- 🧹 **Data Cleaning** — Multi-stage preprocessing and normalization of raw legal text
- 🏷️ **Metadata Management** — Parallel BNS metadata scraping with CSV export
- 🧠 **Vector Indexing** — Dense embeddings ingested into Qdrant for semantic search
- 💬 **Conversational Interface** — Streamlit-based app for asking legal questions in plain English

---

## Project Structure


Advocate-AI-/
├── notebook/               # Jupyter notebooks for exploration & prototyping
├── src/
│   ├── app.py              # Main Streamlit application (entry point)
│   ├── data_cleaning.py    # Text preprocessing and normalization
│   ├── ingest_qdrant.py    # Embeds chunks and indexes them into Qdrant
│   ├── load_metadata.py    # Parallel BNS metadata scraper with CSV export
│   ├── metadata_cleaning.py # Cleans and standardizes BNS metadata
│   └── web_scraping.py     # Web scraper for legal data collection
├── .gitignore
├── LICENSE
└── README.md


---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Vector Database | [Qdrant](https://qdrant.tech/) |
| Embeddings | Dense vector embeddings (e.g., sentence-transformers) |
| Frontend | Streamlit |
| Data Collection | BeautifulSoup / Requests |
| Storage | CSV / Qdrant collections |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Qdrant running locally or via Qdrant Cloud
- Required Python packages (see below)

### Installation

```bash
# Clone the repository
git clone https://github.com/Keshav77463/Advocate-AI-.git
cd Advocate-AI-

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set up your environment variables (create a `.env` file):

```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here        # If using Qdrant Cloud
COLLECTION_NAME=advocate_ai
```

---

## Usage

### Step 1 — Scrape Data

```bash
python src/web_scraping.py
```

Scrapes legal content from configured sources and saves raw data locally.

### Step 2 — Clean & Process Data

```bash
python src/data_cleaning.py
python src/metadata_cleaning.py
```

Normalizes raw text and cleans BNS metadata.

### Step 3 — Load Metadata

```bash
python src/load_metadata.py
```

Runs parallel BNS metadata scraping and exports results to CSV.

### Step 4 — Ingest into Qdrant

```bash
python src/ingest_qdrant.py
```

Generates dense embeddings for text chunks and indexes them into Qdrant for semantic search.

### Step 5 — Launch the App

```bash
streamlit run src/app.py
```

Opens the Advocate AI chat interface in your browser.



## How It Works


Web Sources
    │
    ▼
web_scraping.py  ──►  Raw HTML/Text
    │
    ▼
data_cleaning.py  ──►  Clean Text Chunks
    │
    ▼
ingest_qdrant.py  ──►  Embeddings → Qdrant Vector DB
                                          │
                              User Query ─┘
                                          │
                                          ▼
                                    Semantic Search
                                          │
                                          ▼
                                  LLM-Augmented Answer
                                          │
                                          ▼
                                      app.py (UI)
```



## Use Cases

- 🔍 Search BNS (Bharatiya Nyaya Sanhita) sections by natural language
- ⚖️ Understand legal provisions without reading dense statutory text
- 📋 Research relevant case law and legal metadata quickly
- 🤖 Get AI-generated summaries and explanations of legal content



## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request



## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.

---

## Author

**Keshav77463** — [GitHub Profile](https://github.com/Keshav77463)

---

> *Making legal knowledge accessible through AI.*
