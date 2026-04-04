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