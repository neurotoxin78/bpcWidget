import psutil
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QFrame, QWidget, QGridLayout, QLabel, QProgressBar, QGraphicsDropShadowEffect)
from tools import loadStylesheet, get_config, get_cputemp, setShadow


class SystemLoad(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stylesheet = "stylesheets/systemload.qss"
        self.setStyleSheet(loadStylesheet(stylesheet))
        self.config = get_config()
        self.sensortimer = QTimer()
        self.sensortimer.timeout.connect(self.sysStat)
        self.sensortimer.start(self.config['intervals']['sensor_refresh_ms'])
        self.temptimer = QTimer()
        self.temptimer.timeout.connect(self.tempStat)
        self.temptimer.start(self.config['intervals']['cpu_temp_refresh_ms'])
        font = QFont()
        font.setFamily("DejaVu Sans Mono for Powerline")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(100)
        self.sensor_frame = QFrame()
        self.sensor_frame.setMinimumSize(QSize(0, 135))
        self.sensor_frame.setMaximumSize(QSize(16777215, 135))
        self.sensor_frame.setStyleSheet("background-color: rgba(85, 85, 127, 160);")
        # self.sensor_frame.setFrameShape(QFrame.NoFrame)
        # self.sensor_frame.setFrameShadow(QFrame.Raised)
        self.sensor_frame.setObjectName("sensor_frame")
        self.sensor_frameLayout = QGridLayout(self.sensor_frame)
        self.sensor_frameLayout.setObjectName("sensor_frameLayout")
        self.cpulabel = QLabel()
        self.cpulabel.setFont(font)
        self.cpulabel.setMinimumSize(QSize(39, 39))
        self.cpulabel.setObjectName("cpulabel")
        self.cpulabel.setText("CPU")
        self.sensor_frameLayout.addWidget(self.cpulabel, 0, 0, 1, 1)
        self.cpuBar = QProgressBar()
        self.cpuBar.setMinimumSize(QSize(0, 0))
        self.cpuBar.setMaximumSize(QSize(16777215, 26))
        self.cpuBar.setProperty("value", 0)
        self.cpuBar.setAlignment(Qt.AlignCenter)
        self.cpuBar.setObjectName("cpuBar")
        self.sensor_frameLayout.addWidget(self.cpuBar, 0, 1, 1, 1)
        self.ramLabel = QLabel()
        self.ramLabel.setMinimumSize(QSize(39, 31))
        self.ramLabel.setObjectName("ramLabel")
        self.ramLabel.setFont(font)
        self.sensor_frameLayout.addWidget(self.ramLabel, 1, 0, 1, 1)
        self.ramBar = QProgressBar()
        self.ramBar.setMaximumSize(QSize(16777215, 26))
        self.ramBar.setProperty("value", 0)
        self.ramBar.setAlignment(Qt.AlignCenter)
        self.ramBar.setObjectName("ramBar")
        self.sensor_frameLayout.addWidget(self.ramBar, 1, 1, 1, 1)
        self.cpu_tempLabel = QLabel()
        self.cpu_tempLabel.setMinimumSize(QSize(51, 31))
        self.cpu_tempLabel.setObjectName("cpu_tempLabel")
        self.cpu_tempLabel.setFont(font)
        self.sensor_frameLayout.addWidget(self.cpu_tempLabel, 2, 0, 1, 1)
        self.tempBar = QProgressBar()
        self.tempBar.setMaximumSize(QSize(16777215, 26))
        self.tempBar.setMinimum(20)
        self.tempBar.setMaximum(80)
        self.tempBar.setProperty("value", 19)
        self.tempBar.setAlignment(Qt.AlignCenter)
        self.tempBar.setObjectName("tempBar")
        self.sensor_frameLayout.addWidget(self.tempBar, 2, 1, 1, 1)
        self.setLayout(self.sensor_frameLayout)
        self.retranslateUi(SystemLoad)
        setShadow(self.cpuBar, 15)
        setShadow(self.ramBar, 15)
        setShadow(self.tempBar, 15)
        setShadow(self.cpulabel, 15)
        setShadow(self.ramLabel, 15)
        setShadow(self.cpu_tempLabel, 15)

    def retranslateUi(self, SystemLoad):
        _translate = QCoreApplication.translate
        self.cpulabel.setText(_translate("SystemLoad", "CPU:"))
        self.ramLabel.setText(_translate("SystemLoad", "RAM:"))
        self.cpu_tempLabel.setText(_translate("SystemLoad", "t°C:"))
        self.tempBar.setFormat(_translate("SystemLoad", "%p%°C"))

    def shadowize(self):
        self.blurRadius = 15
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(self.blurRadius)
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(self.blurRadius)
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(self.blurRadius)
        self.cpuBar.setGraphicsEffect(shadow1)
        self.ramBar.setGraphicsEffect(shadow2)
        self.tempBar.setGraphicsEffect(shadow3)

    def sysStat(self):
        self.ramBar.setValue(int(psutil.virtual_memory().percent))
        self.cpuBar.setMaximum(100)
        self.cpuBar.setValue(int(psutil.cpu_percent()))

    def tempStat(self):
        temp = get_cputemp(self.config['cpu_temp']['cpu_temp_sensor_path'])
        self.tempBar.setMaximum(100 * 100)
        self.tempBar.setValue(int(temp) * 100)
        self.tempBar.setFormat("%.01f °C" % temp)
