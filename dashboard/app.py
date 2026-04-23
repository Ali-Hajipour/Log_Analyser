import streamlit as st
import pandas as pd
import sys
import os

from streamlit import divider

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


def render_metric_cards(results : dict) :
    col1 ,col2 , col3 , col4  = st.columns(4)

    with col1:
        st.metric("Total", f"{results['total']:;}")
    with col2 :
        st.metric("Error Count" , f"{results['error_count']:;}")
    with col3:
        rate = results['error_rate'] * 100
        st.metric("Error Rate", f"{rate:.2f}%")
    with col4:
        st.metric("Unique Sources", len(results['top_sources']))



def render_level_chart(results : dict):
    st.subheader("Level Breakdown")
    if not results['level_counts']:
        print("No Level Data Available!")

    df = (pd.DataFrame(list(results['level_counts'].items()) , columns=["Level" , "Count"])
          .sort_values("Count" , ascending= False))
    st.bar_chart(df.set_index("Level"))

def render_errors_by_hours(results : dict):
    st.subheader("Errors by Hour")
    if not results["errors_by_hour"]:
        st.info("No errors found.")
        return
    df = pd.DataFrame(
        list(results["errors_by_hour"].items()),
        columns=["Hour", "Errors"]).sort_values("Hour")
    df["Hour"] = df["Hour"].apply(lambda h: f"{h:02d}:00")
    st.line_chart(df.set_index("Hour"))


def render_top_sources(results: dict):
    st.subheader("Top 10 Sources")
    if not results["top_sources"]:
        st.info("No Source Data Available.")
        return
    df = pd.DataFrame(results["top_sources"] ,  columns=["Source" , "Count"])
    st.dataframe(df , use_container_width=True)

def render_top_ips(results : dict):
    st.subheader("Top 10 IP Addresses")
    if not results["top_ip_addresses"] :
        st.info("No Ips Available. - only For Apache Logs")
        return
    df = pd.DataFrame(results["top_ip_addresses"] , columns=["IP" , "Count"])
    st.dataframe(df, use_container_width=True)

def render_spikes(results:dict):
    if not results["spikes"]:
        st.info("No Spikes Available.")
        return
    for spike in results["spikes"]:
        st.warning(
            f"⚠ Hour {spike['hour']:02d}:00 — "
            f"**{spike['error_count']} errors** "
            f"({spike['multiplier']}x above baseline of {spike['baseline']})"
        )

def main():
    st.set_page_config(
        page_title= "Log Analyser",
        page_icon="🔍",
        layout="wide"
    )

    st.title("Log Analyser | Developed by Ali Hajipour")
    st.caption("Add Json, Syslog, and Apache logs to be analysed.")
    st.divider()

    col1 , col2 = st.columns([3 ,1])

    with col1:
        uploaded_file = st.file_uploader("Upload your Log file :",
                                         type=["log", "json", "txt"],
                                         help="Select the format which your log's format is.")

    with col2:
        fmt = st.selectbox("Log Format", options=["json", "syslog" , "Apache"])
        if uploaded_file is None:
            st.info("👆 Upload a log file above to get started.")
            return

        with st.spinner(f"Parsing {uploaded_file.name} as {fmt} format..."):
            try:
                results = run_analysis(uploaded_file, fmt)
            except Exception as e:
                st.error(f"Failed to parse file: {e}")
                return

    if results["total"] == 0:
        st.warning("No entries could be parsed. Check that the format matches your file.")
        return

    divider()
    render_metric_cards(results)

    st.divider()

    col_left , col_right = st.columns(2)
    render_level_chart(results)










if __name__ == '__main__':
    main()