


# THIRD PARTY LIBS
from PySide6.QtCore import QThread


class MyThread(QThread):
    """
    QThread is the base class.
    """
    def __init__(self, func, callback, args=()) -> None:
        super().__init__()
        self.func = func            # so that self.run() can access func
        self.callback = callback    # so self.callitback() can access callback
        self.args = args            # so that self.run() can access args
        self.finished.connect(self.callitback)      # I could not just use self.callback


    def __del__(self):
        self.wait()

    def run(self) -> None:
        self.func(*self.args)

    def callitback(self) -> None:      # for self.finished.connect()
        self.callback()        # I should not include self as argument, otherwise, real arguments like tid will not be matched.
