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

def get_vl_registered_samples_data(start_date: datetime, end_date: datetime):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    query = f"""
SELECT
       [LabName],
       [Total],
       [Registered],
       [Rejected],
       [StartDate],
       [EndDate],
       [UpdatedAt],
       [CreatedAt]
   FROM [ReportData].[dbo].[VLRegisteredSamples]
WHERE StartDate >= '{start_date_str}'
AND EndDate <= '{end_date_str}'
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
       [no_data],
       [StartDate],
       [EndDate],
       [UpdatedAt],
       [CreatedAt]
   FROM [ReportData].[dbo].[VLSamplesBacklog]
WHERE StartDate >= '{start_date_str}'
AND EndDate <= '{end_date_str}'
"""
    return execute_custom_query(query)