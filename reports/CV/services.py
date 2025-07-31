from utils.db_connector import execute_custom_query
from datetime import datetime

def get_samples_instruments_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
SELECT 
    [LabName],
    [Instrument],
    [VL],
    [EID],
    [StartDate],
    [EndDate]
FROM [ReportData].[dbo].[SamplesInstruments]
WHERE StartDate >= '{start_date_str}'
AND EndDate <= '{end_date_str}'
AND Instrument <> 'MPIMA'
ORDER BY LabName ASC
"""
    return execute_custom_query(query)

def get_vl_samples_backlog_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
SELECT
       [LabName],
       [Total],
       [<7],
       [7-15],
       [15-21],
       [>21],
       [no_data]
   FROM [ReportData].[dbo].[VLSamplesBacklog]
WHERE StartDate >= '{start_date_str}'
AND EndDate <= '{end_date_str}'
AND LabName NOT IN('HM Maputo')
ORDER BY LabName ASC
"""
    return execute_custom_query(query)

# from utils.db_connector import execute_custom_query

def get_vl_samples_tested_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
        SELECT
            [lab_name]
           ,[total_samples]
           ,[collection_less_than_7]
           ,[collection_btwn_7_and_15]
           ,[collection_btwn_16_and_21]
           ,[collection_greater_than_21]
           ,[collection_no_data]
           ,[registration_less_than_7]
           ,[registration_btwn_7_and_15]
           ,[registration_btwn_16_and_21]
           ,[registration_greater_than_21]
           ,[testing_less_than_2]
           ,[testing_btwn_2_and_7]
           ,[testing_greater_than_7]
           ,[tat_less_than_7]
           ,[tat_btwn_7_and_15]
           ,[tat_btwn_16_and_21]
           ,[tat_greater_than_21]
           ,[tat_average]
           ,[no_collection_date]
           ,[no_age]
           ,[no_sex]
         FROM [ReportData].[dbo].[VLSamplesTested]
         WHERE start_date >= '{start_date_str}' AND end_date <= '{end_date_str}'
         AND lab_name NOT IN('HM Maputo')
         ORDER BY lab_name ASC
    """
    data = execute_custom_query(query)
    print("Dados de VLSamplesTested:", data)
    return data

def get_vl_registered_samples_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
SELECT 
        [lab_name] 
       ,[registered] 
       ,[collection_lt_7] 
       ,[collection_7_15] 
       ,[collection_16_21] 
       ,[collection_gt_21] 
       ,[no_specimen_date] 
       ,[testing_lt_7] 
       ,[testing_7_15] 
       ,[testing_16_21] 
       ,[testing_gt_21] 
       ,[no_testing_date] 
   FROM [ReportData].[dbo].[VLRegisteredSamples] 
   WHERE start_date >= '{start_date_str}' AND end_date <= '{end_date_str}' 
 AND lab_name NOT IN('HM Maputo') 
 ORDER BY lab_name ASC
    """
    data = execute_custom_query(query)
    # print("Dados de VLRegisteredSamples:", data)
    return data

def get_vl_tat_by_health_facility_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
SELECT 
 	    [FacilityNationalCode] 
       ,[RequestingFacilityCode] 
       ,[ProvinceName] 
       ,[DistrictName] 
       ,[RequestingFacilityName] 
       ,[TestingFacilityName] 
       ,[TypeOfTest] 
       ,[TotalTestedSamples] 
 	   ,[rejected] 
       ,[TestedSamplesWithCollectionDate] 
       ,[collected_lt_7] 
       ,[collected_7_15] 
       ,[collected_16_21] 
       ,[collected_gt_21] 
       ,[collected_no_data] 
       ,[received_lt_7] 
       ,[received_7_15] 
       ,[received_16_21] 
       ,[received_gt_21] 
       ,[received_no_data] 
       ,[registered_lt_7] 
       ,[registered_7_15] 
       ,[registered_16_21] 
       ,[registered_gt_21] 
       ,[registered_no_data] 
       ,[tested_lt_2] 
       ,[tested_2_7] 
       ,[tested_gt_7] 
       ,[tested_no_data] 
       ,[total_lt_7] 
       ,[total_7_15] 
       ,[total_16_21] 
       ,[total_gt_21] 
       ,[total_no_data] 
       ,[tat] 
 FROM [ReportData].[dbo].[VLTatByHealthFacility] 
 WHERE startdate >= '{start_date_str}' AND enddate <= '{end_date_str}' 
 ORDER BY [TypeOfTest] ASC, [TestingFacilityName] ASC
    """
    data = execute_custom_query(query)
    print("Dados de VLTatByHealthFacility:", data)
    return data

