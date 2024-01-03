import threading


class ThreadManagement:
    injectionLock = threading.RLock()
    replayLock = threading.RLock()
    stopInject = False
    stopReplay = False
