# Log Analyser

A production-grade log analysis tool built in Python. Parses, normalises, and extracts insights from multiple log formats — JSON, Apache Combined Log Format, and Syslog — using a unified, extensible parser architecture.

---

## Features

- **Multi-format parsing** — JSON, Apache, and Syslog parsers with a shared interface
- **Memory-efficient streaming** — processes files of any size line by line, constant memory usage
- **Level normalisation** — maps format-specific level names to a standard set (`INFO`, `WARN`, `ERROR`, `CRITICAL`)
- **Graceful error handling** — malformed lines are skipped and counted, never crash the program
- **Extensible architecture** — add new formats by implementing one method (`parse_line`)
- **Fully tested** — 80+ tests across all parsers using pytest

---

## Project Structure

```
log_analyser/
├── parsers/
│   ├── base.py            # Abstract base class — shared interface for all parsers
│   ├── json_parser.py     # JSON log parser (supports multiple field aliases)
│   ├── apache_parser.py   # Apache Combined Log Format parser
│   └── syslog_parser.py   # Syslog format parser with keyword-based level detection
├── tests/
│   ├── test_json_parser.py
│   ├── test_apache_parser.py
│   └──