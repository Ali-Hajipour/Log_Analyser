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

        if entry.source :
            source_counts[entry.source] += 1

        ip = entry.get("ip")

        if ip:
            ip_counts[ip] += 1

    return {
        "total" : total,
        "error_count" : error_count,
        "error rate" : round(error_count / total , 4) if total > 0 else 0.0,
        "level count" : dict(level_count),
        "errors_by_hour" : dict(errors_by_hour),
        "top_ip_addresses" : ip_counts.most_common(10),
        "top_sources" :  source_counts.most_common(10),
        #"spikes" : detect_spikes()

    }