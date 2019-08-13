from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
import urllib.request
import urllib.parse
import sys

local_name = ['선택하세요','전국', '서울,경기도', '강원도', '충청북도','충청남도','경상북도','전라북도','전라남도','경상남도','제주도']
local_code = [000, 108,109,105,131,133,143,146,156,159,184]

class WeatherWindow(QWidget) :
    def __init__(self):
        super().__init__()
        self.expr = ""

        self.initWidget()
        self.initLayout()
        self.initEvent()

    def initWidget(self):
        self.locallbl = QLabel('지역')
        self.localCode = QComboBox()

        self.citylbl = QLabel('도시')
        self.cityCode = QComboBox()

        self.timelbl = QLabel('시간')
        self.timeCode = QComboBox()

        self.output = QTextEdit()

        self.btn_ok = QPushButton('검색')

        self.localCode.addItems(local_name)
        

    def initLayout(self):
        self.grid = QGridLayout()

        self.grid.addWidget(self.locallbl,0,0)
        self.grid.addWidget(self.citylbl,0,1)
        self.grid.addWidget(self.timelbl,0,2)

        self.grid.addWidget(self.localCode,1,0)
        self.grid.addWidget(self.cityCode,1,1)
        self.grid.addWidget(self.timeCode,1,2)

        self.group = QGroupBox('날씨')
        self.group.setLayout(self.grid)

        self.Btnbox = QHBoxLayout()
        self.Btnbox.addWidget(self.btn_ok)

        box = QVBoxLayout()
        box.addWidget(self.group)
        box.addWidget(self.output)
        box.addLayout(self.Btnbox)
        
        
        self.setWindowTitle('날씨조회')
        self.setLayout(box)
        self.setGeometry(100,100,450,300)
        self.show()


    def initEvent(self):


        self.localCode.currentIndexChanged.connect(self.set_cityCode)
        self.cityCode.currentIndexChanged.connect(self.set_timeCode)
        self.btn_ok.clicked.connect(self.show_weather)

    def set_cityCode(self, index):
        count = self.cityCode.count()
        for i in reversed(range(count)) :
            self.cityCode.removeItem(i)


        code = local_code[index]

        url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=" + str(code)
        response = urllib.request.urlopen(url)
        self.html = response.read()

        self.soup = BeautifulSoup(self.html, 'html.parser')

        locations = self.soup.find_all('location')
        city_list = []
        for i in locations :
            city_list.append(i.find('city'))
        for cityname in city_list :
            self.cityCode.addItem(cityname.text)

    def set_timeCode(self, index):
        city = self.soup.find_all('location')[index]
        self.data_list = city.find_all('data')

        for data in self.data_list :
            text = data.find('tmef').text
            self.timeCode.addItem(text)

    def show_weather(self):
        self.output.clear()
        index = self.timeCode.currentIndex()
        data = self.data_list[index]

        wf = data.find('wf').text
        tmn = data.find('tmn').text
        tmx = data.find('tmx').text

        self.output.setText('날씨 : ' + wf + '\n')
        self.output.append('최저 기온 : ' + tmn + '\n')
        self.output.append('최고 기온 : ' + tmx + '\n')
        self.output.append('이소스는 ')
        self.output.append('Copyright 2019. VersionKoreaProject All Rights Reserved.')





app = QApplication(sys.argv)
window = WeatherWindow()
app.exec_()