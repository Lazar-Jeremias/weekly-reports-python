import openpyxl

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from utils.date_utils import get_previous_week_dates, format_week_range

def populate_cv_report_template(template_path, output_path, data_sets):
    samples_instruments_data = data_sets.get("Samples Instruments", [])
    vl_samples_backlog_data = data_sets.get("VL Samples Backlog", [])
    vl_registered_samples_data = data_sets.get("VL Registered Samples", [])
    workbook = load_workbook(template_path)
    sheet = workbook['Capacidade Laboratorial']

    start_date, end_date = get_previous_week_dates()
    week_range_str = format_week_range(start_date, end_date)


    # Unmerge cells in the data area to avoid MergedCell errors
    start_row = 6
    for merged_cell_range in list(sheet.merged_cells.ranges):
        min_col, min_row, max_col, max_row = merged_cell_range.bounds
        # Check if the merged cell range overlaps with our data writing area (from row 4 onwards)
        if max_row >= start_row:
            sheet.unmerge_cells(str(merged_cell_range))

    # Populate cells D4 and E4 with the week range string
    sheet.merge_cells('D4:E4')
    d4_cell = sheet['D4']
    d4_cell.value = week_range_str
    d4_cell.alignment = Alignment(vertical='center', horizontal='center')

    # Apply medium border around the header from A4 to E5
    for r in range(4, 6):
        for c in range(1, 6):
            cell = sheet.cell(row=r, column=c)
            current_border = cell.border
            new_left = current_border.left
            new_right = current_border.right
            new_top = current_border.top
            new_bottom = current_border.bottom

            if r == 4: # Top border of the header
                new_top = Side(style='medium')
            if r == 5: # Bottom border of the header
                new_bottom = Side(style='medium')
            if c == 1: # Left border of the header
                new_left = Side(style='medium')
            if c == 5: # Right border of the header
                new_right = Side(style='medium')
            
            cell.border = Border(left=new_left, right=new_right, top=new_top, bottom=new_bottom)

    current_row = start_row
    current_lab_name = None

    for row_data in samples_instruments_data:
        lab_name = row_data.get('LabName')

        if current_lab_name is None:
            current_lab_name = lab_name

        if lab_name != current_lab_name:
            # Apply thick bottom border to the previous lab's last row, preserving existing borders
            for col in range(1, 6):  # Columns A to E
                cell = sheet.cell(row=current_row - 1, column=col)
                # Explicitly set thin vertical and top borders, and thick bottom border
                cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='medium'))
            current_lab_name = lab_name

        sheet.cell(row=current_row, column=1, value=lab_name) # Lab
        instrument_cell = sheet.cell(row=current_row, column=2, value=row_data.get('Instrument')) # equipamento
        instrument_cell.font = Font(bold=True)
        # sheet.cell(row=current_row, column=3, value=row_data.get('Capacidade')) # capacidade
        vl_value = row_data.get('VL')
        eid_value = row_data.get('EID')

        vl_cell = sheet.cell(row=current_row, column=4, value='' if vl_value == 0 else vl_value) # VL
        eid_cell = sheet.cell(row=current_row, column=5, value='' if eid_value == 0 else eid_value) # dpi

        # Centralize values in VL and EID columns
        vl_cell.alignment = Alignment(horizontal='center', vertical='center')
        eid_cell.alignment = Alignment(horizontal='center', vertical='center')

        # Apply thin borders to all cells in the data area
        for col in range(1, 6):
            cell = sheet.cell(row=current_row, column=col)
            cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # Fill the last two data columns with #FFF2CC if the cell is empty
        fill_color = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
        if vl_value == 0:
            vl_cell.fill = fill_color
        if eid_value == 0:
            eid_cell.fill = fill_color

        current_row += 1

    # Apply thick border around the entire data table
    if samples_instruments_data:
        max_data_row = current_row - 1
        for r in range(start_row, max_data_row + 1):
            for c in range(1, 6):
                cell = sheet.cell(row=r, column=c)
                current_border = cell.border
                # Initialize new border sides with existing ones
                new_left = current_border.left
                new_right = current_border.right
                new_top = current_border.top
                new_bottom = current_border.bottom

                if r == start_row: # Top border
                    new_top = Side(style='medium')
                if r == max_data_row: # Bottom border
                    new_bottom = Side(style='medium')
                if c == 1: # Left border
                    new_left = Side(style='medium')
                if c == 5: # Right border
                    new_right = Side(style='medium')
                
                cell.border = Border(left=new_left, right=new_right, top=new_top, bottom=new_bottom)








    # # Populate VLSamplesBacklog data
    # sheet_backlog = workbook['VLSamplesBacklog']
    # start_row_backlog = 2  # Assuming headers are in row 1
    # for row_idx, row_data in enumerate(vl_samples_backlog_data):
    #     sheet_backlog.cell(row=start_row_backlog + row_idx, column=1, value=row_data.get('LabName'))
    #     sheet_backlog.cell(row=start_row_backlog + row_idx, column=2, value=row_data.get('Total'))
    #     sheet_backlog.cell(row=start_row_backlog + row_idx, column=3, value=row_data.get('StartDate'))
    #     sheet_backlog.cell(row=start_row_backlog + row_idx, column=4, value=row_data.get('EndDate'))

    # # Populate VLRegisteredSamples data
    # sheet_registered = workbook['VLRegisteredSamples']
    # start_row_registered = 2  # Assuming headers are in row 1
    # for row_idx, row_data in enumerate(vl_registered_samples_data):
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=1, value=row_data.get('LabName'))
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=2, value=row_data.get('Total'))
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=3, value=row_data.get('Registered'))
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=4, value=row_data.get('Rejected'))
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=5, value=row_data.get('StartDate'))
    #     sheet_registered.cell(row=start_row_registered + row_idx, column=6, value=row_data.get('EndDate'))
    #

    # Adjust column widths for better readability
    sheet.column_dimensions[get_column_letter(1)].width = 20  # LabName
    sheet.column_dimensions[get_column_letter(2)].width = 20  # Instrument
    sheet.column_dimensions[get_column_letter(3)].width = 15  # VL
    sheet.column_dimensions[get_column_letter(4)].width = 15  # EID

    workbook.save(output_path)