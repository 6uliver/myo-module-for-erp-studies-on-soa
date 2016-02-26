from MyoWebsocket import MyoWebsocket
import json

class Commands:
    VIBRATE = 'vibrate'
    SET_LOCKING_POLICY= 'set_locking_policy'

class Vibration:
    SHORT = 'short'
    MEDIUM = 'medium'
    LONG = 'long'

class Pose:
    REST = 'rest'
    WAVE_OUT = 'wave_out'
    WAVE_IN = 'wave_in'
    DOUBLE_TAP = 'double_tap'
    FINGERS_SPREAD = 'fingers_spread'
    FIST = 'fist'

class LockingPolicy:
    NONE = 'none'
    STANDARD = 'standard'

class Events:
    ORIENTATION = 'orientation'
    ACCELEROMETER = 'accelerometer'
    GYROSCOPE = 'gyroscope'
    EMG = 'emg'
    PAIRED = 'paired'
    CONNECTED = 'connected'
    LOCKED = 'locked'
    UNLOCKED = 'unlocked'
    POSE = 'pose'

class Myo():
    TYPE = 'type'
    EVENT = 'event'

    def __init__(self, appId='com.myopython.default'):
        self.websocket = MyoWebsocket(self, appId)
        self.websocket.start()
        self.myos = {}

    def close(self):
        self.websocket.close()

    def sendCommand(self, command):
        self.websocket.send(json.dumps(['command', command]))

    def onConnected(self, onConnectedCallback):
        self.onConnectedCallback = onConnectedCallback

    def onMessage(self, messageString):
        messageObject = json.loads(messageString)
        if messageObject[0] != Myo.EVENT:
            return
        message = messageObject[1]
        type = message[Myo.TYPE]
        if type == Events.PAIRED:
            pass
        elif type == Events.CONNECTED:
            self.myos[message['myo']] = MyoInstance(self, 0)
            self.onConnectedCallback(self.myos[message['myo']])
            pass
        else:
            self.myos[0].onMessage(message)
            pass

class MyoInstance():
    def __init__(self, myoConnector, index):
        self.callbacks = {}
        self.myoConnector = myoConnector
        self.index = index

    def _sendCommand(self, command):
        self.myoConnector.sendCommand(command)

    def setLockingPolicy(self, policy = LockingPolicy.STANDARD):
        self._sendCommand({
            "command": Commands.SET_LOCKING_POLICY,
            "myo": self.index,
            "type": policy
        })

    def vibrate(self, intensity = Vibration.MEDIUM):
        self._sendCommand({
            "command": Commands.VIBRATE,
            "myo": self.index,
            "type": intensity
        })

    def setStreamEMG(self, enabled):
        self._sendCommand({
            "command": "set_stream_emg",
            "myo": self.index,
            "type": 'enabled' if enabled else 'disabled'
        })

    def onOrientation(self, cb):
        self.callbacks[Events.ORIENTATION] = cb

    def onAccelerometer(self, cb):
        self.callbacks[Events.ACCELEROMETER] = cb

    def onGyroscope(self, cb):
        self.callbacks[Events.GYROSCOPE] = cb

    def onPose(self, cb):
        self.callbacks[Events.POSE] = cb

    def onEMG(self, cb):
        self.callbacks[Events.EMG] = cb

    def onMessage(self, message):
        type = message[Myo.TYPE]
        if type == Events.ORIENTATION:
            if Events.ORIENTATION in self.callbacks:
                self.callbacks[Events.ORIENTATION](message[Events.ORIENTATION])
            if Events.ACCELEROMETER in self.callbacks:
                self.callbacks[Events.ACCELEROMETER](message[Events.ACCELEROMETER])
            if Events.GYROSCOPE in self.callbacks:
                self.callbacks[Events.GYROSCOPE](message[Events.GYROSCOPE])
            pass
        elif type == Events.POSE:
            if Events.POSE in self.callbacks:
                self.callbacks[Events.POSE](message[Events.POSE])
            pass
        elif type == Events.EMG:
            if Events.EMG in self.callbacks:
                self.callbacks[Events.EMG](message[Events.EMG])
            pass
        else:
            pass