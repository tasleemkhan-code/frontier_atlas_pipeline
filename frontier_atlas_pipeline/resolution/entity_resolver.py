# resolution/entity_resolver.py
import re
from rapidfuzz import process, fuzz
from typing import Tuple, List, Dict

SEED_CANONICAL_ENTITIES = [
    "OpenAI", "Anthropic", "Cohere", "Mistral AI", "Hugging Face", "Scale AI",
    "Stability AI", "Midjourney", "Character.ai", "Perplexity AI", "Databricks",
    "Runway", "Glean", "Pinecone", "Weaviate", "LangChain", "LlamaIndex",
    "Together AI", "Anyscale", "DeepL", "ElevenLabs", "Harvey", "Poolside",
    "Cognition", "Abridge", "Writer", "Synthesia", "Pika", "Suno", "Udio",
    "Cerebras", "Groq", "SambaNova", "Baseten", "Modal", "Replicate", "Fal AI",
    "Cursor", "Windsurf", "Devin", "Augment", "Factory", "Magic", "Sierra"
]

class EntityResolver:
    def __init__(self, canonical_list: List[str] = SEED_CANONICAL_ENTITIES):
        self.canonical_list = canonical_list
        self.legal_suffixes = re.compile(
            r'\b(inc\.?|incorporated|corp\.?|corporation|llc|ltd\.?|limited|technologies|tech|ai|labs|io|group)\b',
            re.IGNORECASE
        )
        self.mapping_logs: List[Dict[str, str]] = []

    def clean_name(self, raw_name: str) -> str:
        if not raw_name:
            return "Unknown"
        cleaned = self.legal_suffixes.sub('', raw_name)
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned)
        return ' '.join(cleaned.split()).strip()

    def resolve(self, raw_name: str, threshold: float = 82.0) -> str:
        if not raw_name:
            return "Unknown"

        cleaned = self.clean_name(raw_name)

        # 1. Exact case-insensitive matching
        for canon in self.canonical_list:
            if cleaned.lower() == self.clean_name(canon).lower():
                self.mapping_logs.append({
                    "raw_name": raw_name,
                    "canonical_name": canon,
                    "match_type": "EXACT",
                    "confidence": "100%"
                })
                return canon

        # 2. Fuzzy Token Sort Match
        match, score, _ = process.extractOne(
            raw_name,
            self.canonical_list,
            scorer=fuzz.token_sort_ratio
        )

        if score >= threshold:
            self.mapping_logs.append({
                "raw_name": raw_name,
                "canonical_name": match,
                "match_type": "FUZZY",
                "confidence": f"{round(score, 1)}%"
            })
            return match

        # 3. If below threshold, retain original cleaned form
        final_name = raw_name.strip()
        self.mapping_logs.append({
            "raw_name": raw_name,
            "canonical_name": final_name,
            "match_type": "UNMAPPED_ORIGINAL",
            "confidence": "N/A"
        })
        return final_name