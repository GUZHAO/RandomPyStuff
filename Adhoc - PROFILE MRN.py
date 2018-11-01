import pandas
import cx_Oracle
import pprint

# Import PROFILE population's MRN
MRN_profile = pandas.read_excel(
    "//cifs2/coba$/Ad-Hoc Data Requests/Elia's Profile Population/MRNS_Sequenced_031918.xlsx",
    sheet_name=1, dtype={'DFCI_MRN': str})
print(MRN_profile.count())  # Check row count -- passed
print(MRN_profile['DFCI_MRN'].str.len().unique())  # Check whether MRN is only 6 digits -- passed

MRN_outpatient = pandas.read_excel(
    "//cifs2/coba$/Ad-Hoc Data Requests/Elia's Profile Population/Outpatient_Population.xlsx",
    sheet_name=0, dtype={'DFCI_MRN': str})
print(MRN_outpatient.count())  # Check row count -- passed

connection = cx_Oracle.connect("COBATABLEAU", "Bobby1234", "dfcinp01-scan:1521/dartprdo")
cursor = connection.cursor()
cursor.execute(
    """
SELECT DISTINCT
  t2.PT_DFCI_MRN,
  CASE WHEN t2.ENC_LOC_NM_DV = 'DANA-FARBER CANCER INSTITUTE LONGWOOD' THEN 'MAIN CAMPUS'
    ELSE 'SATELLITE' END AS SITE,
  t3.PT_DEATH_DT
FROM dart_ods.ods_edw_enc_pt_enc t1
  LEFT JOIN DART_ODS.MV_COBA_PT_ENC t2 ON t1.PT_ID = t2.PT_ID
  LEFT JOIN DART_ODS.MV_COBA_PT t3 ON t1.PT_ID = t3.PT_ID
WHERE
  t1.PT_ID IN (
    SELECT pe.pt_id
    FROM dart_ods.mv_coba_pt_enc pe
    WHERE pe.enc_status_descr IN ('ARRIVED', 'COMPLETED')
          AND pe.enc_loc_nm_dv IN (
      'DANA-FARBER CANCER INSTITUTE LONGWOOD',
      'DANA-FARBER AT ST. ELIZABETH MEDICAL CENTER',
      'DANA-FARBER BWCC AT MILFORD REGIONAL MEDICAL CENTER',
      'DANA-FARBER BWCC SOUTH SHORE CANCER CENTER',
      'DANA-FARBER LONDONDERRY'
    )) AND t2.ENC_LOC_NM_DV IN (
    'DANA-FARBER CANCER INSTITUTE LONGWOOD',
    'DANA-FARBER AT ST. ELIZABETH MEDICAL CENTER',
    'DANA-FARBER BWCC AT MILFORD REGIONAL MEDICAL CENTER',
    'DANA-FARBER BWCC SOUTH SHORE CANCER CENTER',
    'DANA-FARBER LONDONDERRY')
AND CONT_DTTM >= :dt
    """, dt='1-JAN-17'
)

# export result to csv file
with open("//cifs2/coba$/Ad-Hoc Data Requests/Elia's Profile Population/" + timestr + '.csv', "w",
          newline='') as csvfile:
    output = csv.writer(csvfile)
    output.writerow(["DFCI_MRN", "Site", "Death_Date"])
    for row in cursor:
        output.writerow(row)

# close Oracle connection
cursor.close()
connection.close()