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

    print("\n --- Errors by hour ----")
    if results["errors_by_hour"]:
        for hour in sorted(results["errors_by_hour"]):
            count = results["errors_by_hour"][hour]
            bar = "█" * min(count, 40)
            print(f"  {hour:02d}:00  {count:>5,}  {bar}")
    else:
        print("No errors found.")



    print("\n--- Top 10 Sources ---")
    if results["top_sources"]:
        for source , count in results["top_sources"]:
            print(f"  {source:<30} {count:>6,}")
        else:
            print("No sources found.")

    print("\n --- Top 10 IPs")
    if results["top_ip_addresses"]:
        for ip , count in results["top_ip_addresses"]:
            print(f"  {ip:<20} {count:>6,}")
    else:
        print("No IPs found (not Apache logs).")


    print("/n ---Spike Alerts ---")
    if results["spikes"]:
        for spike in results["spikes"]:
            print(f"  ⚠ Hour {spike['hour']:02d}:00 — "
                  f"{spike['error_count']} errors "
                  f"({spike['multiplier']}x above baseline of {spike['baseline']})")
    else:
        print("  No spikes detected.")


        print("\n" + "=" * 50 + "\n")

    def main():
        arg_parser = build_parser()
        args =arg_parser.parse_args()

        if args.format not in PARSERS:
            print(f"Unknown format {args.format}")
            sys.exit(1)

