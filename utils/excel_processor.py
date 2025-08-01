import openpyxl

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from utils.date_utils import get_previous_week_dates, format_week_range

def populate_cv_report_template(template_path, output_path, data_sets):
    samples_instruments_data = data_sets.get("Samples Instruments", [])
    vl_samples_backlog_data = data_sets.get("VL Samples Backlog", [])
    vl_samples_tested_data = data_sets.get("VL Samples Tested", [])
    vl_registered_samples_data = data_sets.get("VL Registered Samples", [])
    vl_tat_by_health_facility_data = data_sets.get("VL TRL by US", [])
    vl_transport_tat_data = data_sets.get("Tempo de Transporte", [])

    # Carrega o template
    workbook = load_workbook(template_path)

    # Capacidade Laboratorial
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
        instrument_cell = sheet.cell(row=current_row, column=2, value=row_data.get('AnalyzerDesc')) # equipamento
        instrument_cell.font = Font(bold=True)
        # capacity_cell = sheet.cell(row=current_row, column=3, value=row_data.get('Capacity')) # capacidade
        capacity_value = row_data.get('Capacity')
        eid_value = row_data.get('EID')
        vl_value = row_data.get('VL')
        

        capacity_cell = sheet.cell(row=current_row, column=3, value='' if capacity_value == 0 else capacity_value) # capacidade
        eid_cell = sheet.cell(row=current_row, column=4, value='' if eid_value == 0 else eid_value) # dpi
        vl_cell = sheet.cell(row=current_row, column=5, value='' if vl_value == 0 else vl_value) # VL
        # Centralize values in VL and EID columns
        capacity_cell.alignment = Alignment(horizontal='center', vertical='center')
        eid_cell.alignment = Alignment(horizontal='center', vertical='center')
        vl_cell.alignment = Alignment(horizontal='center', vertical='center')
        

        # Apply thin borders to all cells in the data area
        for col in range(1, 6):
            cell = sheet.cell(row=current_row, column=col)
            cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # Fill the last two data columns with #FFF2CC if the cell is empty
        fill_color = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
        
        if eid_value == 0:
            eid_cell.fill = fill_color
        if vl_value == 0:
            vl_cell.fill = fill_color

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


    # Populate VLSamplesBacklog data
    sheet_backlog = workbook['Amostras não processadas']
    start_row_backlog = 7  # Data starts at row 7
    
    # Get the list of labs in the same order as they appear in the Excel template
    template_labs = [
        'Cabo Delgado', 'Carmelo', 'Chimoio', 'Dream Beira', 'Dream Maputo',
        'INS', 'Lichinga', 'Machava', 'Mavalane', 'Nampula',
        'Ponta Gea', 'Quelimane', 'Tete', 'Xai-Xai'
    ]
    
    # Create a mapping from lab name to backlog data for quick lookup
    backlog_data_map = {row['LabName']: row for row in vl_samples_backlog_data}
    
    for row_idx, lab_name in enumerate(template_labs):
        row_data = backlog_data_map.get(lab_name, {})
        
        # Fill columns B to G (Total, <7, 7-15, 15-21, >21, no_data)
        # Replace None/Null values with 0 to ensure formulas work
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=2, value=row_data.get('Total', 0))
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=3, value=row_data.get('<7', 0))
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=4, value=row_data.get('7-15', 0))
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=5, value=row_data.get('15-21', 0))
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=6, value=row_data.get('>21', 0))
        sheet_backlog.cell(row=start_row_backlog + row_idx, column=7, value=row_data.get('no_data', 0))


    # Populate weekly range string in 'Amostras não processadas' sheet
    for merged_cell_range in list(sheet_backlog.merged_cells.ranges):
        if 'B3' in str(merged_cell_range) or 'C3' in str(merged_cell_range):
            sheet_backlog.unmerge_cells(str(merged_cell_range))
    sheet_backlog.merge_cells('B3:F3')
    b3_cell = sheet_backlog['B3']
    b3_cell.value = f"Amostras não Processadas (Semana: {week_range_str})"
    b3_cell.alignment = Alignment(vertical='center', horizontal='center')

    # Populate 'Monitoria das Amostras' sheet
    sheet_monitoria = workbook['Monitoria das Amostras']
    lab_order_monitoria = [
        'Cabo Delgado', 'Carmelo', 'Chimoio', 'Dream Beira', 'Dream Maputo',
        'INS', 'Lichinga', 'Machava', 'Mavalane', 'Nampula',
        'Ponta Gea', 'Quelimane', 'Tete', 'Xai-Xai'
    ]

    query_data_columns = [
        'total_samples',
        'collection_less_than_7',
        'collection_btwn_7_and_15',
        'collection_btwn_16_and_21',
        'collection_greater_than_21',
        'collection_no_data',
        'registration_less_than_7',
        'registration_btwn_7_and_15',
        'registration_btwn_16_and_21',
        'registration_greater_than_21',
        'testing_less_than_2',
        'testing_btwn_2_and_7',
        'testing_greater_than_7',
        'tat_less_than_7',
        'tat_btwn_7_and_15',
        'tat_btwn_16_and_21',
        'tat_greater_than_21',
        'tat_average',
        'no_collection_date',
        'no_age',
        'no_sex'
    ]

    samples_tested_data_map = {row['lab_name']: row for row in vl_samples_tested_data}

    start_row_monitoria = 5
    start_col_monitoria = 2

    for row_idx, lab_name in enumerate(lab_order_monitoria):
        row_data = samples_tested_data_map.get(lab_name, {})
        for col_idx, col_name in enumerate(query_data_columns):
            cell_value = row_data.get(col_name, 0)
            sheet_monitoria.cell(row=start_row_monitoria + row_idx, column=start_col_monitoria + col_idx, value=cell_value)

    # Populate VLRegisteredSamples data in 'Monitoria das Amostras' sheet (B26 to L39)
    registered_query_data_columns = [
        'registered',
        'collection_lt_7',
        'collection_7_15',
        'collection_16_21',
        'collection_gt_21',
        'no_specimen_date',
        'testing_lt_7',
        'testing_7_15',
        'testing_16_21',
        'testing_gt_21',
        'no_testing_date'
    ]

    registered_samples_data_map = {row['lab_name']: row for row in vl_registered_samples_data}

    start_row_registered = 26
    start_col_registered = 2

    for row_idx, lab_name in enumerate(lab_order_monitoria):
        row_data = registered_samples_data_map.get(lab_name, {})
        for col_idx, col_name in enumerate(registered_query_data_columns):
            cell_value = row_data.get(col_name, 0)
            if cell_value == '' or cell_value is None:
                cell_value = 0
            sheet_monitoria.cell(row=start_row_registered + row_idx, column=start_col_registered + col_idx, value=cell_value)

    # Adjust column widths for better readability
    sheet.column_dimensions[get_column_letter(1)].width = 20  # LabName
    sheet.column_dimensions[get_column_letter(2)].width = 20  # Instrument
    sheet.column_dimensions[get_column_letter(3)].width = 15  # VL
    sheet.column_dimensions[get_column_letter(4)].width = 15  # EID


    # Populate 'TRL por US' sheet
    sheet_trl_us = workbook['TRL por US']
    start_row_trl_us = 6

    # Populate weekly range string in 'TRL por US' sheet
    for merged_cell_range in list(sheet_trl_us.merged_cells.ranges):
        if 'B2' in str(merged_cell_range) or 'C2' in str(merged_cell_range):
            sheet_trl_us.unmerge_cells(str(merged_cell_range))
    sheet_trl_us.merge_cells('B2:H2')
    b2_cell = sheet_trl_us['B2']
    b2_cell.value = f"Tempo de Resposta Laboratorial das Amostras por Unidade Sanitária (Semana: {week_range_str})"
    b2_cell.alignment = Alignment(vertical='center', horizontal='center')

    # Define the columns to be populated from the query result
    trl_us_columns = [
        'FacilityNationalCode',
        'RequestingFacilityCode',
        'ProvinceName',
        'DistrictName',
        'RequestingFacilityName',
        'TestingFacilityName',
        'TypeOfTest',
        'TotalTestedSamples',
        'rejected',
        'TestedSamplesWithCollectionDate',
        'collected_lt_7',
        'collected_7_15',
        'collected_16_21',
        'collected_gt_21',
        'collected_no_data',
        'received_lt_7',
        'received_7_15',
        'received_16_21',
        'received_gt_21',
        'received_no_data',
        'registered_lt_7',
        'registered_7_15',
        'registered_16_21',
        'registered_gt_21',
        'registered_no_data',
        'tested_lt_2',
        'tested_2_7',
        'tested_gt_7',
        'tested_no_data',
        'total_lt_7',
        'total_7_15',
        'total_16_21',
        'total_gt_21',
        'total_no_data',
        'tat'
    ]

    # Determine the number of rows to fill
    num_data_rows = len(vl_tat_by_health_facility_data)

    if num_data_rows > 0:
        # Copy style from row 6 to subsequent rows
        source_row = sheet_trl_us[start_row_trl_us]
        for r_idx in range(start_row_trl_us + 1, start_row_trl_us + num_data_rows):
            for c_idx, cell in enumerate(source_row):
                new_cell = sheet_trl_us.cell(row=r_idx, column=c_idx + 1)
                if cell.has_style:
                    new_cell.font = cell.font.copy()
                    new_cell.border = cell.border.copy()
                    new_cell.fill = cell.fill.copy()
                    new_cell.number_format = cell.number_format
                    new_cell.alignment = cell.alignment.copy()

        # Populate data
        for row_idx, row_data in enumerate(vl_tat_by_health_facility_data):
            for col_idx, col_name in enumerate(trl_us_columns):
                cell_value = row_data.get(col_name)
                # Replace None with empty string or 0 based on context
                if cell_value is None:
                    if col_name in ['TotalTestedSamples', 'rejected', 'collected_lt_7', 'collected_7_15', 'collected_16_21', 'collected_gt_21', 'collected_no_data', 'received_lt_7', 'received_7_15', 'received_16_21', 'received_gt_21', 'received_no_data', 'registered_lt_7', 'registered_7_15', 'registered_16_21', 'registered_gt_21', 'registered_no_data', 'tested_lt_2', 'tested_2_7', 'tested_gt_7', 'tested_no_data', 'total_lt_7', 'total_7_15', 'total_16_21', 'total_gt_21', 'total_no_data', 'tat']:
                        cell_value = 0  # Replace with 0 for numeric columns
                    else:
                        cell_value = ''  # Replace with empty string for other columns
                sheet_trl_us.cell(row=start_row_trl_us + row_idx, column=col_idx + 1, value=cell_value)

    # Populate 'Tempo de Transporte' sheet
    sheet_transport_tat = workbook['Tempo de Transporte']
    start_row_transport_tat = 6

    # Populate weekly range string in 'Tempo de Transporte' sheet
    for merged_cell_range in list(sheet_transport_tat.merged_cells.ranges):
        if 'B2' in str(merged_cell_range) or 'C2' in str(merged_cell_range):
            sheet_transport_tat.unmerge_cells(str(merged_cell_range))
    sheet_transport_tat.merge_cells('B2:H2')
    b2_cell_transport = sheet_transport_tat['B2']
    b2_cell_transport.value = f"Tempo de Transporte das Amostras (Semana: {week_range_str})"
    b2_cell_transport.alignment = Alignment(vertical='center', horizontal='center')

    # Define the columns to be populated from the query result
    transport_tat_columns = [
        'FacilityNationalCode',
        'RequestingFacilityCode',
        'ProvinceName',
        'DistrictName',
        'RequestingFacilityName',
        'TestingFacilityName',
        'TypeOfTest',
        'Total_de_Amostras',
        'TestedSamplesWithCollectionDate',
        'collection_to_hub_lt_7',
        'collection_to_hub_7_15',
        'collection_to_hub_16_21',
        'collection_to_hub_gt_21',
        'collection_to_hub_no_data',
        'hub_reception_to_registration_lt_7',
        'hub_reception_to_registration_7_15',
        'hub_reception_to_registration_16_21',
        'hub_reception_to_registration_gt_21',
        'hub_reception_to_registration_no_data',
        'hub_to_lab_reception_lt_7',
        'hub_to_lab_reception_7_15',
        'hub_to_lab_reception_16_21',
        'hub_to_lab_reception_gt_21',
        'hub_to_lab_reception_no_data',
        'lab_reception_to_registration_lt_7',
        'lab_reception_to_registration_7_15',
        'lab_reception_to_registration_16_21',
        'lab_reception_to_registration_gt_21',
        'lab_reception_to_registration_no_data',
        'collection_to_lab_reception_lt_7',
        'collection_to_lab_reception_7_15',
        'collection_to_lab_reception_16_21',
        'collection_to_lab_reception_gt_21',
        'collection_to_lab_reception_no_data'
    ]

    # Determine the number of rows to fill
    num_data_rows_transport = len(vl_transport_tat_data)

    if num_data_rows_transport > 0:
        # Copy style from row 6 to subsequent rows
        source_row_transport = sheet_transport_tat[start_row_transport_tat]
        for r_idx in range(start_row_transport_tat + 1, start_row_transport_tat + num_data_rows_transport):
            for c_idx, cell in enumerate(source_row_transport):
                new_cell = sheet_transport_tat.cell(row=r_idx, column=c_idx + 1)
                if cell.has_style:
                    new_cell.font = cell.font.copy()
                    new_cell.border = cell.border.copy()
                    new_cell.fill = cell.fill.copy()
                    new_cell.number_format = cell.number_format
                    new_cell.alignment = cell.alignment.copy()

        # Populate data
        for row_idx, row_data in enumerate(vl_transport_tat_data):
            for col_idx, col_name in enumerate(transport_tat_columns):
                cell_value = row_data.get(col_name)
                # Replace None with empty string or 0 based on context
                if cell_value is None:
                    if col_name in [
                        'Total_de_Amostras',
                        'TestedSamplesWithCollectionDate',
                        'collection_to_hub_lt_7',
                        'collection_to_hub_7_15',
                        'collection_to_hub_16_21',
                        'collection_to_hub_gt_21',
                        'collection_to_hub_no_data',
                        'hub_reception_to_registration_lt_7',
                        'hub_reception_to_registration_7_15',
                        'hub_reception_to_registration_16_21',
                        'hub_reception_to_registration_gt_21',
                        'hub_reception_to_registration_no_data',
                        'hub_to_lab_reception_lt_7',
                        'hub_to_lab_reception_7_15',
                        'hub_to_lab_reception_16_21',
                        'hub_to_lab_reception_gt_21',
                        'hub_to_lab_reception_no_data',
                        'lab_reception_to_registration_lt_7',
                        'lab_reception_to_registration_7_15',
                        'lab_reception_to_registration_16_21',
                        'lab_reception_to_registration_gt_21',
                        'lab_reception_to_registration_no_data',
                        'collection_to_lab_reception_lt_7',
                        'collection_to_lab_reception_7_15',
                        'collection_to_lab_reception_16_21',
                        'collection_to_lab_reception_gt_21',
                        'collection_to_lab_reception_no_data'
                    ]:
                        cell_value = 0  # Replace with 0 for numeric columns
                    else:
                        cell_value = ''  # Replace with empty string for other columns
                sheet_transport_tat.cell(row=start_row_transport_tat + row_idx, column=col_idx + 1, value=cell_value)

    workbook.save(output_path)