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

def print_results(results : dict) -> None :
    print("\n" + "=" * 50)
    print("  LOG ANALYSER RESULTS")
    print("=" * 50)

    print(f"\n{'Total entries:':<25} {results['total']:,}")
    print(f"{'Error count:':<25} {results['error_count']:,}")
    print(f"{'Error rate:':<25} {results['error_rate'] * 100:.2f}%")

    print("\n ----level Breakdown----")
    for level, count in sorted(results["level_counts"].items()):
        bar = "█" * min(count // 10, 40)
        print(f"  {level:<12} {count:>6,}  {bar}")


