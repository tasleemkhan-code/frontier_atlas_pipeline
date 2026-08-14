import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import re
import os
import ssl

class PaperScraper:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Authorization": f"Bearer {self.github_token}"} if self.github_token else {}

    async def fetch_github_stars(self, session: aiohttp.ClientSession, github_url: str) -> int:
        if not github_url:
            return 0
        match = re.search(r'github\.com/([^/]+)/([^/]+)', github_url)
        if not match:
            return 0
        owner, repo = match.group(1), match.group(2).replace(".git", "").replace(")", "").replace(".", "")
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            async with session.get(api_url, headers=self.headers, timeout=5, ssl=False) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("stargazers_count", 0)
        except Exception:
            pass
        return 0

    async def fetch_arxiv_papers(self, limit: int = 1000) -> list:
        print(f"[*] Fetching {limit} AI Research Papers from ArXiv...")
        url = f"https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.CV+OR+cat:cs.LG&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
        
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=30) as resp:
                xml_data = await resp.text()

        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip()
                published = entry.find('atom:published', ns).text.strip()
                paper_url = entry.find('atom:id', ns).text.strip()
                
                authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
                
                # Abstract me se GitHub link search karein
                github_match = re.search(r'https?://github\.com/[^\s\)\.\,]+', summary)
                github_url = github_match.group(0) if github_match else None
                
                stars = 0
                if github_url:
                    stars = await self.fetch_github_stars(session, github_url)

                papers.append({
                    "schemaVersion": "1.0",
                    "recordType": "RESEARCH_PAPER",
                    "content": {
                        "title": title,
                        "authors": authors,
                        "paper_url": paper_url,
                        "github_url": github_url,
                        "github_stars": stars,
                        "published_date": published
                    }
                })
        print(f"[✓] Successfully acquired {len(papers)} Research Papers.")
        return papers