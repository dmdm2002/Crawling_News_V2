import re
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QLineEdit, QCheckBox, QComboBox, QMessageBox
from get_News_item import Crawling_news
import pandas as pd
from UpLoadModule import naver_login
import time
import os


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.crawling_type = 0

    def setupUi(self):
        os.makedirs('./txts', exist_ok=True)
        self.setWindowTitle('News Crawler')
        self.resize(500, 500)

        temp = os.listdir('./txts')

        load_id = ''
        load_pw = ''
        tags = ''
        keywork = ''
        count = ''

        for name in temp:
            if name == 'login_info.txt':
                login_info = []
                f = open(f'./txts/{name}', 'r')
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    login_info.append(line)
                load_id = login_info[0]
                load_pw = login_info[1]

            elif name == 'current_tags.txt':
                f = open(f'./txts/{name}', 'r', encoding='utf8')
                tags = f.read()
                tags = re.compile('  ').sub(',', tags)
                tags = re.compile(' ').sub('', tags)

            elif name == 'current_keyword.txt':
                f = open(f'./txts/{name}', 'r', encoding='utf8')
                keywork = f.read()

            elif name == 'current_count.txt':
                f = open(f'./txts/{name}', 'r', encoding='utf8')
                count = f.read()


        self.line_edit_keyword = QLineEdit(self)
        self.line_edit_keyword.move(75, 75)
        self.line_edit_keyword.setText(keywork)

        self.line_deit_counter = QLineEdit(self)
        self.line_deit_counter.move(75, 125)
        self.line_deit_counter.setText(count)

        self.line_deit_id = QLineEdit(self)
        self.line_deit_id.move(75, 175)
        self.line_deit_id.setText(load_id)

        self.line_deit_pwd = QLineEdit(self)
        self.line_deit_pwd.setEchoMode(QLineEdit.Password)
        self.line_deit_pwd.move(75, 225)
        self.line_deit_pwd.setText(load_pw)

        self.line_deit_tag = QLineEdit(self)
        self.line_deit_tag.move(75, 275)
        self.line_deit_tag.setText(tags)

        self.text_label_keywork = QLabel(self)
        self.text_label_keywork.move(75, 60)
        self.text_label_keywork.setText('키워드')

        self.text_label_counter = QLabel(self)
        self.text_label_counter.move(75, 110)
        self.text_label_counter.setText('개수')

        self.text_label_id = QLabel(self)
        self.text_label_id.move(75, 160)
        self.text_label_id.setText('아이디')

        self.text_label_pwd = QLabel(self)
        self.text_label_pwd.move(75, 210)
        self.text_label_pwd.setText('비밀번호')

        self.text_label_tag = QLabel(self)
        self.text_label_tag.move(75, 260)
        self.text_label_tag.setText('태그')

        """ 버튼 """
        self.button_csv = QPushButton(self)
        self.button_csv.move(130, 320)
        self.button_csv.setText('Export CSV file')
        self.button_csv.clicked.connect(self.button_event_df2csv)

        self.button_cafe = QPushButton(self)
        self.button_cafe.move(50, 320)
        self.button_cafe.setText('Export cafe')
        self.button_cafe.clicked.connect(self.button_event_write_blog)

        """ 키워드 저장 """
        self.keywork_checkBox = QCheckBox(self)
        self.keywork_checkBox.move(250, 160)
        self.keywork_checkBox.stateChanged.connect(self.keywork_saveAction)

        self.keywork_checklabel = QLabel(self)
        self.keywork_checklabel.move(270, 160)
        self.keywork_checklabel.setText('현재 키워드 저장')

        """ 개수 저장 """
        self.countCheckBox = QCheckBox(self)
        self.countCheckBox.move(250, 190)
        self.countCheckBox.stateChanged.connect(self.count_saveAction)

        self.countChecklabe = QLabel(self)
        self.countChecklabe.move(270, 190)
        self.countChecklabe.setText('현재 개수 저장')

        """ 계정 저장 """
        self.checkbox = QCheckBox(self)
        self.checkbox.move(250, 220)
        self.checkbox.stateChanged.connect(self.login_info_box_changeAction)

        self.labelA = QLabel(self)
        self.labelA.move(270, 220)
        self.labelA.setText('계정 정보 저장')

        # """ Login Info Loader """
        # self.loader_box = QCheckBox(self)
        # self.loader_box.move(250, 170)
        # self.loader_box.stateChanged.connect(self.login_info_loadAction)
        #
        # self.labelB = QLabel(self)
        # self.labelB.move(270, 170)
        # self.labelB.setText('최근 계정 가져오기')

        """ tag Loader """
        self.tag_save = QCheckBox(self)
        self.tag_save.move(250, 250)
        self.tag_save.stateChanged.connect(self.tag_box_saveAction)

        self.tag_A = QLabel(self)
        self.tag_A.move(270, 250)
        self.tag_A.setText('현재 태그 저장')

        # self.tag_box = QCheckBox(self)
        # self.tag_box.move(250, 230)
        # self.tag_box.stateChanged.connect(self.tag_loadAction)
        #
        # self.tag_B = QLabel(self)
        # self.tag_B.move(270, 230)
        # self.tag_B.setText('최근 태그 가져오기')

        """ Crawling Type """
        type_cb = QComboBox(self)
        type_cb.addItem('전부 크롤링')
        type_cb.addItem('제목에 키워드 포함')
        type_cb.addItem('본문에 키워드 포함')
        type_cb.move(250, 100)
        type_cb.activated[str].connect(self.select_type)

        self.show()

    def select_type(self, text):
        if text == '전부 크롤링':
            self.crawling_type = 0
        elif text == '제목에 키워드 포함':
            self.crawling_type = 1
        elif text == '본문에 키워드 포함':
            self.crawling_type = 2

    def button_event_df2csv(self):
        text_keyword = self.line_edit_keyword.text()  # line_edit text 값 가져오기
        text_counter = self.line_deit_counter.text()  # line_edit text 값 가져오기

        crawling = Crawling_news(text_keyword, int(text_counter), self.crawling_type)
        urls, names = crawling.get_item()

        print(urls)
        print(names)

        newsDic = {
            'addresses': urls,
            'names' : names
        }

        df = pd.DataFrame(newsDic)
        ctime = time.strftime("%Y_%m_%d_%H%M%S")
        path = './csv_files'
        os.makedirs(path, exist_ok=True)
        df.to_csv(f'{path}/{ctime}.csv', encoding='utf-8-sig')
        QMessageBox.about(self, 'Finish', 'csv로 저장 완료!')

        print('Save Csv Finish!!!')

    def button_event_write_blog(self):
        text_keyword = self.line_edit_keyword.text()  # line_edit text 값 가져오기
        text_counter = self.line_deit_counter.text()  # line_edit text 값 가져오기
        id = self.line_deit_id.text()
        pwd = self.line_deit_pwd.text()
        tags = self.line_deit_tag.text()

        crawling = Crawling_news(text_keyword, int(text_counter), self.crawling_type)
        urls, names = crawling.get_item()

        naver_login(names, urls, id, pwd, tags)
        QMessageBox.about(self, 'Finish', '업로드 완료!')

        print('Finish Upload!!!')

    def login_info_box_changeAction(self, state):
        id = self.line_deit_id.text()
        pwd = self.line_deit_pwd.text()

        if state == 2:
            if id == '' or pwd == '':
                QMessageBox.about(self, 'Warning', '아이디와 비밀번호를 입력하고 박스를 다시 체크해주세요')

            else:
                with open('./txts/login_info.txt', 'w') as file:
                    file.write(f'{id}\n')
                    file.write(f'{pwd}')
                print('ID/PWD 저장 완료!')

        else:
            pass

    # def login_info_loadAction(self, state):
    #     login_info = []
    #     if state == 2:
    #         f = open('./txts/login_info.txt', 'r')
    #         lines = f.readlines()
    #         for line in lines:
    #             line = line.strip()
    #             login_info.append(line)
    #
    #         self.line_deit_id.setText(login_info[0])
    #         self.line_deit_pwd.setText(login_info[1])
    #
    #     else:
    #         pass

    def tag_box_saveAction(self, state):
        tags = self.line_deit_tag.text()

        if state == 2:
            if tags == '':
                QMessageBox.about(self, 'Warning', '태그를 입력하세요')

            else:
                tag_list = tags.split(',')
                print(tag_list)
                with open('./txts/current_tags.txt', 'w', encoding='utf8') as file:
                    for tag in tag_list:
                        file.write(f' {tag} ')
                print('Tag 저장 완료!')

        else:
            pass

    # def tag_loadAction(self, state):
    #     if state == 2:
    #         f = open('./txts/current_tags.txt', 'r', encoding='utf8')
    #         tags = f.read()
    #         tags = re.compile(' ').sub(',', tags)
    #
    #         self.line_deit_tag.setText(tags)
    #
    #     else:
    #         pass
    def keywork_saveAction(self, state):
        keyword = self.line_edit_keyword.text()
        if state == 2:
            if keyword == '':
                QMessageBox.about(self, 'Warning', '키워드를 입력하세요')

            else:
                os.makedirs('./txts', exist_ok=True)
                with open('./txts/current_keyword.txt', 'w', encoding='utf8') as file:
                    file.write(f'{keyword}')
                print('키워드 저장 완료!')

        else:
            pass

    def count_saveAction(self, state):
        count = self.line_deit_counter.text()
        if state == 2:
            if count == '':
                QMessageBox.about(self, 'Warning', '개수를 입력하세요')

            else:
                os.makedirs('./txts', exist_ok=True)
                with open('./txts/current_count.txt', 'w', encoding='utf8') as file:
                    file.write(f'{count}')
                print('Tag 저장 완료!')

        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()

    sys.exit(app.exec_())