from PySide2.QtWidgets import QMessageBox
from functools import wraps

def confirmation_self(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Action?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            method_output = method(self, *method_args, **method_kwargs)
            return method_output
    return _impl
    
