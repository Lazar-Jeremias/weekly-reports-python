from utils.date_utils import get_previous_week_dates, format_week_range
from datetime import datetime
from reports.CV.report_generator import generate_weekly_report as generate_cv_report
from reports.EID.report_generator import generate_weekly_report as generate_eid_report
from utils.date_utils import get_previous_week_dates

if __name__ == '__main__':
    start_date, end_date = get_previous_week_dates()
    # No change needed, start_date and end_date are already datetime objects

    # --- Carga Viral Report Generation ---
    cv_tables_to_fetch = [
        "samples_instruments",
        "vl_samples_backlog",
        "vl_registered_samples",
        "VL Samples Tested",
        "VL TRL by US",
        "Tempo de Transporte"
    ]

    cv_output_path = generate_cv_report("Carga Viral", cv_tables_to_fetch, start_date, end_date, overwrite=True)
    if cv_output_path:
        print(f"Carga Viral report generated at: {cv_output_path}")

    # --- DPI Report Generation ---
    eid_tables_to_fetch = [
        "EID Data Table 1", # Replace with actual EID table names
        "EID Data Table 2"  # Replace with actual EID table names
    ]

    eid_output_path = generate_eid_report("DPI", eid_tables_to_fetch, start_date, end_date, overwrite=True)
    if eid_output_path:
        print(f"DPI report generated at: {eid_output_path}")
