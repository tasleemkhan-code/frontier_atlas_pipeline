# extraction/date_normalizer.py
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
from dateutil import parser as dparser
import re

def parse_and_validate_24h(date_str: str) -> Tuple[bool, Optional[str]]:
    """
    Parses dates and checks if it falls strictly within the last 24 hours.
    Returns: (is_within_24h, iso_timestamp_string)
    """
    if not date_str:
        return False, None

    date_str = str(date_str).strip()
    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=24)

    # 1. Check relative strings like "X hours ago", "X mins ago"
    rel_match = re.search(r'(\d+)\s*(hour|hr|minute|min|sec)s?\s*ago', date_str, re.IGNORECASE)
    if rel_match:
        val, unit = int(rel_match.group(1)), rel_match.group(2).lower()
        if "hour" in unit or "hr" in unit:
            dt = now_utc - timedelta(hours=val)
        elif "min" in unit:
            dt = now_utc - timedelta(minutes=val)
        else:
            dt = now_utc - timedelta(seconds=val)
        return dt >= cutoff, dt.isoformat()

    # 2. Standard timestamp parsing
    try:
        dt = dparser.parse(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        return dt >= cutoff, dt.isoformat()
    except Exception:
        # Fallback to now if unparseable
        return False, None