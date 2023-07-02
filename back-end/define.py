import enum
import platform

class CMD(enum.Enum):
    ADD = 1
    DEL = 2
    EDITPHOTO = 3
    EDITNAME = 4

class Socket(enum.Enum):
    BUFFER = 8192
    PORT = 5000
    UPDATE_PORT = 8000
    WAITLIST = 1
    TIMEOUT  = 1
    # IPADRESS = "localhost"
    IPADRESS = "192.168.43.80"

class Time(enum.Enum):
    TIME_SLEEP_500MS = 0.5
    TIME_SLEEP_10MS = 0.01
    TIME_SLEEP_2S = 2
    TIME_SLEEP_5S = 5000
    TIME_SLEEP_10S = 10

class Item(enum.Enum):
    HELMET = 0
    VEST = 1
    GLOVE = 2

class Platform(enum.Enum):
    SYSTEM = platform.system()

class Device(enum.Enum):
    USER_NAME = "jetson-nano"
    USER_PASSWD = "123456"
    USER_IP = "192.168.43.80"
