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


