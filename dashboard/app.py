import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.json_parser import JSONParser
from parsers.apache_parser import ApacheParser
from parsers.syslog_parser import SyslogParser
from analytics.aggregator import analyse


PARSERS = {
    "json":   JSONParser,
    "apache": ApacheParser,
    "syslog": SyslogParser,
}

LEVEL_COLORS = {
    "INFO":     "#4CAF50",
    "WARN":     "#FF9800",
    "WARNING":  "#FF9800",
    "ERROR":    "#F44336",
    "CRITICAL": "#9C27B0",
    "DEBUG":    "#2196F3",
    "UNKNOWN":  "#9E9E9E",
}

def run_analysis(uploaded_file , file_extension : str) -> dict:
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False , suffix=f"{file_extension}") as temp :
        temp.write(uploaded_file.read())
        temp_path = temp.name
        parser = PARSERS[file_extension]()
        entries = parser.parse_file(temp_path)
        result = analyse(entries)
        os.unlink(temp_path)
        return result
