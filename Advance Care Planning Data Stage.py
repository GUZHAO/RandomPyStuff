import pyodbc
import json
import sqlalchemy


def query():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=PHSEDW;DATABASE=Epic;')
    cursor = cnxn.cursor()
    return cursor.execute("""
    SELECT fsm.EDW_ID,
         p.PatientLastNM  AS LAST_NAME,
         p.PatientFirstNM AS FIRST_NAME,
         p.BirthDTS       AS DOB,
         p.SexDSC         AS GENDER,
         fsm.SER_ILL,
         fsm.SER_ILL_DISPALY,
         fsm.SER_ILL_CONV,
         fsm.MeasureCommentTXT,
         fsm.SER_ILL_CONV_AUTHOR,
         fsm.SER_ILL_CONV_DATE
FROM (SELECT fsrl.PatientID        AS EDW_ID,
						 fsm.ReceivedDTS,
						 fsm.RecordedDTS,
						 fg.FlowsheetMeasureNM AS SER_ILL,
						 fg.DisplayNM          AS SER_ILL_DISPALY,
						 fsm.MeasureTXT        AS SER_ILL_CONV,
						 fsm.MeasureCommentTXT,
						 e.UserNM              AS SER_ILL_CONV_AUTHOR,
						 fsm.EntryTimeDTS      AS SER_ILL_CONV_DATE
			FROM (SELECT *
						FROM Epic.Clinical.FlowsheetMeasure_DFCI
						WHERE FlowsheetMeasureID IN ('37901', '37902', '37903', '37948', '37905', '37906')) fsm
						 LEFT JOIN Epic.Person.Employee_DFCI e ON fsm.UserID = e.UserID
						 LEFT JOIN Epic.Clinical.FlowsheetGroup_DFCI fg ON fsm.FlowsheetMeasureID = fg.FlowsheetMeasureID
						 LEFT JOIN Epic.Clinical.FlowsheetRecordLink_DFCI fsrl ON fsm.FlowsheetDataID = fsrl.FlowsheetDataID
		 /*WHERE e.UserStatusCD <> 2*/) fsm
			 LEFT JOIN Epic.Patient.Patient_DFCI p ON fsm.EDW_ID = p.PatientID
WHERE P.TestFLG = 0
    """).fetchall()


# declare data
acp_data = []
rows = query()
for row in rows:
    acp_data.append({'EDW_ID': row[0],
                     'LAST_NAME': row[1],
                     'FIRST_NAME': row[2],
                     'DOB': row[3],
                     'GENDER': row[4],
                     'SER_ILL': row[5],
                     'SER_ILL_DISPLAY': row[6],
                     'SER_ILL_CONV': row[7],
                     'SER_ILL_CONV_COMM': row[8],
                     'SER_ILL_CONV_AUTHOR': row[9],
                     'SER_ILL_CONV_DATE': row[10],
                     })
with open('C:/Users/gz056/Downloads/acp.json', 'w') as outfile:
    json.dump(acp_data, outfile)
