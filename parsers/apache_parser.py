import re
from datetime import datetime
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
