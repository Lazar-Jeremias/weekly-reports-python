from reports.EID.services import get_eid_samples_backlog_data, get_eid_tested_samples_monitoria_data, get_eid_registered_samples_data, get_eid_tat_by_health_facility_data, get_eid_transport_tat_data
from reports.EID.excel_processor import populate_eid_report_template
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
    report_name = "DPI"

    # Fetch data using specific functions for EID
    eid_samples_backlog_data = get_eid_samples_backlog_data(start_date, end_date)
    if eid_samples_backlog_data is None:
        print("Warning: EID Samples Backlog data could not be fetched.")
        report_data["EID Samples Backlog"] = []
    else:
        report_data["EID Samples Backlog"] = eid_samples_backlog_data

    # EID Samples Tested data removido - tabela não existe
    # Os dados são obtidos via EIDTestedSamplesPerWeek na função get_eid_tested_samples_monitoria_data

    # Fetch EID Monitoria data
    eid_tested_samples_monitoria_data = get_eid_tested_samples_monitoria_data(start_date, end_date)
    if eid_tested_samples_monitoria_data is None:
        print("Warning: EID Tested Samples Monitoria data could not be fetched.")
        report_data["EID Tested Samples Monitoria"] = []
    else:
        report_data["EID Tested Samples Monitoria"] = eid_tested_samples_monitoria_data

    # Fetch EID Registered Samples data
    eid_registered_samples_data = get_eid_registered_samples_data(start_date, end_date)
    if eid_registered_samples_data is None:
        print("Warning: EID Registered Samples data could not be fetched.")
        report_data["EID Registered Samples"] = []
    else:
        report_data["EID Registered Samples"] = eid_registered_samples_data

    # Fetch EID TAT by Health Facility data
    eid_tat_by_health_facility_data = get_eid_tat_by_health_facility_data(start_date, end_date)
    if eid_tat_by_health_facility_data is None:
        print("Warning: EID TAT by Health Facility data could not be fetched.")
        report_data["EID TRL by US"] = []
    else:
        report_data["EID TRL by US"] = eid_tat_by_health_facility_data

    # Fetch EID Transport TAT data
    eid_transport_tat_data = get_eid_transport_tat_data(start_date, end_date)
    if eid_transport_tat_data is None:
        print("Warning: EID Transport TAT data could not be fetched.")
        report_data["Tempo de Transporte"] = []
    else:
        report_data["Tempo de Transporte"] = eid_transport_tat_data

    # Determine template and output paths based on report type
    template_path = os.path.join("templates", "EID_Template.xlsx")
    report_name_prefix = "DPI"

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
    populate_eid_report_template(template_path, output_file_path, report_data)

    return output_file_path