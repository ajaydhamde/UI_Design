import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

# Connect to the SQLite database
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Execute a query to retrieve data
cursor.execute('SELECT * FROM my_table')
data = cursor.fetchall()

# Close the database connection when done
connection.close()
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super(MyTableModel, self).__init__(parent)
        self._data = data[:100]  # Load initial subset of data

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    def load_data_from_database(count):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM my_table LIMIT {count}')
        additional_data = cursor.fetchall()
        connection.close()
        return additional_data

    def load_more_data(self, count):
        # Load additional data dynamically
        additional_data = load_data_from_database(count)
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data) + count - 1)
        self._data.extend(additional_data)
        self.endInsertRows()

# Usage
model = MyTableModel(data)
table_view = QtWidgets.QTableView()
table_view.setModel(model)
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, items_per_page=100, parent=None):
        super(MyTableModel, self).__init__(parent)
        self._data = data
        self._items_per_page = items_per_page
        self._current_page = 0

    def rowCount(self, parent=QtCore.QModelIndex()):
        return min(len(self._data) - (self._current_page * self._items_per_page), self._items_per_page)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            row_index = index.row() + (self._current_page * self._items_per_page)
            return self._data[row_index][index.column()]

    def next_page(self):
        if (self._current_page + 1) * self._items_per_page < len(self._data):
            self.beginResetModel()
            self._current_page += 1
            self.endResetModel()

    def previous_page(self):
        if self._current_page > 0:
            self.beginResetModel()
            self._current_page -= 1
            self.endResetModel()

# Usage
model = MyTableModel(data)
table_view = QtWidgets.QTableView()
table_view.setModel(model)
next_button = QtWidgets.QPushButton("Next")
previous_button = QtWidgets.QPushButton("Previous")
next_button.clicked.connect(model.next_page)
previous_button.clicked.connect(model.previous_page)
