# storage/sheets_exporter.py
import pandas as pd
import os

class DataExporter:
    @staticmethod
    def export_to_excel(startups, products, papers, jobs, news, entity_logs, filename="frontier_atlas_output.xlsx"):
        print("\n[*] Packaging data into 6 Canonical Tabs...")

        # 1. Startups Tab
        startups_rows = [{
            "schemaVersion": item["schemaVersion"],
            "recordType": item["recordType"],
            "source.name": item["source"]["name"],
            "source.url": item["source"]["url"],
            "content.entityName": item["content"]["entityName"],
            "content.data.employeeCount": item["content"]["data"]["employeeCount"],
            "collectedAt": item["collectedAt"]
        } for item in startups]
        df_startups = pd.DataFrame(startups_rows)

        # 2. Products Tab
        products_rows = [{
            "schemaVersion": item["schemaVersion"],
            "recordType": item["recordType"],
            "source.name": item["source"]["name"],
            "source.url": item["source"]["url"],
            "content.startupName": item["content"]["startupName"],
            "content.pricingModel": item["content"]["pricingModel"],
            "collectedAt": item["collectedAt"]
        } for item in products]
        df_products = pd.DataFrame(products_rows)

        # 3. Research Papers Tab
        papers_rows = [{
            "schemaVersion": item["schemaVersion"],
            "recordType": item["recordType"],
            "content.title": item["content"]["title"],
            "content.authors": ", ".join(item["content"]["authors"]),
            "content.paper_url": item["content"]["paper_url"],
            "content.github_url": item["content"]["github_url"],
            "content.github_stars": item["content"]["github_stars"],
            "content.published_date": item["content"]["published_date"]
        } for item in papers]
        df_papers = pd.DataFrame(papers_rows)

        # 4. Jobs Tab
        jobs_rows = [{
            "schemaVersion": item["schemaVersion"],
            "recordType": item["recordType"],
            "content.company": item["content"]["company"],
            "content.date": item["content"]["date"],
            "content.is_remote": item["content"]["is_remote"],
            "content.role_family": item["content"]["role_family"]
        } for item in jobs]
        df_jobs = pd.DataFrame(jobs_rows) if jobs_rows else pd.DataFrame(columns=["schemaVersion", "recordType", "content.company", "content.date", "content.is_remote", "content.role_family"])

        # 5. News Tab
        news_rows = [{
            "schemaVersion": item["schemaVersion"],
            "recordType": item["recordType"],
            "content.title": item["content"]["title"],
            "content.source_name": item["content"]["source_name"],
            "content.published_date": item["content"]["published_date"],
            "content.url": item["content"]["url"]
        } for item in news]
        df_news = pd.DataFrame(news_rows) if news_rows else pd.DataFrame(columns=["schemaVersion", "recordType", "content.title", "content.source_name", "content.published_date", "content.url"])

        # 6. Entity Mapping Log Tab
        df_entity_logs = pd.DataFrame(entity_logs)

        # 6-Tab Workbook Export
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df_startups.to_excel(writer, sheet_name='Startups', index=False)
            df_products.to_excel(writer, sheet_name='Products', index=False)
            df_papers.to_excel(writer, sheet_name='Research Papers', index=False)
            df_jobs.to_excel(writer, sheet_name='Jobs', index=False)
            df_news.to_excel(writer, sheet_name='News', index=False)
            df_entity_logs.to_excel(writer, sheet_name='Entity Mapping Log', index=False)

        print(f"[✓] SUCCESS: Master File Generated at: {os.path.abspath(filename)}")