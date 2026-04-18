import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.json_parser import JSONParser
from parsers.apache_parser import ApacheParser
from parsers.syslog_parser import SyslogParser
from analytics.aggregator import analyse
