import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QDialog, QApplication
from PyQt5 import QtWidgets
import sqlite3
from PyQt5 import uic


class Main_Table_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("coffee.db")
        self.cur = con.cursor()
        uic.loadUi('main.ui', self)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.table.cellDoubleClicked.connect(self.edit_olympiad)
        # self.add.clicked.connect(self.add)
        self.table_run()

    def table_run(self):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Cтепень обжарки", "Структура", "Цена", "Объем"])
        self.table.setRowCount(0)
        result = self.cur.execute("select coffe_info.title, roast.roasted, coffe_info.structure, coffe_info.price, "
                                  "volume FROM coffe_info LEFT JOIN roast on roast.id = coffe_info.roasted").fetchall()
        res = []
        for el in result:
            if el[2] == 0:
                res.append([el[0], el[1], "в зёрнах", el[3], el[4]])
            else:
                res.append([el[0], el[1], "молотый", el[3], el[4]])
        for i, row in enumerate(res):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, el in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(el)))
        self.table.resizeColumnsToContents()
        column_head = self.table.horizontalHeader()
        column_head.setSectionResizeMode(0, QHeaderView.Stretch)

    # def add_ol(self):
    #     self.add_window = Add_olympiad(ww.USER_ID)
    #     self.add_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main_Table_Window()
    w.show()
    sys.exit(app.exec_())
