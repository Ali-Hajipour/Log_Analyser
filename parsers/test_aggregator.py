import pytest
from datetime import datetime
from collections import Counter
from parsers.base import LogEntry
from analytics.aggregator import analyse , detect_spikes

def make_entry(
        level = "INFO",
        source = "api",
        timestamp = None,
        ip = None,
        message = "test message"
):
    return LogEntry(
        timestamp = timestamp,
        level=level,
        message=message,
        source=source,
        raw= "raw line",
        extra = {"ip" : ip} if ip else {}
    )

def make_ts(hour : int) -> datetime:
    return datetime(2026,4,7, hour,0,0)

class TestAnalyseBasics:
    def test_empty_entries_returns_zero_total(self):
        assert analyse(iter([]))["total"] == 0
