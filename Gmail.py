from __future__ import print_function
import random
import string
import pickle
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def build_api():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_subject(idx):
    msgs = service.users().messages().get(userId=userId, id=idx, format="metadata").execute()
    details = msgs["payload"]["headers"]
    out = ["", "", ""]
    for detail in details:
        if detail["name"] == "Subject":
            out[0] = detail["value"]
        if detail["name"] == "From":
            out[1] = detail["value"]
        if detail["name"] == "Date":
            out[2] = detail["value"]
    return out

def get_idxs():
    results = service.users().messages().list(userId=userId, q=query, includeSpamTrash=True).execute()
    
    next_page = results["nextPageToken"]
    results = results["messages"]

    idxs = []
    for result in results:
        idxs.append(result["id"])

    while next_page is not None:
        results = service.users().messages().list(userId=userId, q=query, pageToken=next_page, includeSpamTrash=True).execute()

        if "nextPageToken" not in list(results.keys()):
            break

        next_page = results["nextPageToken"]
        results = results["messages"]
        for result in results:
            idxs.append(result["id"])

    return idxs

def words_in_sub(exclude_words, sub):
    for exclude_word in exclude_words:
        if exclude_word in sub:
            return True
    return False

def export_to_csv(subs):
    df = pd.DataFrame(subs, columns=["subject", "sender", "date"])
    file_path = f"result/subject_list_{user_name}.csv"
    df.to_csv(file_path, index=True, encoding="utf_8_sig")

def main():
    subs = []
    idxs = get_idxs()

    with open("exclude_words.txt") as f:
        exclude_words = f.readlines()
        exclude_words = [word.strip("\n").strip(" ") for word in exclude_words]

    for idx in idxs:
        sub = get_subject(idx)
        if not words_in_sub(exclude_words, sub[0]):
            print(sub)
            subs.append(sub)
            if len(subs) % 10 == 0:
                export_to_csv(subs)
                print(f"\n===============已儲存{len(subs)}筆eDM主旨===============\n")
    print(f"\n===============總共有{len(subs)}筆eDM主旨===============\n")
    

if __name__ == '__main__':
    service = build_api()
    userId = "me"
    user_name = "".join(random.choice(string.ascii_lowercase) for i in range(5))
    query = input("請輸入搜尋關鍵字：")
    if query == "None":
        query = None
    main()