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