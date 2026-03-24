from abc import ABC , abstractmethod
from dataclasses import dataclass, field
from typing import Iterator
from datetime import datetime



@dataclass
class LogEntry :
    timestamp : datetime | None
    level : str | None
    message : str | None
    source : str | None
    raw :  str
    extra : dict = field(default_factory=dict)



class BaseParser(ABC) :

    @abstractmethod
    def parse_line (self , line : str) -> LogEntry | None:
        """
        parse a single raw line and return a log entry
        if the line should be ignored it returns None
        """

        ...
    def parse_file(self ,  filepath :  str)-> Iterator[LogEntry] :
        """
                Stream a log file line by line,
                by using Iterator it is also memory safe for large files.

        """

        failed = 0 # counts of parse lines which are failed to parse
        total = 0  # total parse lines parsed.

