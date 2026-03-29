import json
from datetime import datetime
from .base import LogEntry ,  BaseParser


KNOWN_FIELDS = {"timestamp", "level" , "message" , "source", "service" , "logger"}

LEVEL_MAP = {
    "info" : "INFO",
    "warn" : "WARN",
    "warning" : "WARN",
    "error" : "ERROR",
    "err" : "ERROR",
    "debug" : "DEBUG",
    "critical" : "CRITICAL",
    "fatal" : "CRITICAL"
}

class JSONParser(BaseParser):
    def parse_line(self , line : str) -> LogEntry | None:
        line = line.strip()

        if not line :
            return None

        data = json.loads(line)

        if not isinstance(data , dict):
            return None

        if not any([data.get("message") , data.get("msg") ,  data.get("lvl") , data.get("level") , data.get("severity") ,  data.get("timestamp") , data.get("ts")]):
            return None

        timestamp = self._parse_timestamp(data)
        level = self._parse_level(data)
        message = data.get("message") or data.get("msg")
        source = data.get("source") or data.get("service") or data.get("logger")
        extra = {k : v for k, v in data.items() if k  not in KNOWN_FIELDS}

        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source,
            raw=line,
            extra=extra,
        )



    def _parse_timestamp(self , data : dict ) -> datetime | None:
        raw_timestamp =  data.get("timestamp") or data.get("time") or data.get("ts")
        if not raw_timestamp:
            return None
        try:
            return datetime.fromisoformat(str(raw_timestamp).strip())
        except (ValueError , TypeError) :
            return None


    def _parse_level(self , data :dict) -> str | None:
        raw_level = data.get("level") or data.get("lvl") or data.get("severity")
        if not raw_level :
            return None

        return LEVEL_MAP.get(str(raw_level).strip().lower() , str(raw_level).strip().upper())

