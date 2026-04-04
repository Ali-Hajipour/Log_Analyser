import re
from datetime import datetime
from logging import raiseExceptions

from .base import BaseParser,LogEntry

SYSLOG_PATTERN = re.compile(
    r'(\w+\s+\d+\s+\d+:\d+:\d+)'   
    r'\s+(\S+)'                      
    r'\s+(\S+?)'                     
    r'(?:\[(\d+)\])?'                
    r':\s*(.*)'
)

TIMESTAMP_FORMAT = "%Y %b %d %H:%M:%S"

LEVEL_MAP ={
    "error" : "ERROR",
    "err" : "ERROR",
    "failed" : "ERROR",
    "failure" : "ERROR",
    "panic" : "CRITICAL",
    "emerg" : "CRITICAL",
    "alert" : "CRITICAL",
    "warn" : "WARN",
    "warning" : "WARN",
    "notice" : "WARN",
    "info" : "INFO",
    "accepted" : "INFO",
    "started" : "INFO",
    "debug" : "DEBUG"
}


class SyslogParser(BaseParser):

    def parse_line(self, line : str)-> LogEntry | None:
        line = line.strip()
        if not line :
            return None

        match = SYSLOG_PATTERN.match(line)
        if not match :
            return None

        raw_ts = match.group(1)
        hostname = match.group(2)
        app = match.group(3).rstrip(":")
        pid = match.group(4)
        message = match.group(5).strip()
