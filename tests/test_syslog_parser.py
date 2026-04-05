import pytest
from datetime import datetime
from parsers.syslog_parser import SyslogParser
from parsers.base import LogEntry

VALID_LINE     = 'Apr 04 10:23:45 webserver sshd[1234]: Failed password for root from 192.168.1.1'
NO_PID_LINE    = 'Apr 04 10:23:45 webserver kernel: Disk full on /dev/sda1'
ACCEPTED_LINE  = 'Apr 04 10:23:45 webserver sshd[1234]: Accepted password for deploy from 10.0.0.1'
PANIC_LINE     = 'Apr 04 10:23:45 webserver kernel: Kernel panic - not syncing: Fatal exception'
WARNING_LINE   = 'Apr 04 10:23:45 webserver nginx[9012]: warning: disk space low'
PLAIN_LINE     = 'Apr 04 10:23:45 webserver cron[7890]: (root) CMD (/usr/bin/backup.sh)'

@pytest.fixture

def parser():
    return SyslogParser()

class TestSyslogParserValidInput:

    def test_valid_log_returns_logentry(self,parser):
        assert isinstance(parser.parse_line(VALID_LINE) , LogEntry)

    def test_raw_is_preserved(self,parser):
        assert parser.parse_line(VALID_LINE).raw == VALID_LINE

    def test_message_extracted(self,parser):
        assert parser.parse_line(VALID_LINE).message == "Failed password for root from 192.168.1.1"

    def test_source_is_app_name(self,parser):
        assert parser.parse_line(VALID_LINE).source == "sshd"

    def test_hostname_in_extra(self , parser):
        assert parser.parse_line(VALID_LINE).extra["hostname"] == "webserver"

    def test_app_in_extra(self , parser):
        assert parser.parse_line(VALID_LINE).extra["app"] == "sshd"

    def test_pid_is_extracted(self,parser):
        assert parser.parse_line(VALID_LINE).extra["pid"] == 1234

    def test_pid_extracted_as_integer(self,parser):
        assert isinstance(parser.parse_line(VALID_LINE).extra["pid"] , int)

    def test_returns_log_entry_instances(self,parser):
        assert isinstance(parser.parse_line(VALID_LINE) , LogEntry)

class TestSyslogParserInvalidInput:

    def test_blank_line_returns_none(self,parser):
        assert parser.parse_line("") is None

    def test_whitespace_returns_none(self,parser):
        assert parser.parse_line(" ") is None

    def test_non_syslog_line_returns_none(self,parser):
        assert parser.parse_line("this is abosulotely not a syslog") is None

    def test_json_line_returns_none(self,parser):
        assert parser.parse_line('{"level": "ERROR", "message": "Disk full"}') is None

    def test_apache_line_returns_line(self,parser):
        assert parser.parse_line('192.168.1.1 - - [15/Jan/2024:10:23:45 +0000] "GET / HTTP/1.1" 200 512') is None

class TestSyslogPidField :
    def test_pid_present(self,parser):
        assert  parser.parse_line(VALID_LINE).extra["pid"] == 1234

    def test_pid_is_int(self,parser):
        assert isinstance(parser.parse_line(VALID_LINE).extra["pid"], int)

    def test_pid_missing_returns_none(self,parser):
        assert parser.parse_line(NO_PID_LINE).extra["pid"] is None

class TestSyslogLevelDetection:

    def test_failed_maps_to_error(self,parser):
        assert parser.parse_line(VALID_LINE).level == "ERROR"

    def test_accepted_maps_to_info(self,parser):
        assert parser.parse_line(ACCEPTED_LINE).level == "INFO"

    def test_panic_maps_to_info(self,parser):
        assert parser.parse_line(PANIC_LINE).level == "CRITICAL"

    def test_warning_maps_to_info(self,parser):
        assert parser.parse_line(WARNING_LINE).level == "WARN"

    def test_no_keyword_maps_to_info(self,parser):
        assert parser.parse_line(PLAIN_LINE).level == "INFO"

    def test_level_detection_case_insensitive(self, parser):
        line = 'Jan 15 10:23:45 webserver app[1]: ERROR something broke'
        assert parser.parse_line(line).level == "ERROR"

    def test_uppercase_failed_detected(self, parser):
        line = 'Jan 15 10:23:45 webserver app[1]: FAILED to connect'
        assert parser.parse_line(line).level == "ERROR"

class TestSyslogTimestamp:
    def test_valid_timestamp_parsed(self,parser):
        entry = parser.parse_line(VALID_LINE)
        assert entry.timestamp is not None
        assert isinstance(entry.timestamp, datetime)
        assert entry.timestamp.month  == 4
        assert entry.timestamp.day    == 4
        assert entry.timestamp.hour   == 10
        assert entry.timestamp.minute == 23
        assert entry.timestamp.second == 45

    def test_timestamp_year_is_correct(self, parser):
        assert parser.parse_line(VALID_LINE).timestamp.year == datetime.now().year

    def test_invalid_timestamp_returns_none(self,parser):
        assert parser.parse_line('Xyz 99 99:99:99 webserver app[1]: message').timestamp is None

class TestSyslogNoPid:

    def test_no_pid_line_parsed_correctly(self,parser):
       entry = (parser.parse_line(NO_PID_LINE))
       assert entry.extra["pid"] is None
       assert entry.message == "Disk full on /dev/sda1"

class TestParseString :

    def test_multiple_syslog_lines(self,parser):
        text = """
Apr 05 10:23:45 webserver sshd[1234]: Failed password for root
Apr 05 10:23:46 webserver sshd[1234]: Accepted password for deploy
Apr 05 10:23:47 webserver kernel: Kernel panic - not syncing
"""
        entries = list(parser.parse_string(text))
        assert len(entries) == 3
        assert entries[0].raw == "Apr 05 10:23:45 webserver sshd[1234]: Failed password for root"
        assert entries[0].level == "ERROR"
        assert entries[1].level == "INFO"
        assert entries[2].level == "CRITICAL"

    def test_blank_lines_skipped(self,parser):
        text = """
Apr 05 10:23:45 webserver sshd[1234]: Failed password for root

Apr 05 10:23:47 webserver kernel: Kernel panic - not syncing
"""
        entries = list(parser.parse_string(text))
        assert len(entries) == 2
        assert entries[0].level == "ERROR"
        assert entries[1].level == "CRITICAL"


