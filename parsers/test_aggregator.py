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
    def test_errors_grouped_by_hour(self):
        entries = (
                [make_entry(level="ERROR", timestamp=make_ts(10))]
            +  [make_entry(level="ERROR" , timestamp=make_ts(10)) ]
            +   [make_entry(level="ERROR" ,timestamp= make_ts(14) )]
        )
        result = analyse(iter(entries))
        assert result["errors_by_hour"][14] == 1
        assert result["errors_by_hour"][10] == 2

    def test_entry_without_ts_wont_counted(self):
        result = analyse(iter([make_entry(level="INFO")]))
        assert result["errors_by_hour"] == {}

class TestAnalyseTopSources:
    def test_top_sources_sorted_by_count(self):
        entries = [
            make_entry(source="api"),
            make_entry(source="api"),
            make_entry(source="nginx"),
        ]
        result = analyse(iter(entries))
        assert result["top_sources"][0] == ("api", 2)
        assert result["top_sources"][1] == ("nginx", 1)

    def test_entry_without_source_not_counted(self):
        entry = [make_entry(source=None)]
        result = analyse(iter(entry))
        assert result["top_sources"] == []

    def test_top_sources_limited_to_10(self):
        entries =([make_entry( source= f"service {i}") for i in range(20)])
        result = analyse(iter(entries))
        assert len(result["top_sources"]) == 10

class TestAnalyseTopIps:

    def test_top_ips_sorted_by_count(self):
       entries =( [make_entry(ip=f"192.168.1.1") for _ in range (10)] +
                  [make_entry(ip=f"192.168.2.2") for _ in range (5)])
       result =analyse(iter(entries))
       assert len(result["top_ip_addresses"]) == 2
       assert result["top_ip_addresses"][0] == ("192.168.1.1", 10)
       assert result["top_ip_addresses"][1] == ("192.168.2.2", 5)

    def test_entry_without_ip_not_counted(self):
        result =analyse(iter([make_entry(ip=None)]))

        assert len(result["top_ip_addresses"]) == 0

    def test_top_ips_limited_to_ten(self):
        entries = [make_entry(ip=f"192.168.1.{i}") for i in range (13)]
        result = analyse(iter(entries))

        assert len(result["top_ip_addresses"]) == 10

class TestDetectSpikes :
    def test_fewer_than_3_hours_returns_empty(self):
        errors_by_hour = Counter({17 : 100 , 11:2})
        assert detect_spikes(errors_by_hour) == []