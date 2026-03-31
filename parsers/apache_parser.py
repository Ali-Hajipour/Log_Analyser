import re
from datetime import datetime
from logging import exception
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

        ip = match.group(1)
        user = match.group(2)
        raw_ts   = match.group(3)
        method   = match.group(4)
        path     = match.group(5)
        protocol = match.group(6)
        status   = int(match.group(7))
        size = None if match.group(8) == "-" else int(match.group(8))

        #return LogEntry

    def _parse_timestamp(self, raw_ts : str)-> datetime | None:
        try :
            return datetime.strptime(raw_ts.strip() , TIMESTAMP_FORMAT)
        except (ValueError , TypeError):
            return None

    def _status_to_level(self, status : int) ->str:
        if status < 400 :
            return "INFO"
        elif status < 500:
            return "WARN"
        else:
            return "ERROR"
