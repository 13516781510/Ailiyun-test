import base64
import json
import time

import paho.mqtt.client as mqtt


def cv2_to_base64(img):
    img = cv2.imencode('.png', img)[1]
    image_code = str(base64.b64encode(img))[2:-1]
    return image_code


# 连接成功回调
class Mqtt_Publisher:
    def __init__(self, broker_ip='iot-06z00jl8tcjx5tf.mqtt.iothub.aliyuncs.com',
                 clientId="k0eudLzkYR8.stm32_mqtt_esp8266|securemode=2,signmethod=hmacsha256,timestamp=1699097409592|",
                 port=1883,
                 username="stm32_mqtt_esp8266&k0eudLzkYR8",
                 intopic="/sys/k0eudLzkYR8/stm32_mqtt_esp8266/thing/service/property/set",
                 outtopic="/sys/k0eudLzkYR8/stm32_mqtt_esp8266/thing/event/property/post",
                 password="a2435ec609f8229bbed71235d9be4c6c83f8e6f81fd72717a38b74a5c565a963", timeout=60):

        # def __init__(self, broker_ip='iot-06z00jl8tcjx5tf.mqtt.iothub.aliyuncs.com',
        #              clientId="k0eudLzkYR8.app1|securemode=2,signmethod=hmacsha256,timestamp=1699097397678|", port=1883,
        #              username="app1&k0eudLzkYR8", intopic="/sys/k0eudLzkYR8/app1/thing/service/property/set",
        #              outtopic="/sys/k0eudLzkYR8/app1/thing/event/property/post",
        #              password="0ea5530e7102db70088e68774060f592de3083b9e242d2de6d596840a77d6528", timeout=60):
        '''
        :param central_ip: Broker的地址
        :param port:  端口号
        :project_id:产品id
        ：device_id
        : device_name
        :param timeout:  连接延时
        :param node_name: 设备名称
        :param anonymous: 是否同时允许多个节点
        '''
        self.clientId = clientId
        self.username = username
        self.broker_ip = broker_ip
        self.broker_port = port
        self.timeout = timeout
        self.connected = False
        self.intopic = intopic
        self.outtopic = outtopic
        self.password = password
        self.Start()
        self.data = {}

    def Start(self):
        self.client = mqtt.Client(self.clientId, protocol=mqtt.MQTTv311)  # 创建客户端
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect  # 指定回调函数
        self.client.connect(self.broker_ip, self.broker_port, self.timeout)

        self.client.subscribe(self.intopic)
        self.client.on_message = self.on_message_callback
        self.client.loop_start()

    def Publish(self, payload, qos=0, retain=False):
        if self.connected:
            return self.client.publish(self.outtopic, payload=payload, qos=qos, retain=retain)
        else:
            raise Exception("mqtt server not connected! you may use .Start() function to connect to server firstly.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            raise Exception("Failed to connect mqtt server.")

    def on_message_callback(self, client, userdata, message):
        data1 = json.loads(message.payload.decode())
        if "items" in data1:
            self.data = data1["items"]

    def stop(self):
        self.client.loop_stop()


if __name__ == '__main__':
    import cv2

    p = Mqtt_Publisher()
    while not p.connected:
        pass
    print(p.client.is_connected())
    i = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, 160)
    cap.set(4, 120)
    while True:
        i = i + 1
        _, img = cap.read()

        if _:
            vdata = cv2_to_base64(img)
            data = {
                "params": {
                    "vedio1": vdata,
                    "location": [1, 2, 3],
                    "collected": 42
                },
                "veision": "1.0.0"
            }
            p.Publish(json.dumps(data))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 打印按指定格式排版的时间
            cv2.imshow("vedio1", img)
            cv2.waitKey(300)
    cv2.destroyAllWindows()
