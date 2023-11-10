import base64
import json
import sys
import time

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

from iot import Ui_IOT
from mqtt_publisher import Mqtt_Publisher


class IOT(QWidget, Ui_IOT):
    def __init__(self):
        super(IOT, self).__init__()
        self.filename = None
        self.pix = QPixmap()

        self.systemtimer = QTimer(self)
        self.systemtimer.timeout.connect(self.updateframe)

        self.videotimer = QTimer(self)
        self.videotimer.timeout.connect(self.vedio_operate)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.close_button.clicked.connect(self.closeEvent)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.connected_button.clicked.connect(self.create_mqtt_pubblisher)
        self.open_video1.clicked.connect(self.onOpenVideoButtonClicked)
        self.close_video1.clicked.connect(self.closeOpenVideoButtonClicked)
        self.open_or_close_pipeline.clicked.connect(self.changepipelinestate)
        self.open_or_close_robot.clicked.connect(self.changerobotstate)
        self.choose_xipan.clicked.connect(self.endbexipan)
        self.choose_jiazhua.clicked.connect(self.endbejiazhua)
        self.set_pipeline_v.valueChanged.connect(self.set_V)
        self.tableWidget1.horizontalHeader().setVisible(True)
        self.tableWidget1.horizontalHeader().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)
        self.tableWidget1.verticalHeader().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)

    def create_mqtt_pubblisher(self):
        self.publisher = Mqtt_Publisher(
            broker_ip='iot-06z00jl8tcjx5tf.mqtt.iothub.aliyuncs.com',
            clientId="k0eudLzkYR8.app1|securemode=2,signmethod=hmacsha256,timestamp=1699097397678|", port=1883,
            username="app1&k0eudLzkYR8", intopic="/sys/k0eudLzkYR8/app1/thing/service/property/set",
            outtopic="/sys/k0eudLzkYR8/app1/thing/event/property/post",
            password="0ea5530e7102db70088e68774060f592de3083b9e242d2de6d596840a77d6528", timeout=60
        )
        while not self.publisher.connected:
            pass
        i = 0
        self.state_pipeline1.setText(self._translate("IOT", "生产线1已成功接入阿里云平台，可选择转至其他页面"))
        self.systemtimer.start(20)

    '''涉及发送指令的'''

    def set_V(self):
        data = {
            "params": {
                "V_pipeline": self.set_pipeline_v.value()
            },
            "veision": "1.0.0"
        }
        self.publisher.Publish(json.dumps(data))


    def endbexipan(self):
        self.state_end_excutive.setText(self._translate("IOT", "目前：吸盘"))
        data = {
            "params": {
                "end_excutor": 0
            },
            "veision": "1.0.0"
        }
        self.publisher.Publish(json.dumps(data))

    def endbejiazhua(self):
        self.state_end_excutive.setText(self._translate("IOT", "目前：夹爪"))
        data = {
            "params": {
                "end_excutor": 1
            },
            "veision": "1.0.0"
        }
        self.publisher.Publish(json.dumps(data))


    def changerobotstate(self):
        if (self.open_or_close_robot.text() == "关闭"):
            self.open_or_close_robot.setText(self._translate("IOT", "开启"))
            self.state_robot.setText(self._translate("IOT", "已关闭"))
            data = {
                "params": {
                    "ctrl_robotic": 0
                },
                "veision": "1.0.0"
            }
            self.publisher.Publish(json.dumps(data))

        else:
            self.open_or_close_robot.setText(self._translate("IOT", "关闭"))
            self.state_robot.setText(self._translate("IOT", "已开启"))
            data = {
                "params": {
                    "ctrl_robotic": 1
                },
                "veision": "1.0.0"
            }
            self.publisher.Publish(json.dumps(data))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 打印按指定格式排版的时间
    def changepipelinestate(self):
        if (self.open_or_close_pipeline.text() == "关闭"):
            self.open_or_close_pipeline.setText(self._translate("IOT", "开启"))
            self.set_pipeline_v.setValue(0.00)
            self.set_pipeline_v.setDisabled(True)
            data = {
                "params": {
                    "control_pipiline": 0
                },
                "veision": "1.0.0"
            }
            self.publisher.Publish(json.dumps(data))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 打印按指定格式排版的时间

        else:
            self.open_or_close_pipeline.setText(self._translate("IOT", "关闭"))
            self.set_pipeline_v.setEnabled(True)
            data = {
                "params": {
                    "control_pipiline": 1
                },
                "veision": "1.0.0"
            }
            self.publisher.Publish(json.dumps(data))

    def updateframe(self):
        if "end_location" in self.publisher.data:
            self.end_x.setText(self._translate("IOT", str(self.publisher.data["end_location"]["value"])))
        if "collected" in self.publisher.data:
            pass
        if "vedio1" in self.publisher.data:
            pass
        if "vedio1" in self.publisher.data:
            pass
        if "vedio1" in self.publisher.data:
            pass
        if "vedio1" in self.publisher.data:
            pass
        if "vedio1" in self.publisher.data:
            pass

    def onOpenVideoButtonClicked(self):
        self.videotimer.start(20)  # 设置计时间隔并启动，间隔20ms
        self.video1.setScaledContents(False)

    def closeOpenVideoButtonClicked(self):
        self.videotimer.stop()

    def vedio_operate(self):
        if "vedio1" in self.publisher.data:
            img = base64.b64decode(self.publisher.data["vedio1"]["value"])
            self.pix.loadFromData(img)
            self.video1.setPixmap(self.pix)
            QApplication.processEvents()

        else:
            self.video1.setPixmap(QPixmap("resource/error_no_image.png"))

    def closeEvent(self):
        sys.exit()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == PyQt5.QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = QMouseEvent.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            QMouseEvent.accept()
            self.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if PyQt5.QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(PyQt5.QtGui.QCursor(PyQt5.QtCore.Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = IOT()
    ui.show()
    sys.exit(app.exec_())
