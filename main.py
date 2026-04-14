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