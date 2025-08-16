import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADER = ["source","company","title","location","remote","posted_date","apply_url","req_id",
          "recruiter_name","recruiter_email","recruiter_link","skills","jd_text",
          "status","notes","cover_letter_path","resume_path","email_status"]

def open_sheet(sheet_id: str):
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    ws = sh.sheet1
    # ensure header
    row1 = ws.row_values(1)
    if row1 != HEADER:
        ws.clear()
        ws.append_row(HEADER)
    return ws

def append_jobs(ws, jobs):
    rows = []
    for j in jobs:
        rows.append([j.source, j.company, j.title, j.location, j.remote, j.posted_date,
                     j.apply_url, j.req_id, j.recruiter_name, j.recruiter_email,
                     j.recruiter_link, ", ".join(j.skills), j.jd_text, "New", "", "", "", ""])
    if rows:
        ws.append_rows(rows, value_input_option="RAW")