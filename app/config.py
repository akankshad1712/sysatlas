"""Validated configuration with safe defaults for local development."""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv("SYSATLAS_DATABASE", "./data/sysatlas.db")
    collector_binary: str = os.getenv("SYSATLAS_COLLECTOR", "./build/sysatlas-collector")
    collection_timeout_seconds: float = float(os.getenv("SYSATLAS_COLLECTION_TIMEOUT", "3"))
    max_page_size: int = int(os.getenv("SYSATLAS_MAX_PAGE_SIZE", "100"))
    stale_after_seconds: int = int(os.getenv("SYSATLAS_STALE_AFTER_SECONDS", "120"))

settings = Settings()
