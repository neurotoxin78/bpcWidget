
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (QWidget, QGridLayout, QTextBrowser)
from tools import get_config
from chat import ChatBot
import time

class BrowserHandler(QObject):
    running = False
    newTextAndColor = pyqtSignal(str, object)

    # method which will execute algorithm in another thread
    def run(self):
        config = get_config()
        refresh_interval = (int(config['intervals']['humor_fefresh_min']) * 1024) * 60
        chatbot = ChatBot()
        while True:
            # send signal with new text and color from aonther thread
            chatbot.setPrompt("Пожартуй весело та коротко на довільну тему. не більше 180 символів")
            response = chatbot.getResponce(max_tokens=1024, n=1, stop=None, temperature=0.5)
            humor_text = response[0].text
            self.newTextAndColor.emit(
                '{}.'.format(humor_text),
                QColor(255, 255, 255)
            )
            QThread.msleep(refresh_interval)




class GPTHumor(QWidget):
    def __init__(self, *args, **kwargs):
        super(GPTHumor, self).__init__(*args, **kwargs)
        # Load the UI Page
        self.config = get_config()
        uic.loadUi('ui/humor_box.ui', self)
        #self.humor_box_timer = QTimer()
        #self.humor_box_timer.timeout.connect(self.recurring_timer)
        #refresh_interval = (int(self.config['intervals']['humor_fefresh_min']) * 1024) * 60
        #self.humor_box_timer.start(refresh_interval)
        font = QFont()
        font.setFamily("DejaVu Sans Mono for Powerline")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(100)
        self.humor_box.setFont(font)
        self.humor_box.setAcceptRichText(True)
        self.humor_box.setOpenExternalLinks(True)
        self.chatbot = ChatBot()
        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.browserHandler = BrowserHandler()
        # move object to another thread
        self.browserHandler.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        self.browserHandler.newTextAndColor.connect(self.addNewTextAndColor)
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.browserHandler.run)
        # start thread
        self.thread.start()

    @pyqtSlot(str, object)
    def addNewTextAndColor(self, string, color):
        self.humor_box.setTextColor(color)
        self.humor_box.clear()
        self.humor_box.append(string)

    def addAnotherTextAndColor(self):
        self.humor_box.setTextColor(QColor(0, 255, 0))
        self.humor_box.append(
            '{} - thread 2 variant 3.\n'.format(str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))))


    def refresh(self):
        self.humor_box.clear()
        self.humor_box.append('<p style="font-size: 20px"><b>' + text + '</b></p>')
