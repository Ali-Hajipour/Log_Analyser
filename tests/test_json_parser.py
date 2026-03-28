import pytest
from datetime import datetime
from parsers.json_parser import JSONParser
from parsers.base import LogEntry

@pytest.fixture()
def parser():
    return JSONParser()


class TestParseLineValidInput:

    def test_valid_ful_log_line(self, parser):
        line = '{"timestamp": "2024-01-15T10:23:45", "level": "ERROR", "message": "Disk full", "service": "api"}'
        enrty = parser.parse_line(line)

        assert enrty is not None
        assert enrty.level == "ERROR"
        assert enrty.message == "Disk full"
        assert enrty.source == "api"
        assert enrty.timestamp == datetime(2024, 1, 15, 10, 23, 45)

    def test_raw_preserved(self , parser):
         line = '{"level": "INFO" , "message" : "Server Started"}'
         entry =parser.parse_line(line)

         assert entry.raw == line

    def test_unknown_fields_in_extra(self, parser):
        line = '{"timestamp": "2024-01-15T10:23:45", "level": "ERROR", "message": "Disk full", "service": "api" ,  "request_id" : "ali32" , "env" : "prod" }'
        entry = parser.parse_line(line)

        assert entry.extra["request_id"] == "ali32"
        assert entry.extra["env"] == "prod"



#class TestParseLineInvalidInput :



#class TestLevelNormalization :



#class TestTimestampParsing :


#class TestParseString :
