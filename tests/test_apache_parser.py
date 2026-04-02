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