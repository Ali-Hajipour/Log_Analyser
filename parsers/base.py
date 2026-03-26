from abc import ABC , abstractmethod
from dataclasses import dataclass, field
from logging import exception
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

        with open(filepath , "r" , encoding="utf-8", errors="replace" ) as f:
            for line in f :
                line = line.rstrip("\n") # removing the \n from the right side of the parse line
                if not line.strip():
                    continue
                total +=1
                try:
                    enrty = self.parse_line(line)
                    if enrty is not None:
                        yield enrty
                except exception:
                    failed +=1

        if failed :
            print(f"[parser] {failed}/{total} lines could not be parsed and were skipped.")

    def parse_string(self ,  text : str) -> Iterator[LogEntry]:
        for line in text.splitlines():
            if not line.split():
                continue
            try:
                entry = self.parse_line(line)
                if entry is not None:
                    yield entry
            except exception:
                pass



