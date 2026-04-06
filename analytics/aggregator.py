from collections import Counter
from typing import Iterator
from statistics import mean, stdev
from parsers.base import LogEntry

def analyse(entries : Iterator[LogEntry]) -> dict :

    total = 0
    error_count = 0
    level_count = Counter()
    errors_by_hour : Counter()
    source_counts = Counter()
    ip_counts = Counter ()

    for entry in entries :
        total += 1

        level = entry.level or "Uknown"
        level_count[level] += 1

        if level in(["ERROR" , "CRITICAL"]):
            error_count += 1
            if entry.timestamp:
                errors_by_hour[entry.timestamp.hour] += 1
