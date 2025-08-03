from utils.db_connector import fetch_data_from_table
from reports.CV.services import get_samples_instruments_data, get_vl_samples_backlog_data, get_vl_registered_samples_data, get_vl_samples_tested_data, get_vl_tat_by_health_facility_data, get_vl_transport_tat_data
from reports.CV.excel_processor import populate_cv_report_template
from reports.EID.services import get_eid_samples_backlog_data
from utils.db_connector import get_db_connection, execute_custom_query
from utils.date_utils import format_week_range
import os
import glob
from datetime import datetime
import locale

def generate_weekly_report(report_type: str, tables: list, start_date: datetime, end_date: datetime, overwrite: bool = False):
    report_data = {}

    # Generate week range string first
    week_range_str = format_week_range(start_date, end_date)
    report_name = "Carga Viral" if report_type == "CV" else "DPI"

    # Fetch data using specific functions
    report_data["Samples Instruments"] = get_samples_instruments_data(start_date, end_date)
    report_data["VL Samples Backlog"] = get_vl_samples_backlog_data(start_date, end_date)
    report_data["VL Samples Tested"] = get_vl_samples_tested_data(start_date, end_date)
    report_data["VL Registered Samples"] = get_vl_registered_samples_data(start_date, end_date)
    report_data["VL TRL by US"] = get_vl_tat_by_health_facility_data(start_date, end_date)
    report_data["Tempo de Transporte"] = get_vl_transport_tat_data(start_date, end_date)

    # Add DPI specific data fetching here if report_type is 'DPI'
    if report_type == "DPI":
        report_data["EID Samples Backlog"] = get_eid_samples_backlog_data(start_date, end_date)

    # Determine template and output paths based on report type
    if report_type == "Carga Viral":
        template_path = os.path.join("templates", "Template Carga Viral.xlsx")
        report_name_prefix = "Carga Viral"
    elif report_type == "DPI":
        template_path = os.path.join("templates", "EID_Template.xlsx")
        report_name_prefix = "DPI"
    else:
        raise ValueError("Invalid report type specified.")

    # Create dynamic output path
    year = end_date.year
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8') # Set locale to Portuguese
    month_name = end_date.strftime('%B').capitalize()
    locale.setlocale(locale.LC_TIME, '') # Reset locale
    output_dir = os.path.join("output", str(year), month_name, week_range_str)
    os.makedirs(output_dir, exist_ok=True) # ensure directory exists

    output_file_path = os.path.join(output_dir, f"{report_name_prefix} - semana {week_range_str}.xlsx")

    # Remove existing file if overwrite is True
    if overwrite and os.path.exists(output_file_path):
        try:
            os.remove(output_file_path)
            print(f"Existing file removed: {output_file_path}")
        except PermissionError:
            print(f"Warning: Could not remove existing file (may be open in Excel): {output_file_path}")
            print("Please close the file and try again.")
            return None

    # Populate the Excel template
    if report_type == "Carga Viral":
        populate_cv_report_template(template_path, output_file_path, report_data)
    elif report_type == "DPI":
        populate_eid_report_template(template_path, output_file_path, report_data)

    return output_file_path