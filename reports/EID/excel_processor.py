import openpyxl

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from utils.date_utils import get_previous_week_dates, format_week_range

def populate_eid_report_template(template_path, output_path, data_sets):
    eid_samples_backlog_data = data_sets.get("EID Samples Backlog", [])
    # eid_tested_samples_data removido - não usado
    eid_tested_samples_monitoria_data = data_sets.get("EID Tested Samples Monitoria", [])
    eid_registered_samples_data = data_sets.get("EID Registered Samples", [])
    eid_tat_by_health_facility_data = data_sets.get("EID TRL by US", [])
    eid_transport_tat_data = data_sets.get("Tempo de Transporte", [])

    # Carrega o template
    workbook = load_workbook(template_path)

    # Amostras não processadas
    sheet_backlog = workbook['Amostras não processadas']
    start_row_backlog = 7  # Data starts at row 7

    start_date, end_date = get_previous_week_dates()
    week_range_str = format_week_range(start_date, end_date)

    # Populate weekly range string in 'Amostras não processadas' sheet
    for merged_cell_range in list(sheet_backlog.merged_cells.ranges):
        if 'B3' in str(merged_cell_range) or 'C3' in str(merged_cell_range):
            sheet_backlog.unmerge_cells(str(merged_cell_range))
    sheet_backlog.merge_cells('B3:E3')
    b3_cell = sheet_backlog['B3']
    b3_cell.value = f"Amostras não Processadas (Semana: {week_range_str})"
    b3_cell.alignment = Alignment(vertical='center', horizontal='center')

    # Get the list of labs in the same order as they appear in the Excel template
    template_labs = [
        'Cabo Delgado', 'Carmelo', 'Chimoio', 'Inhambane',
        'INS', 'Lichinga', 'Machava', 'Mavalane', 'Nampula',
        'Ponta Gea', 'Quelimane', 'Tete', 'Xai-Xai'
    ]

    # Create a mapping from lab name to backlog data for quick lookup
    backlog_data_map = {row['LabName']: row for row in eid_samples_backlog_data}

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

    # Populate 'Monitoria das Amostras' sheet
    sheet_monitoria = workbook['Monitoria das Amostras']
    lab_order_monitoria = [
        'Cabo Delgado', 'Carmelo', 'Chimoio', 'Inhambane',
        'INS', 'Lichinga', 'Machava', 'Mavalane', 'Nampula',
        'Ponta Gea', 'Quelimane', 'Tete', 'Xai-Xai'
    ]

    # New EID Monitoria query data columns - mapping to the new query fields
    monitoria_query_data_columns = [
        'TotalTested',
        '<7',
        '7-15', 
        '16-21',
        '>21',
        'no_data',
        'hub_lt_7',
        'hub_7_15',
        'hub_16_21',
        'hub_gt_21',
        'hub_no_data',
        'hub_registered_lt_7',
        'hub_registered_7_15',
        'hub_registered_16_21',
        'hub_registered_gt_21',
        'hub_registered_no_data',
        'registered_lt_7',
        'registered_btw_7_15',
        'registered_btw_16_21',
        'registered_gt_21',
        'tested_lt_2',
        'tested_btw_2_7',
        'tested_gt_7',
        'tat_lt_7',
        'tat_btw_7_15',
        'tat_btw_16_21',
        'tat_gt_21',
        'tat',
        'rejected',
        'NoSpecimenDate',
        'NoAge',
        'NoSex',
        'NoNid',
        'TotalPositivity'
    ]

    # Create data mapping for the new EID monitoria data
    monitoria_data_map = {row['LabName']: row for row in eid_tested_samples_monitoria_data}

    start_row_monitoria = 6
    start_col_monitoria = 2

    # Populate data from B6 to AI18 (35 columns total: B=2 to AI=35)
    for row_idx, lab_name in enumerate(lab_order_monitoria):
        row_data = monitoria_data_map.get(lab_name, {})
        for col_idx, col_name in enumerate(monitoria_query_data_columns):
            cell_value = row_data.get(col_name, 0)
            # Ensure null values are treated as zeros for proper summation
            if cell_value is None or cell_value == '':
                cell_value = 0
            sheet_monitoria.cell(row=start_row_monitoria + row_idx, column=start_col_monitoria + col_idx, value=cell_value)

    # Populate title for first table - only set value, keep existing formatting
    b2_cell = sheet_monitoria['B2']
    b2_cell.value = f"Amostras Testadas por Laboratório (Semana: {week_range_str})"

    # Populate title for "Amostras Registadas" table - only set value, keep existing formatting
    b22_cell = sheet_monitoria['B22']
    b22_cell.value = f"Amostras Registadas por Laboratório (Semana: {week_range_str})"

    # Populate EIDRegisteredSamples data in 'Monitoria das Amostras' sheet (B26 to L38)
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

    registered_samples_data_map = {row['lab_name']: row for row in eid_registered_samples_data}

    start_row_registered = 26
    start_col_registered = 2

    # Only populate data values, preserve all existing formatting
    for row_idx, lab_name in enumerate(lab_order_monitoria):
        row_data = registered_samples_data_map.get(lab_name, {})
        for col_idx, col_name in enumerate(registered_query_data_columns):
            cell_value = row_data.get(col_name, 0)
            # Ensure null values are treated as zeros for proper summation
            if cell_value is None or cell_value == '':
                cell_value = 0
            # Only set the value, preserve existing cell formatting
            sheet_monitoria.cell(row=start_row_registered + row_idx, column=start_col_registered + col_idx).value = cell_value

    # Populate 'TRL por US' sheet
    sheet_trl_us = workbook['TRL por US']
    start_row_trl_us = 6

    # Populate title for 'TRL por US' sheet - only set value, keep existing formatting
    b2_cell_trl = sheet_trl_us['B2']
    b2_cell_trl.value = f"Tempo de Resposta Laboratorial das Amostras por Unidade Sanitária (Semana: {week_range_str})"

    # Define the columns to be populated from the query result
    trl_us_columns = [
        'FacilityNationalCode',
        'Datim_ID',
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
    num_data_rows = len(eid_tat_by_health_facility_data)

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

        # Define columns where NULL or zero should be treated as empty for TRL por US (A, B, C, D, E, F, G, I, AI)
        empty_if_null_or_zero_columns = [
            'FacilityNationalCode',    # Coluna A
            'Datim_ID',                # Coluna B
            'ProvinceName',            # Coluna C
            'DistrictName',            # Coluna D
            'RequestingFacilityName',  # Coluna E
            'TestingFacilityName',     # Coluna F
            'TypeOfTest',              # Coluna G
            'rejected',                # Coluna I
            'tat'                      # Coluna AI
        ]

        # Populate data
        for row_idx, row_data in enumerate(eid_tat_by_health_facility_data):
            for col_idx, col_name in enumerate(trl_us_columns):
                cell_value = row_data.get(col_name)
                
                # Special treatment for specific columns - NULL or zero becomes empty
                if col_name in empty_if_null_or_zero_columns:
                    if cell_value is None or cell_value == 0 or cell_value == '0':
                        cell_value = ''
                else:
                    # For other columns, only NULL becomes empty
                    if cell_value is None:
                        cell_value = ''
                        
                sheet_trl_us.cell(row=start_row_trl_us + row_idx, column=col_idx + 1, value=cell_value)

    # Populate 'Tempo de Transporte' sheet
    sheet_transport_tat = workbook['Tempo de Transporte']
    start_row_transport_tat = 6

    # Populate title for 'Tempo de Transporte' sheet - only set value, keep existing formatting
    b2_cell_transport = sheet_transport_tat['B2']
    b2_cell_transport.value = f"Tempo de Transporte de Amostras por Unidade Sanitária (Semana: {week_range_str})"

    # Define the columns to be populated from the query result
    transport_tat_columns = [
        'FacilityNationalCode',
        'Datim_ID',
        'ProvinceName',
        'DistrictName',
        'RequestingFacilityName',
        'TestingFacilityName',
        'TypeOfTest',
        'TotalTestedSamples',
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
    num_data_rows_transport = len(eid_transport_tat_data)

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

        # Define columns where NULL or zero should be treated as empty for Tempo de Transporte (A, B, C, D, E, F, G)
        transport_empty_if_null_or_zero_columns = [
            'FacilityNationalCode',    # Coluna A
            'Datim_ID',                # Coluna B
            'ProvinceName',            # Coluna C
            'DistrictName',            # Coluna D
            'RequestingFacilityName',  # Coluna E
            'TestingFacilityName',     # Coluna F
            'TypeOfTest'               # Coluna G
        ]

        # Populate data
        for row_idx, row_data in enumerate(eid_transport_tat_data):
            for col_idx, col_name in enumerate(transport_tat_columns):
                cell_value = row_data.get(col_name)
                
                # Special treatment for specific columns - NULL or zero becomes empty
                if col_name in transport_empty_if_null_or_zero_columns:
                    if cell_value is None or cell_value == 0 or cell_value == '0':
                        cell_value = ''
                else:
                    # For other columns, only NULL becomes empty
                    if cell_value is None:
                        cell_value = ''
                        
                sheet_transport_tat.cell(row=start_row_transport_tat + row_idx, column=col_idx + 1, value=cell_value)

    workbook.save(output_path)