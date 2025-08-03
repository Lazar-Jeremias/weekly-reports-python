from utils.db_connector import get_db_connection, execute_custom_query

def get_eid_samples_backlog_data(start_date, end_date):
    query = f"""
    SELECT 
        [LabName] 
       ,[Total] 
       ,[<7] 
       ,[7-15] 
       ,[15-21] 
       ,[>21] 
       ,[no_data] 
    FROM [ReportData].[dbo].[EIDSamplesBacklogs] 
    WHERE StartDate >= '{start_date.strftime('%Y-%m-%d')}' 
    AND EndDate <= '{end_date.strftime('%Y-%m-%d')}' 
    AND LabName NOT IN('HM Maputo') 
    ORDER BY LabName ASC
    """
    conn = get_db_connection()
    data = execute_custom_query(query)
    conn.close()
    return data


def get_eid_tested_samples_monitoria_data(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    query = f"""
    SELECT [LabName]
          ,[TotalTested]
          ,[<7]
          ,[7-15]
          ,[16-21]
          ,[>21]
          ,[no_data]
          ,[hub_lt_7]
          ,[hub_7_15]
          ,[hub_16_21]
          ,[hub_gt_21]
          ,[hub_no_data]
          ,[hub_registered_lt_7]
          ,[hub_registered_7_15]
          ,[hub_registered_16_21]
          ,[hub_registered_gt_21]
          ,[hub_registered_no_data]
          ,[registered_lt_7]
          ,[registered_btw_7_15]
          ,[registered_btw_16_21]
          ,[registered_gt_21]
          ,[tested_lt_2]
          ,[tested_btw_2_7]
          ,[tested_gt_7]
          ,[tat_lt_7]
          ,[tat_btw_7_15]
          ,[tat_btw_16_21]
          ,[tat_gt_21]
          ,[tat]
          ,[rejected]
          ,[NoSpecimenDate]
          ,[NoAge]
          ,[NoSex]
          ,[NoNid]
          ,[TotalPositivity]
      FROM [ReportData].[dbo].[EIDTestedSamplesPerWeek]
      WHERE StartDate >= '{start_date_str}'
      AND EndDate <= '{end_date_str}'
      AND LabName NOT IN('HM Maputo')
      ORDER BY LabName ASC
    """
    return execute_custom_query(query)

def get_eid_registered_samples_data(start_date, end_date):
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
      FROM [ReportData].[dbo].[EIDRegisteredSamples] 
      WHERE start_date >= '{start_date_str}' AND end_date <= '{end_date_str}' 
      AND lab_name NOT IN('HM Maputo') 
      ORDER BY lab_name ASC
    """
    return execute_custom_query(query)

def get_eid_tat_by_health_facility_data(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    query = f"""
    SELECT 
  	   B.[FacilityNationalCode] 
      ,B.Datim_ID
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
    FROM [ReportData].[dbo].[EIDTatByHealthFacility] A
    LEFT JOIN (
            SELECT  
                Datim_ID,
                Disa_Code,
                FacilityNationalCode
            FROM [OpenLDRDict].dbo.[Datim]
        ) B 
        ON A.RequestingFacilityCode = B.Disa_Code
        WHERE start_date >= '{start_date_str}' AND end_date <= '{end_date_str}' 
    ORDER BY ProvinceName ASC, DistrictName ASC, TypeOfTest ASC
    """
    return execute_custom_query(query)

def get_eid_transport_tat_data(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    query = f"""
    SELECT 
           B.[FacilityNationalCode] 
          ,B.Datim_ID
          ,[ProvinceName]
          ,[DistrictName]
          ,[RequestingFacilityName]
          ,[TestingFacilityName]
          ,[TypeOfTest]
          ,[TotalTestedSamples]
          ,[TestedSamplesWithCollectionDate]
          ,[collection_to_hub_lt_7]
          ,[collection_to_hub_7_15]
          ,[collection_to_hub_16_21]
          ,[collection_to_hub_gt_21]
          ,[collection_to_hub_no_data]
          ,[hub_reception_to_registration_lt_7]
          ,[hub_reception_to_registration_7_15]
          ,[hub_reception_to_registration_16_21]
          ,[hub_reception_to_registration_gt_21]
          ,[hub_reception_to_registration_no_data]
          ,[hub_to_lab_reception_lt_7]
          ,[hub_to_lab_reception_7_15]
          ,[hub_to_lab_reception_16_21]
          ,[hub_to_lab_reception_gt_21]
          ,[hub_to_lab_reception_no_data]
          ,[lab_reception_to_registration_lt_7]
          ,[lab_reception_to_registration_7_15]
          ,[lab_reception_to_registration_16_21]
          ,[lab_reception_to_registration_gt_21]
          ,[lab_reception_to_registration_no_data]
          ,[collection_to_lab_reception_lt_7]
          ,[collection_to_lab_reception_7_15]
          ,[collection_to_lab_reception_16_21]
          ,[collection_to_lab_reception_gt_21]
          ,[collection_to_lab_reception_no_data]
      FROM [ReportData].[dbo].[EIDTransportTATPerWeek] A
      LEFT JOIN (
            SELECT  
                Datim_ID,
                Disa_Code,
                FacilityNationalCode
            FROM [OpenLDRDict].dbo.[Datim]
        ) B 
        ON A.RequestingFacilityCode = B.Disa_Code
        WHERE start_date >= '{start_date_str}' AND end_date <= '{end_date_str}' 
    ORDER BY ProvinceName ASC, DistrictName ASC, TypeOfTest ASC
    """
    return execute_custom_query(query)
