import re
from datetime import datetime
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
