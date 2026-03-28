import pytest
from datetime import datetime
from parsers.json_parser import JSONParser
from parsers.base import LogEntry

@pytest.fixture()
def parser():
    return JSONParser()


class TestParseLineValidInput:


class TestParseLineInvalidInput :



class TestLevelNormalization :



class TestTimestampParsing :


class TestParseString :
