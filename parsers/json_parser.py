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