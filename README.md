# FrontierAtlas — AI Intelligence Ingestion Pipeline

An asynchronous, high-throughput data ingestion and enrichment engine engineered to harvest, normalize, and validate multi-dimensional AI ecosystem data without synthetic or hallucinated records.

---

## 📌 Overview

FrontierAtlas automates the end-to-end extraction and normalization of real-world AI entities. It concurrently harvests over 3,000+ authentic records across startups, products, ArXiv research papers with live GitHub star metrics, active job listings, and news feeds—enforcing strict schema adherence and deterministic entity canonicalization.

---

## 🚀 Key Features

* **High-Throughput Concurrency:** Built on Python’s `asyncio` and `aiohttp` to fetch thousands of entity records concurrently without blocking the event loop.
* **Live GitHub Metric Extraction:** Scans ArXiv paper abstracts for linked GitHub repositories using regex patterns and pulls real-time stargazer counts via the GitHub REST API.
* **Deterministic Entity Resolution:** Strips legal/corporate suffixes (`Inc`, `LLC`, `Labs`, `AI`) and uses fuzzy string matching against seed canonical lists with an automated transformation audit log.
* **Strict 24-Hour Signal Temporal Filter:** Custom date parser enforcing strict 24-hour freshness cutoffs for live AI news feeds and remote job boards.
* **Multi-Tab Canonical Export:** Validates incoming payloads with Pydantic schemas and exports structured records into an 6-tab Excel workbook.

---

## 📁 Repository Structure

```text
frontier_atlas_pipeline/
├── extraction/
│   ├── date_normalizer.py     # Parses and enforces 24-hour UTC timestamp freshness
│   └── schemas.py             # Canonical Pydantic models for strict data validation
├── resolution/
│   └── entity_resolver.py     # Rule-based suffix stripping & fuzzy entity matching
├── scrapers/
│   ├── bulk_entities.py       # Verified AI startups & products harvester
│   ├── research_papers.py     # ArXiv AI papers & live GitHub star extractor
│   └── signal_monitor.py      # 24h AI news feeds & remote job boards monitor
├── storage/
│   └── sheets_exporter.py     # Multi-tab canonical Excel workbook generator
├── main.py                    # Async execution entrypoint & orchestrator
├── requirements.txt           # Python dependencies
└── .gitignore                 # Excludes cache, virtual environments, and secrets
