from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
import pandas as pd


class DataFrameModel(QAbstractTableModel):
    """rowCount(), columnCount() and data() must be implemented """
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__()
        self.df = df

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self.df.columns.tolist()[section]
            except (IndexError,):
                return None
        elif orientation == Qt.Vertical:
            try:
                return self.df.index.tolist()[section]
            except (IndexError,):
                return None

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if not index.isValid():
            return None

        return str(self.df.iloc[index.row(), index.column()])

    def setData(self, index, value, role=Qt.DisplayRole):
        row = self.df.index[index.row()]
        col = self.df.columns[index.column()]
        dtype = self.df[col].dtype
        if dtype != object:
            value = None if value == '' else dtype.type(value)
        self.df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self.df.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self.df.columns)

    def sort(self, column, order):
        colname = self.df.columns.tolist()[column] # further check
        self.layoutAboutToBeChanged.emit()
        self.df.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
