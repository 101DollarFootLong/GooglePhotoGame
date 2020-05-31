# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import pandas as pd
from selenium import webdriver
import time
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from credentials import password_decoder
from selenium.webdriver.common.keys import Keys
import config

pd.set_option('display.max_colwidth', 150)

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def update():
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'photoslibrary'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    myAblums = service.albums().list().execute()
    myAblums_list = myAblums.get('albums')
    dfAlbums = pd.DataFrame(myAblums_list)
    album_name = "Điên Nà?"
    travel_album_id = dfAlbums[dfAlbums['title'] == album_name]['id'].to_string(index=False).strip()

    response = service.mediaItems().search(body={"albumId": travel_album_id, "pageSize": 25}).execute()

    lst_medias = response.get('mediaItems')

    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.mediaItems().search(body={"albumId": travel_album_id,
                                                     "pageSize": 25,
                                                     "pageToken": nextPageToken}).execute()

        lst_medias.extend(response.get('mediaItems'))

        nextPageToken = response.get('nextPageToken')
    return lst_medias

# User custom field
update_flag = config.user_config["update_flag"]
file_type = config.user_config["file_type"]
number_of_files = config.user_config["number_of_files"]
if file_type == "both":
    file_type = ""

if update_flag:
    lst_medias = update()
    df_media_items = pd.DataFrame(lst_medias)
    df_media_items.to_csv(f"DienNa_photos_metadata.csv")
else:
    df_media_items = pd.read_csv('DienNa_photos_metadata.csv')

df_media_items = df_media_items.sample(frac=1).reset_index(drop=True)

df_media_items = df_media_items[df_media_items.mimeType.str.contains(file_type)].reset_index()

driver = webdriver.Chrome(executable_path="./chromedriver")

username, password = password_decoder()

for x in range(number_of_files):
    url = df_media_items.loc[x].productUrl
    if x == 0:
        driver.get(url)
        inputElement = driver.find_element_by_xpath('//*[@id="identifierId"]')
        inputElement.send_keys(username)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(1)
        passwordElement = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        passwordElement.send_keys(password)
        passwordElement.send_keys(Keys.ENTER)
        time.sleep(2)
    else:
        driver.execute_script("window.open('" + url + "')")
