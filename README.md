# 🔍 Log Analyser
### Developed by Ali Hajipour

A production-grade log analysis tool built in Python from scratch. Parses, normalises, and extracts security insights from multiple log formats — with both a CLI and an interactive Streamlit web dashboard.

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple)
![Tests](https://img.shields.io/badge/Tests-100%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- **Multi-format parsing** — JSON, Apache Combined Log Format, and Syslog through a unified abstract base class interface
- **Memory-efficient streaming** — processes files of any size line by line with constant RAM usage
- **Level normalisation** — maps all format-specific level names to a standard set (`INFO`, `WARN`, `ERROR`, `CRITICAL`)
- **Analytics engine** — single-pass aggregation: error rates, level breakdowns, hourly grouping, top sources, top IPs
- **Statistical spike detection** — flags abnormal error hours using mean + 1σ threshold automatically
- **Streamlit web dashboard** — interactive Plotly charts with colour-coded levels, KPI cards, sortable tables, spike alerts
- **CLI interface** — formatted terminal output with visual bar charts, works on any server or SSH session
- **100+ pytest tests** — full coverage across all parsers and analytics components
- **Graceful error handling** — malformed lines skipped and counted, program never crashes

---

## Supported log formats

### JSON logs
```json
{"timestamp": "2024-01-15T10:23:45", "level": "ERROR", "message": "Disk full", "service": "api"}
```
Supports field aliases: `level / severity / lvl`, `message / msg`, `source / service / logger`, `timestamp / time / ts`

### Apache Combined Log Format
```
192.168.1.1 - frank [15/Jan/2024:10:23:45 +0000] "GET /login HTTP/1.1" 404 512
```
Extracts: IP, user, timestamp, method, path, protocol, status code, response size

### Syslog
```
Jan 15 10:23:45 hostname sshd[1234]: Failed password for root from 192.168.1.1
```
Extracts: timestamp, hostname, app name, PID, message. Level derived from keywords in message.

---

## Security insights

The dashboard helps identify the following patterns through data visualisation:

| Pattern | How to spot it |
|---|---|
| SSH brute force | `sshd` in top sources + spike in ERROR hour + repeated "Failed password" messages |
| Web brute force | Same IP with high request count in Top IPs + many 401s |
| Vulnerability scanning | Single IP hitting many different paths → high 404 count |
| Server incident | Spike alert triggered + 500/503 errors in errors-by-hour chart |
| Privilege escalation | 403 forbidden responses in Apache logs |
| System crash | `kernel` + `panic` keywords → CRITICAL level entries in Syslog |

---

## Architecture

```
parsers/
├── base.py           # Abstract base class — enforces parse_line() contract
│                       Shared parse_file() and parse_string() methods
├── json_parser.py    # JSON parser — field alias normalisation, extra fields
├── apache_parser.py  # Apache parser — regex-based, status → level mapping
└── syslog_parser.py  # Syslog parser — keyword-based level detection

analytics/
└── aggregator.py     # Single-pass analytics engine
                        Counters: level_counts, errors_by_hour, source_counts, ip_counts
                        detect_spikes() — mean + 1σ statistical threshold

dashboard/
└── app.py            # Streamlit web dashboard
                        Plotly bar chart with colour-coded levels
                        Line chart for errors by hour
                        Sortable dataframes for sources and IPs
                        Spike alert boxes

main.py               # CLI entry point — argparse, formatted output with bar charts
```

---

## Installation

```bash
git clone https://github.com/yourname/log-analyser.git
cd log-analyser
pip install -r requirements.txt
```

---

## Usage

### Web dashboard

```bash
streamlit run dashboard/app.py
```

Opens at `http://localhost:8501` — upload a log file and select the format.

### CLI

```bash
python main.py app.log --format json
python main.py access.log --format apache
python main.py syslog.log --format syslog
```

---

## Running tests

```bash
pytest tests/ -v
```

Test coverage:

| File | Tests | What it covers |
|---|---|---|
| `test_json_parser.py` | 24 | Valid input, invalid input, level normalisation, timestamp parsing, parse_string |
| `test_apache_parser.py` | 27 | Valid input, invalid input, status → level mapping, timestamp, size field, user field |
| `test_syslog_parser.py` | 30 | Valid input, invalid input, pid field, keyword level detection, timestamp, parse_string |
| `test_aggregator.py` | 28 | Totals, level counts, error rate, hourly grouping, top sources, top IPs, spike detection |

---

## Tech stack

Python · Regex · ABC & Inheritance · Pandas · Plotly · Streamlit · pytest · argparse · collections.Counter · statistics
