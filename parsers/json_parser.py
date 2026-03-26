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

class JsonParser(BaseParser):
    def parse_line(self , line : str) -> LogEntry | None:
        line = line.strip()

        if not line :
            return None

        data = json.loads(line)

        if not isinstance(data , dict):
            return None

    def _parse_timestamp(self , data) -> datetime | None:
        raw_timestamp =  data.get("timestamp") or data.get("time") or data.get("ts")
        if not raw_timestamp:
            return None
        try:
            return datetime.fromisoformat(str(raw_timestamp).strip())
        except (ValueError , TypeError) :
            return None


    def _parse_level(self , data :str) -> LogEntry | None:
        raw_level = data.get("level") or data.get("lvl") or data.get("severity")
        if not raw_level :
            return None
        try:
            return LEVEL_MAP.get(str(raw_level).strip().lower() , str(raw_level).strip().upper())

