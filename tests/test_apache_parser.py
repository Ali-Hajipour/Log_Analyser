import pytest
from datetime import datetime, timezone, timedelta
from parsers.apache_parser import ApacheParser
from parsers.base import LogEntry

VALID_LINE = '192.168.1.1 - frank [15/Jan/2024:10:23:45 +0000] "GET /login HTTP/1.1" 404 512'
NO_SIZE    = '192.168.1.1 - - [15/Jan/2024:10:23:45 +0000] "HEAD / HTTP/1.1" 200 -'
NO_USER    = '192.168.1.1 - - [15/Jan/2024:10:23:45 +0000] "GET /index HTTP/1.1" 200 1024'

@pytest.fixture
def parser():
    return ApacheParser()


class TestApacheParserValidInput:

    def test_valid_line_returns_log_entry(self, parser):
        entry = parser.parse_line(VALID_LINE)
        assert isinstance(entry, LogEntry)

    def test_raw_is_preserved(self, parser):
        entry = parser.parse_line(VALID_LINE)
        assert entry.raw == VALID_LINE

    def test_source_is_apache(self , parser):
        entry = parser.parse_line(VALID_LINE)
        assert  entry.source == "apache"

    def test_message_contains_method_path_status(self,parser):
        entry = parser.parse_line(VALID_LINE)
        assert entry.message == "GET /login 404"

    def test_all_extra_fields_are_present(self,parser):
        entry = parser.parse_line(VALID_LINE)
        assert entry.extra["ip"] == "192.168.1.1"
        assert entry.extra["user"] == "frank"
        assert entry.extra["protocol"] == "HTTP/1.1"
        assert entry.extra["method"] == "GET"
        assert entry.extra["path"] == "/login"
        assert entry.extra["status"] == 404
        assert entry.extra["size"] == 512

    def test_status_is_integer(self,parser):
        entry = parser.parse_line(VALID_LINE)
        assert isinstance(entry.extra["status"] , int)
