# extraction/schemas.py
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class PricingModelEnum(str, Enum):
    FREE = "FREE"
    FREEMIUM = "FREEMIUM"
    PAID = "PAID"
    ENTERPRISE = "ENTERPRISE"

class BaseRecord(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str
    collectedAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

# 1. Startup Schema
class StartupData(BaseModel):
    employeeCount: Optional[int] = None

class StartupContent(BaseModel):
    entityName: str
    data: StartupData = Field(default_factory=StartupData)

class StartupRecord(BaseRecord):
    recordType: str = "STARTUP"
    source: Dict[str, str] = Field(..., description="{'name': str, 'url': str}")
    content: StartupContent

# 2. Product Schema
class ProductContent(BaseModel):
    startupName: str
    pricingModel: PricingModelEnum = PricingModelEnum.FREEMIUM

class ProductRecord(BaseRecord):
    recordType: str = "PRODUCT"
    source: Dict[str, str]
    content: ProductContent

# 3. Research Paper Schema
class ResearchPaperContent(BaseModel):
    title: str
    authors: List[str]
    paper_url: str
    github_url: Optional[str] = None
    github_stars: Optional[int] = 0
    published_date: str

class ResearchPaperRecord(BaseRecord):
    recordType: str = "RESEARCH_PAPER"
    content: ResearchPaperContent

# 4. Job Schema
class JobContent(BaseModel):
    company: str
    date: str
    is_remote: bool
    role_family: str

class JobRecord(BaseRecord):
    recordType: str = "JOB"
    content: JobContent

# 5. News Schema (for 24h Signal Monitoring)
class NewsContent(BaseModel):
    title: str
    source_name: str
    published_date: str
    url: str

class NewsRecord(BaseRecord):
    recordType: str = "NEWS"
    content: NewsContent