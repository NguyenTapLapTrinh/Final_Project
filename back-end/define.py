import enum

class CMD(enum.Enum):
    ADD = 1
    DEL = 2
    EDITPHOTO = 3
    EDITNAME = 4

class Socket(enum.Enum):
    BUFFER = 8192
    PORT = 5000
    WAITLIST = 1
    TIMEOUT  = 1
    IPADRESS = "localhost"
    # IPADRESS = "192.168.1.6"

class Time(enum.Enum):
    TIME_SLEEP_500MS = 0.5
    TIME_SLEEP_10MS = 0.01
    TIME_SLEEP_2S = 2
    TIME_SLEEP_5S = 5000