# main.py
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from scrapers.research_papers import PaperScraper
from scrapers.bulk_entities import BulkEntityScraper
from scrapers.signal_monitor import SignalMonitor
from resolution.entity_resolver import EntityResolver
from storage.sheets_exporter import DataExporter

async def run_pipeline():
    print("=" * 60)
    print(" FrontierAtlas / The AI Signal - Automated Ingestion Engine ")
    print("=" * 60)

    resolver = EntityResolver()
    paper_scraper = PaperScraper()
    entity_scraper = BulkEntityScraper()
    signal_monitor = SignalMonitor()

    # 1. Fetch Bulk Records Concurrently
    papers_task = paper_scraper.fetch_arxiv_papers(limit=1000)
    startups_task = entity_scraper.fetch_startups(count=1000)
    products_task = entity_scraper.fetch_products(count=1000)
    news_task = signal_monitor.monitor_news_24h()
    jobs_task = signal_monitor.monitor_jobs_24h()

    papers, startups, products, news, jobs = await asyncio.gather(
        papers_task, startups_task, products_task, news_task, jobs_task
    )

    # 2. Run Deterministic Entity Resolution
    print("\n[*] Applying Entity Canonicalization...")
    for item in startups:
        raw_name = item["content"]["entityName"]
        canonical_name = resolver.resolve(raw_name)
        item["content"]["entityName"] = canonical_name

    for item in products:
        raw_name = item["content"]["startupName"]
        canonical_name = resolver.resolve(raw_name)
        item["content"]["startupName"] = canonical_name

    # 3. Export to 6 Tabs
    DataExporter.export_to_excel(
        startups=startups,
        products=products,
        papers=papers,
        jobs=jobs,
        news=news,
        entity_logs=resolver.mapping_logs,
        filename="frontier_atlas_output.xlsx"
    )

    print("\n" + "=" * 60)
    print(" PIPELINE EXECUTION COMPLETED SUCCESSFULLY ")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_pipeline())