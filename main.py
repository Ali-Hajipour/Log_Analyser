import argparse
import sys
from parsers.json_parser import JSONParser
from parsers.syslog_parser import SyslogParser
from parsers.apache_parser import ApacheParser


PARSERS = {
    "json" : JSONParser,
    "apache" : ApacheParser,
    "syslog" : SyslogParser
}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog= "Log Analyser",
        description= "A JSon, Apache,and Syslog supporting log analyser."
    )

    parser.add_argument(
        "file",
        help= "Path of the log file you want to analyse."
    )

    parser.add_argument(
        "--format",
        choices=["json", "apache", "syslog"],
        required= True,
        help= "Log format : Json, Apache, or Syslog"
    )

    return parser