


# THIRD PARTY LIBS
from PySide6.QtCore import QThread


class CustomThread(QThread):
    """
    QThread is the base class.
    """
    def __init__(self, func, callback, args=()) -> None:
        super().__init__()
        self.func = func            # so that self.run() can access func
        self.callback = callback    # so self.callitback() can access callback
        self.args = args            # so that self.run() can access args
        self.finished.connect(self.callitback)

    def __del__(self):
        self.wait()

    def run(self) -> None:
        self.func(*self.args)

    def callitback(self) -> None:      # for self.finished.connect()
        self.callback()
