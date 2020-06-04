# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
import time
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from credentials import password_decoder
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

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


def update(album_name):
    """
    Create a list from the photos in a given album
    :param album_name:
    :return: A list with all the photos metadata
    """
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'photoslibrary'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    myAblums = service.albums().list().execute()
    myAblums_list = myAblums.get('albums')
    dfAlbums = pd.DataFrame(myAblums_list)
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


class Ui_MainWindow(object):
    def __init__(self, _file_type=None, _number_of_files=None, _album_name=None, _update_flag=None, _driver=None):
        if _file_type is None:
            self._file_type = "both"
        if _number_of_files is None:
            self._number_of_files = 5
        if _album_name is None:
            self._album_name = "Điên Nà?"
        if _update_flag is None:
            self._update_flag = False
        if _driver is None:
            self._driver = initalLogin()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(399, 255)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PhotoType = QtWidgets.QComboBox(self.centralwidget)
        self.PhotoType.setGeometry(QtCore.QRect(30, 90, 91, 41))
        self.PhotoType.setObjectName("PhotoType")
        self.PhotoType.addItem("")
        self.PhotoType.addItem("")
        self.PhotoType.addItem("")
        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(90, 150, 211, 61))
        self.SubmitButton.setObjectName("SubmitButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 70, 131, 20))
        self.label_2.setObjectName("label_2")
        self.UpdateAlbum = QtWidgets.QComboBox(self.centralwidget)
        self.UpdateAlbum.setGeometry(QtCore.QRect(280, 80, 91, 61))
        self.UpdateAlbum.setObjectName("UpdateAlbum")
        self.UpdateAlbum.addItem("")
        self.UpdateAlbum.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 70, 91, 16))
        self.label_3.setObjectName("label_3")
        self.PhotoNumber = QtWidgets.QComboBox(self.centralwidget)
        self.PhotoNumber.setGeometry(QtCore.QRect(150, 90, 91, 41))
        self.PhotoNumber.setObjectName("PhotoNumber")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.PhotoNumber.addItem("")
        self.Tittle = QtWidgets.QLabel(self.centralwidget)
        self.Tittle.setGeometry(QtCore.QRect(90, 0, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Tittle.setFont(font)
        self.Tittle.setObjectName("Tittle")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(150, 30, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 399, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.SubmitButton.clicked.connect(self.pressed)
        self.infolist = []
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PhotoType.setItemText(0, _translate("MainWindow", "Both"))
        self.PhotoType.setItemText(1, _translate("MainWindow", "Videos"))
        self.PhotoType.setItemText(2, _translate("MainWindow", "Images"))
        self.SubmitButton.setText(_translate("MainWindow", "Submit"))
        self.label.setText(_translate("MainWindow", "Photo Type:"))
        self.label_2.setText(_translate("MainWindow", "Photos Number:"))
        self.UpdateAlbum.setItemText(0, _translate("MainWindow", "False"))
        self.UpdateAlbum.setItemText(1, _translate("MainWindow", "True"))
        self.label_3.setText(_translate("MainWindow", "Update Album:"))
        self.PhotoNumber.setItemText(0, _translate("MainWindow", "1"))
        self.PhotoNumber.setItemText(1, _translate("MainWindow", "2"))
        self.PhotoNumber.setItemText(2, _translate("MainWindow", "3"))
        self.PhotoNumber.setItemText(3, _translate("MainWindow", "4"))
        self.PhotoNumber.setItemText(4, _translate("MainWindow", "5"))
        self.PhotoNumber.setItemText(5, _translate("MainWindow", "6"))
        self.PhotoNumber.setItemText(6, _translate("MainWindow", "7"))
        self.PhotoNumber.setItemText(7, _translate("MainWindow", "8"))
        self.PhotoNumber.setItemText(8, _translate("MainWindow", "9"))
        self.PhotoNumber.setItemText(9, _translate("MainWindow", "10"))
        self.Tittle.setText(_translate("MainWindow", "Google Photo Game"))
        self.label_5.setText(_translate("MainWindow", "Made by: Mam Ruoc"))

    def get_infolist(self):
        print(self.infolist)

    def pressed(self):
        self._file_type = self.PhotoType.currentText()
        self._number_of_files = int(self.PhotoNumber.currentText())

        if self.UpdateAlbum.currentText() == "False":
            self._update_flag = bool("")
        else:
            self._update_flag = bool("True")
        print(self._file_type, self._number_of_files, self._update_flag)
        self.photo_fetch(self._file_type, self._number_of_files, self._update_flag)


    def photo_fetch(self, _file_type, _number_of_files, _update_flag):
        """
        Get the photos information from an album. Open n number of photos based on the user inputs.
        :param _file_type: can be video/image/both
        :param _number_of_files: the amount of tab the driver will open
        :param _update_flag: if true, it will update the Dataframe based on the album from today.
        :return: None
        """

        if _file_type.lower() == "both":
            _file_type = ""
        else:
            _file_type = _file_type.lower().strip("s")

        if _update_flag:
            lst_medias = update(self._album_name)
            df_media_items = pd.DataFrame(lst_medias)
            df_media_items.to_csv(f"DienNa_photos_metadata.csv")
        else:
            df_media_items = pd.read_csv('DienNa_photos_metadata.csv')

        df_media_items = df_media_items.sample(frac=1).reset_index(drop=True)

        print(_file_type)
        df_media_items = df_media_items[df_media_items.mimeType.str.contains(_file_type)].reset_index()

        for x in range(_number_of_files):
            url = df_media_items.loc[x].productUrl
            self._driver.execute_script("window.open('" + url + "')")


    @property
    def driver(self):
        return self._driver


def initalLogin():
    """
    Create the inital login for the system so the same instance and use the same driver
    :return: the logged in driver
    """
    username, password = password_decoder()
    options = Options()
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
    driver.get(
        "https://accounts.google.com/signin/v2/identifier?continue..&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    inputElement = driver.find_element_by_xpath('//*[@id="identifierId"]')
    inputElement.send_keys(username)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(2)
    passwordElement = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    passwordElement.send_keys(password)
    passwordElement.send_keys(Keys.ENTER)
    time.sleep(1)

    # Open new window and close the log in window
    # https://www.facebook.com/LeThien.1997/videos/2716623988402212/
    url = "https://github.com/101DollarFootLong/GooglePhotoGame"
    driver.execute_script("window.open('" + url + "')")
    # Select the logged in window and close it
    window_name = driver.window_handles[0]
    driver.switch_to.window(window_name=window_name)
    driver.close()
    # Switch to the url window
    driver.switch_to.window(window_name=driver.window_handles[0])
    return driver


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    status = app.exec_()
    if status == 0:
        ui.driver.quit()
        sys.exit(status)
