from PySide2.QtWidgets import QMessageBox


def confirmation_box(func):
    def wrapper(*args):
        reply: QMessageBox.StandardButton = QMessageBox.question(
            args[0], 'Confirmation', 'Action?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            func(*args)
    return wrapper
