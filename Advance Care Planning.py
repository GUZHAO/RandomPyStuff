import pyodbc
import json


def query():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=PHSEDW;DATABASE=Epic;')
    cursor = cnxn.cursor()
    return cursor.execute("""SELECT TOP 500 fsm.EDW_ID,
											MRN.MRN          AS DFCI_MRN,
											MRN.EMPI,
											fsm.RecordedDTS,
											fsm.ReceivedDTS,
											p.PatientLastNM  AS LAST_NAME,
											p.PatientFirstNM AS FIRST_NAME,
											p.BirthDTS       AS DOB,
											p.SexDSC         AS GENDER,
											hcp.HEALTH_PROXY_DATE,
											mol.MOLST_DATE,
											note.SCANNED_ACP_DATE,
											note.ACP_DATE,
											note.ACP_AUTHOR  AS ACP_NOTE_AUTHOR,
											fsm.SER_ILL,
											fsm.SER_ILL_CONV,
											fsm.SER_ILL_CONV_AUTHOR,
											fsm.SER_ILL_CONV_DATE
							 FROM (SELECT fsrl.PatientID        AS EDW_ID,
														fsm.ReceivedDTS,
														fsm.RecordedDTS,
														fg.FlowsheetMeasureNM AS SER_ILL,
														fsm.MeasureTXT        AS SER_ILL_CONV,
														e.UserNM              AS SER_ILL_CONV_AUTHOR,
														fsm.EntryTimeDTS      AS SER_ILL_CONV_DATE
										 FROM (SELECT *
													 FROM Epic.Clinical.FlowsheetMeasure_DFCI
													 WHERE FlowsheetMeasureID IN ('37901', '37902', '37903', '37948', '37905', '37906')) fsm
														LEFT JOIN Epic.Person.Employee_DFCI e ON fsm.UserID = e.UserID
														LEFT JOIN Epic.Clinical.FlowsheetGroup_DFCI fg
															ON fsm.FlowsheetMeasureID = fg.FlowsheetMeasureID
														LEFT JOIN Epic.Clinical.FlowsheetRecordLink_DFCI fsrl
															ON fsm.FlowsheetDataID = fsrl.FlowsheetDataID
										/*WHERE e.UserStatusCD <> 2*/) fsm
											LEFT JOIN Epic.Patient.Patient_DFCI p ON fsm.EDW_ID = p.PatientID
											LEFT JOIN Integration.EMPI.MRN_DFCI MRN ON p.EDWPatientID = MRN.EDWPatientID
											LEFT JOIN (SELECT MAX(di.ScannedDTS) AS HEALTH_PROXY_DATE, di.PatientID
																 FROM Epic.Encounter.DocumentInformation_DFCI di
																 WHERE di.DocumentTypeCD = '1000000'
																 GROUP BY di.PatientID) hcp ON fsm.EDW_ID = hcp.PatientID
											LEFT JOIN (SELECT MAX(di.ScannedDTS) AS MOLST_DATE, di.PatientID
																 FROM Epic.Encounter.DocumentInformation_DFCI di
																 WHERE di.DocumentTypeCD = '2010257'
																 GROUP BY di.PatientID) mol ON fsm.EDW_ID = mol.PatientID
											LEFT JOIN (SELECT * FROM (SELECT nt.PatientID,
																				nei.EntryDTS     AS SCANNED_ACP_DATE,
																				nei.NoteFiledDTS AS ACP_DATE,
																		    e.UserNM         AS ACP_AUTHOR,
																				ROW_NUMBER() OVER (PARTITION BY nt.PatientID ORDER BY nei.NoteFiledDTS DESC, nei.EntryDTS DESC) AS ROWNUMBER
																 FROM Epic.Clinical.Note_DFCI nt
																				LEFT JOIN Epic.Clinical.NoteEncounterInformation_DFCI nei
																					ON nt.NoteID = nei.NoteID
																				LEFT JOIN Epic.Person.Employee_DFCI e ON nei.AuthorUserID = e.UserID
																 WHERE nei.ChangedNoteTypeCD = '1000076') rk_note
                                 WHERE ROWNUMBER = 1
																 ) note ON fsm.EDW_ID = note.PatientID
							 WHERE MRN.StatusCD = 'A'
								 AND P.TestFLG = 0""").fetchall()


# declare data
acp_data = []
rows = query()
for row in rows:
    acp_data.append({'EDW_ID': row[0],
                     'DFCI_MRN': row[1],
                     'EMPI': row[2],
                     'RRCORD_DATE': row[3],
                     'RECEIVE_DATE': row[4],
                     'LAST_NAME': row[5],
                     'FIRST_NAME': row[6],
                     'DOB': row[7],
                     'GENDER': row[8],
                     'HEALTH_PROXY_DATE': row[9],
                     'MOLST_DATE': row[10],
                     'SCAN_ACP_DATE': row[11],
                     'ACP_DATE': row[12],
                     'ACP_NOTE_AUTHOR': row[13],
                     'SER_ILL': row[14],
                     'SER_ILL_CONV': row[15],
                     'SER_ILL_CONV_AUTHOR': row[16],
                     'SER_ILL_CONV_DATE': row[17],
                     })

with open('F:/data.json', 'w') as outfile:
    json.dump(acp_data, outfile)
