import re
from datetime import datetime
from re import match

from .base import BaseParser, LogEntry

APACHE_PATTERN = re.compile(
    r'(\S+)'         
    r' \S+'          
    r' (\S+)'        
    r' \[([^\]]+)\]' 
    r' "(\S+)'   
    r' (\S+)'    
    r' (\S+)"'         
    r' (\d{3})'        
    r' (\d+|-)'
)

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

class ApacheParser(BaseParser):
    def json_parser(self , line : str) -> LogEntry | None:
        line =line.strip()
        if not line :
            return None
        match = APACHE_PATTERN.match(line)

        if not match :
            return None