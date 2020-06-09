# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'googlephotoUIv2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import sys
from selenium import webdriver
import time
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from resources.credentials import password_decoder
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import ast
from datetime import datetime
import qdarkstyle
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
    if getattr(sys, 'frozen', False):
        pickle_path = os.path.join(sys._MEIPASS, f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
    else:
        pickle_path = f'resources/token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    pickle_file = pickle_path
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
    if getattr(sys, 'frozen', False):
        json_path = os.path.join(sys._MEIPASS, 'credentials.json')
    else:
        json_path = 'resources/credentials.json'
    CLIENT_SECRET_FILE = json_path
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
    def __init__(self):
        self._file_type = "both"
        self._number_of_files = 5
        self._album_name = "Điên Nà?"
        self._update_flag = False
        self._driver = initalLogin()
        self._date_list = []
        self._playerOnePoint = 0
        self._playerTwoPoint = 0
        self._date_list_index = 0
        self._tabs_to_delete = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        #MainWindow.setStyleSheet(open("style.qss", "r").read())
        MainWindow.resize(391, 222)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PhotoType = QtWidgets.QComboBox(self.centralwidget)
        self.PhotoType.setGeometry(QtCore.QRect(20, 80, 91, 31))
        self.PhotoType.setObjectName("PhotoType")
        self.PhotoType.addItem("")
        self.PhotoType.addItem("")
        self.PhotoType.addItem("")
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(280, 130, 91, 41))
        self.GenerateButton.setObjectName("GenerateButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15, 55, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(155, 55, 101, 21))
        self.label_2.setObjectName("label_2")
        self.UpdateAlbum = QtWidgets.QComboBox(self.centralwidget)
        self.UpdateAlbum.setGeometry(QtCore.QRect(280, 80, 91, 31))
        self.UpdateAlbum.setObjectName("UpdateAlbum")
        self.UpdateAlbum.addItem("")
        self.UpdateAlbum.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(275, 55, 91, 21))
        self.label_3.setObjectName("label_3")
        self.PhotoNumber = QtWidgets.QComboBox(self.centralwidget)
        self.PhotoNumber.setGeometry(QtCore.QRect(160, 80, 91, 31))
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
        self.label_5.setGeometry(QtCore.QRect(155, 30, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.PlayerOneDateGuess = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.PlayerOneDateGuess.setGeometry(QtCore.QRect(20, 220, 111, 24))
        self.PlayerOneDateGuess.setObjectName("PlayerOneDateGuess")

        self.PlayerTwoDateGuess = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.PlayerTwoDateGuess.setGeometry(QtCore.QRect(150, 220, 113, 24))
        self.PlayerTwoDateGuess.setObjectName("PlayerTwoDateGuess")

        self.PlayOneLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlayOneLabel.setGeometry(QtCore.QRect(20, 190, 71, 21))
        self.PlayOneLabel.setObjectName("PlayOneLabel")
        self.PhotoDateList = QtWidgets.QComboBox(self.centralwidget)
        self.PhotoDateList.setGeometry(QtCore.QRect(270, 220, 113, 24))
        self.PhotoDateList.setObjectName("PhotoDateList")
        self.PhotoDateLabel = QtWidgets.QLabel(self.centralwidget)
        self.PhotoDateLabel.setGeometry(QtCore.QRect(280, 190, 81, 21))
        self.PhotoDateLabel.setObjectName("PhotoDateLabel")
        self.PlayerOneName = QtWidgets.QLineEdit(self.centralwidget)
        self.PlayerOneName.setGeometry(QtCore.QRect(20, 140, 121, 21))
        self.PlayerOneName.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.PlayerOneName.setAlignment(QtCore.Qt.AlignCenter)
        self.PlayerOneName.setObjectName("PlayerOneName")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 120, 111, 20))
        self.label_4.setObjectName("label_4")
        self.PlayerTwoName = QtWidgets.QLineEdit(self.centralwidget)
        self.PlayerTwoName.setGeometry(QtCore.QRect(150, 140, 121, 21))
        self.PlayerTwoName.setText("")

        self.PlayerOneScore = QtWidgets.QLineEdit(self.centralwidget)
        self.PlayerOneScore.setGeometry(QtCore.QRect(90, 190, 41, 20))
        self.PlayerOneScore.setText("")

        self.PlayerTwoScore = QtWidgets.QLineEdit(self.centralwidget)
        self.PlayerTwoScore.setGeometry(QtCore.QRect(220, 190, 41, 20))
        self.PlayerTwoScore.setText("")

        self.PlayerTwoName.setAlignment(QtCore.Qt.AlignCenter)
        self.PlayerTwoName.setObjectName("PlayerTwoName")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(160, 120, 111, 20))
        self.label_6.setObjectName("label_6")
        # self.PlayerOneSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        # self.PlayerOneSpinBox.setGeometry(QtCore.QRect(90, 190, 41, 20))
        # self.PlayerOneSpinBox.setObjectName("PlayerOneSpinBox")
        # self.PlayerTwoSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        # self.PlayerTwoSpinBox.setGeometry(QtCore.QRect(220, 190, 41, 20))
        # self.PlayerTwoSpinBox.setObjectName("PlayerTwoSpinBox")
        self.PlayerTwoLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlayerTwoLabel.setGeometry(QtCore.QRect(150, 190, 71, 21))
        self.PlayerTwoLabel.setObjectName("PlayerTwoLabel")
        self.CalculateButton = QtWidgets.QPushButton(self.centralwidget)
        self.CalculateButton.setGeometry(QtCore.QRect(160, 260, 91, 41))
        self.CalculateButton.setObjectName("CalculateButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 391, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.PlayOneLabel.hide()
        self.PlayerTwoLabel.hide()
        self.PlayerOneScore.hide()
        self.PlayerTwoScore.hide()
        self.PlayerOneDateGuess.hide()
        self.PlayerTwoDateGuess.hide()
        self.PhotoDateLabel.hide()
        self.PhotoDateList.hide()
        self.CalculateButton.hide()

        self.GenerateButton.clicked.connect(self.gen_pressed)
        self.CalculateButton.clicked.connect(self.cal_pressed)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PhotoType.setItemText(0, _translate("MainWindow", "Both"))
        self.PhotoType.setItemText(1, _translate("MainWindow", "Videos"))
        self.PhotoType.setItemText(2, _translate("MainWindow", "Images"))
        self.GenerateButton.setText(_translate("MainWindow", "Generate"))
        self.label.setText(_translate("MainWindow", "Photo Type"))
        self.label_2.setText(_translate("MainWindow", "Photos Number"))
        self.UpdateAlbum.setItemText(0, _translate("MainWindow", "False"))
        self.UpdateAlbum.setItemText(1, _translate("MainWindow", "True"))
        self.label_3.setText(_translate("MainWindow", "Update Album"))
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
        self.PlayOneLabel.setText(_translate("MainWindow", "NameOne"))
        self.PhotoDateLabel.setText(_translate("MainWindow", "Photo Date:"))
        self.label_4.setText(_translate("MainWindow", "Player One Name"))
        self.label_6.setText(_translate("MainWindow", "Player Two Name"))
        self.PlayerTwoLabel.setText(_translate("MainWindow", "NameTwo"))
        self.CalculateButton.setText(_translate("MainWindow", "Calculate"))
        self.PlayerOneDateGuess.setDisplayFormat(_translate("MainWindow", "yyyy/mm/dd"))
        self.PlayerTwoDateGuess.setDisplayFormat(_translate("MainWindow", "yyyy/mm/dd"))

    def gen_pressed(self):
        MainWindow.resize(391, 340)
        self.PlayOneLabel.show()
        self.PlayerTwoLabel.show()
        self.PlayerOneScore.show()
        self.PlayerTwoScore.show()
        self.PlayerOneDateGuess.show()
        self.PlayerTwoDateGuess.show()
        self.PhotoDateLabel.show()
        self.PhotoDateList.show()
        self.CalculateButton.show()

        _translate = QtCore.QCoreApplication.translate
        PlayerOneName = self.PlayerOneName.text()
        PlayerTwoName = self.PlayerTwoName.text()
        print(PlayerOneName, PlayerTwoName)
        self.PlayOneLabel.setText(_translate("MainWindow", PlayerOneName))
        self.PlayerTwoLabel.setText(_translate("MainWindow", PlayerTwoName))

        self._file_type = self.PhotoType.currentText()
        self._number_of_files = int(self.PhotoNumber.currentText())

        if self.UpdateAlbum.currentText() == "False":
            self._update_flag = bool("")
        else:
            self._update_flag = bool("True")
        print(self._file_type, self._number_of_files, self._update_flag)

        # append the exisiting list to a new generated list
        self._date_list.extend(self.photo_fetch(self._file_type, self._number_of_files, self._update_flag))
        print(self._date_list)

    def cal_pressed(self):
        try:
            date_list = [datetime.strptime(x, '%Y/%m/%d') for x in self._date_list]
            try:
                playerOneDate = datetime.strptime(self.PlayerOneDateGuess.text(), '%Y/%m/%d')
                playerTwoDate = datetime.strptime(self.PlayerTwoDateGuess.text(), '%Y/%m/%d')
                playerOneDelta = abs(date_list[self._date_list_index] - playerOneDate)
                playerTwoDelta = abs(date_list[self._date_list_index] - playerTwoDate)

                if playerOneDelta.days < playerTwoDelta.days:
                    #self.PlayerTwoSpinBox.stepBy(1)
                    self.PlayerOneScore.setText(str(self._playerOnePoint + 1))
                    self._playerOnePoint += 1

                else:
                    self.PlayerTwoScore.setText(str(self._playerTwoPoint + 1))
                    self._playerTwoPoint += 1
                print(playerOneDelta, " ", playerTwoDelta)
                _translate = QtCore.QCoreApplication.translate
                self.PhotoDateList.addItem("")
                self.PhotoDateList.setItemText(self._date_list_index,
                                               _translate("MainWindow", self._date_list[self._date_list_index]))
                self._date_list_index += 1
                MainWindow.show()
            except ValueError:
                print("Please take a guess for the date")
        except IndexError:
            print("No more photos to play, click Generate for more!")

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

        if getattr(sys, 'frozen', False):
            csv_path = os.path.join(sys._MEIPASS, "DienNa_photos_metadata.csv")
        else:
            csv_path = "resources/DienNa_photos_metadata.csv"

        if _update_flag:
            lst_medias = update(self._album_name)
            df_media_items = pd.DataFrame(lst_medias)
            df_media_items.to_csv(csv_path)
        else:
            df_media_items = pd.read_csv(csv_path)

        df_media_items = df_media_items.sample(frac=1).reset_index(drop=True)

        print(_file_type)
        df_media_items = df_media_items[df_media_items.mimeType.str.contains(_file_type)].reset_index()
        photo_dates_list = []
        for x in range(_number_of_files):
            url = df_media_items.loc[x].productUrl
            photo_dict = ast.literal_eval(df_media_items.loc[x].mediaMetadata)
            photo_dates_list.append(photo_dict["creationTime"][:10].replace("-", "/"))
            self._driver.execute_script("window.open('" + url + "')")

        # Delete the previous n number of tabs
        for x in range(self._tabs_to_delete):
            self._driver.switch_to.window(window_name=self._driver.window_handles[0])
            self._driver.close()
            self._driver.switch_to.window(window_name=self._driver.window_handles[0])
        # Switch to the first tab
        self._driver.switch_to.window(window_name=self._driver.window_handles[-1])
        self._tabs_to_delete = _number_of_files

        return photo_dates_list

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
    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver")
        driver = webdriver.Chrome(chromedriver_path)
    else:
        driver = webdriver.Chrome(executable_path="./resources/chromedriver", chrome_options=options)
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
