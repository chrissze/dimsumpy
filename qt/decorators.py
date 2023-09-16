from PySide6.QtWidgets import QMessageBox
from functools import wraps

def self_confirmation(method):
    """
    IMPORTS: QMessageBox, wraps
    """
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Action?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            method_output = method(self, *method_args, **method_kwargs)
            return method_output
    return _impl



def list_confirmation(method):
    """
    IMPORTS: QMessageBox, wraps
    This decorator requires that the function or method have (self, list) arguments.
    I need to put @list_confirmation on top of function definition. 
    """
    @wraps(method)
    def _impl(self, xs):
        number: int = len(xs)
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', f'Do you want to work on {number} items?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            method_output = method(self, xs)
            return method_output
    return _impl

