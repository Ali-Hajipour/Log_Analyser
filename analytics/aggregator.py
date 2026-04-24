from collections import Counter
from typing import Iterator
from statistics import mean, stdev
from parsers.base import LogEntry

def analyse(entries : Iterator[LogEntry]) -> dict :

    total = 0
    error_count = 0
    level_count = Counter()
    errors_by_hour = Counter()
    source_counts = Counter()
    ip_counts = Counter ()

    for entry in entries :
        total += 1

        level = entry.level or "UNKNOWN"
        level_count[level] += 1

        if level in(["ERROR" , "CRITICAL", "WARN"]):
            error_count += 1
            if entry.timestamp:
                errors_by_hour[entry.timestamp.hour] += 1

        if entry.source :
            source_counts[entry.source] += 1

        ip = entry.extra.get("ip")

        if ip:
            ip_counts[ip] += 1

    return {
        "total" : total,
        "error_count" : error_count,
        "error_rate" : round(error_count / total , 4) if total > 0 else 0.0,
        "level_counts" : dict(level_count),
        "errors_by_hour" : dict(errors_by_hour),
        "top_ip_addresses" : ip_counts.most_common(10),
        "top_sources" :  source_counts.most_common(10),
        "spikes" : detect_spikes(errors_by_hour)

    }

def detect_spikes (errors_by_hour :Counter ) ->list:

    if len(errors_by_hour) < 3:
        return []

    numbers = list(errors_by_hour.values())

    baseline = mean(numbers)
    deviation = stdev(numbers)
    threshold = baseline + (2 * deviation)

    spikes =[]

    for hour , count in errors_by_hour.items():
        if count > threshold :
            spikes.append({
                "hour" : hour,
                "error_count" : count,
                "baseline" :  round(baseline, 2),
                "multiplier" : round(count/baseline , 1) if baseline > 0 else 0
            })

    return sorted(spikes , key=lambda x : x["error_count"], reverse=True)