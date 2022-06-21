from threading import Thread, Lock
from timelapse import Timelapse
from log import Log

class TimelapseThread(Thread):

    def __init__(self, timelapse: Timelapse):
        Thread.__init__(self)
        self._timelapse = timelapse
        self._lock = Lock()

    def run(self) -> None:
        self._lock.acquire()
        self._timelapse.save()
        self._lock.release()
