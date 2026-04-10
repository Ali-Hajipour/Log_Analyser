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

    def test_none_level_counted_as_unknown(self):
        entry = [make_entry(level=None)]
        result = analyse(iter(entry))

        assert result["level_count"]["UNKNOWN"] == 1

    def test_critical_counted_in_level_counts(self):
        entry = [make_entry(level="CRITICAL")]
        result = analyse(iter(entry))

        assert result["level_count"]["CRITICAL"] ==  1

class TestAnalyseErrorRate:
    def test_zero_errors_gives_zero_error_rate(self):
        entries = [make_entry(level="INFO") for _ in range(10)]
        result = analyse(iter(entries))
        assert result["error_count"] == 0
        assert result["error_rate"] == 0.0

    def test_all_errors_gives_the_rate_of_one(self):
        entries = [make_entry(level="ERROR") for _ in range(10)]
        result = analyse(iter(entries))

        assert result["error_rate"] == 1.0

    def test_half_errors_gives_the_rate_of_half(self):
        entries = (
                [make_entry(level="ERROR") for _ in range(5)] +
                [make_entry(level="INFO")  for _ in range(5)]
        )
        result = analyse(iter(entries))

        assert result["error_rate"] == 0.5

    def test_critical_counts_in_error_rate(self):
        entries=(
                [make_entry(level="CRITICAL")] +
                [make_entry(level="INFO")]
        )

        result  = analyse(iter(entries))
        assert result["error_rate"] == 0.5

    def test_error_rate_rounded_to_4_decimals(self):
        entries = ([make_entry(level="INFO") for _ in range (3)] +
                   [make_entry(level="ERROR") ])
        result = analyse(iter(entries))

        assert result["error_rate"] == 0.25

class TestAnalyseErrorsByHour: