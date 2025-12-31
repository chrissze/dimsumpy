

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)







def closeEvent(self, event: QCloseEvent) -> None:
    """
    commonly used to override defalut self.close() function. Input the function inside QWidget classes:

        def closeEvent(self, event: QCloseEvent) -> None:
            return closeEvent(self, event)

    """
    reply: QMessageBox.StandardButton = QMessageBox.question(
        self, 'Confirmation', 'Do you want to QUIT now?', QMessageBox.Yes | QMessageBox.Cancel)
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()
