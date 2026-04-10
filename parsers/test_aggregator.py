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

    def test_empty_entries_returns_error_rate(self):
        assert analyse(iter([]))["error_rate"] == 0.0

    def test_total_counts_all_entries (self):
        entries =  [ make_entry() for _ in range (10)]
        assert  analyse(iter(entries))["total"] == 10

    def test_single_entry(self):
        result = analyse(iter([make_entry(level="ERROR")]))
        assert result["total"] == 1
        assert result["error_count"] == 1


class TestAnalyseLevelCount:

    def test_level_counts_correct(self):
        entries = [
            make_entry(level="INFO"),
            make_entry(level="INFO"),
            make_entry(level="ERROR"),
            make_entry(level="WARN"),
            make_entry(level="ERROR")
        ]
        result = analyse(iter(entries))
        assert result["level_count"]["INFO"] == 2
        assert result["level_count"]["WARN"] == 1
        assert result["level_count"]["ERROR"] == 2