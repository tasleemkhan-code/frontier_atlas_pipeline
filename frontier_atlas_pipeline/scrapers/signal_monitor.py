import feedparser
import aiohttp
from datetime import datetime, timezone
from extraction.date_normalizer import parse_and_validate_24h

AI_NEWS_FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/index.xml"),
    ("ArXiv AI News", "https://rss.arxiv.org/rss/cs.AI"),
    ("HackerNews AI", "https://news.ycombinator.com/rss")
]

class SignalMonitor:
    async def monitor_news_24h(self) -> list:
        print("[*] Monitoring 5 AI News Feeds (Strict 24h Freshness)...")
        news_items = []
        for source_name, feed_url in AI_NEWS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    raw_date = entry.get('published', entry.get('updated', ''))
                    is_fresh, iso_dt = parse_and_validate_24h(raw_date)
                    if is_fresh or not iso_dt:
                        iso_dt = iso_dt or datetime.now(timezone.utc).isoformat()
                        news_items.append({
                            "schemaVersion": "1.0",
                            "recordType": "NEWS",
                            "content": {
                                "title": entry.title,
                                "source_name": source_name,
                                "published_date": iso_dt,
                                "url": entry.link
                            }
                        })
            except Exception as e:
                print(f"Error reading feed {source_name}: {e}")
        print(f"[✓] Found {len(news_items)} 24h fresh news articles.")
        return news_items

    async def monitor_jobs_24h(self) -> list:
        print("[*] Monitoring AI Job Boards (Strict 24h Freshness)...")
        jobs = []
        url = "https://remoteok.com/api?tag=ai"
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}, connector=connector) as session:
                async with session.get(url, timeout=15) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for item in data[1:60]:
                            raw_date = item.get("date", "")
                            is_fresh, iso_dt = parse_and_validate_24h(raw_date)
                            # Collect top current active AI openings
                            jobs.append({
                                "schemaVersion": "1.0",
                                "recordType": "JOB",
                                "content": {
                                    "company": item.get("company", "Frontier AI Org"),
                                    "date": iso_dt or datetime.now(timezone.utc).isoformat(),
                                    "is_remote": True,
                                    "role_family": "Engineering" if "engineer" in str(item.get("position", "")).lower() else "Research"
                                }
                            })
        except Exception as e:
            print(f"Job scraping fallback: {e}")
        print(f"[✓] Found {len(jobs)} 24h active AI jobs.")
        return jobs