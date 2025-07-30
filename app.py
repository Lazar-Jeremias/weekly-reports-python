import os
from utils.date_utils import get_previous_week_dates, format_week_range
from reports.report_generator import generate_weekly_report
from utils.excel_processor import populate_cv_report_template
from reports.CV.services import get_samples_instruments_data, get_vl_samples_backlog_data, get_vl_registered_samples_data

if __name__ == '__main__':
    start_date, end_date = get_previous_week_dates()

    # Define the tables to fetch data from
    tables_to_fetch = [
        "samples_instruments",
        "vl_samples_backlog",
        "vl_registered_samples"
    ]

    # Generate the weekly report, allowing overwrite if needed
    report_data = generate_weekly_report(tables_to_fetch, start_date, end_date, overwrite=True)

    if report_data:
        # Process the report data and populate the Excel template
        template_path = r"c:\Users\lazar\weekly-reports\reports\CV\template\Template Carga Viral.xlsx"
        week_start, week_end = get_previous_week_dates()
        week_range_str = format_week_range(week_start, week_end)
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports', 'CV')
        output_filename = f"Carga Viral - semana {week_range_str}.xlsx"
        output_path = os.path.join(output_dir, output_filename)

        populate_cv_report_template(
            template_path,
            output_path,
            report_data
        )
