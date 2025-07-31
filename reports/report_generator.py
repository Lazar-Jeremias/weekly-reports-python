from utils.db_connector import fetch_data_from_table
from reports.CV.services import get_samples_instruments_data, get_vl_samples_backlog_data, get_vl_registered_samples_data, get_vl_samples_tested_data, get_vl_tat_by_health_facility_data, get_vl_transport_tat_data
from utils.db_connector import get_db_connection, execute_custom_query
from utils.date_utils import format_week_range
import os
import glob

def generate_weekly_report(tables: list, start_date: str, end_date: str, overwrite: bool = False):
    report_data = {}

    # Check if a report for the given date range already exists
    week_range_str = format_week_range(start_date, end_date)
    report_filename_pattern = os.path.join("reports", "CV", f"Carga Viral - semana {week_range_str}.xlsx")
    existing_reports = glob.glob(report_filename_pattern)

    if existing_reports and not overwrite:
        print(f"Report for {start_date} to {end_date} already exists. Skipping generation.")
        return None  # Or return the path to the existing report

    # Fetch data using specific functions
    report_data["Samples Instruments"] = get_samples_instruments_data(start_date, end_date)
    report_data["VL Samples Backlog"] = get_vl_samples_backlog_data(start_date, end_date)
    report_data["VL Samples Tested"] = get_vl_samples_tested_data(start_date, end_date)
    report_data["VL Registered Samples"] = get_vl_registered_samples_data(start_date, end_date)
    report_data["VL TRL by US"] = get_vl_tat_by_health_facility_data(start_date, end_date)
    report_data["Tempo de Transporte"] = get_vl_transport_tat_data(start_date, end_date)

    

    return report_data