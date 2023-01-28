import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QDialog, QApplication
from PyQt5 import QtWidgets
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui
from main1 import Ui_MainWindow
from addEditCoffeeForm import Ui_k


class Add_Coffee(QDialog, Ui_k):
    def __init__(self, obj):
        self.obj = obj
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(611, 373)
        self.con = sqlite3.connect("data/coffee.db")
        self.add.clicked.connect(self.new_func)
        self.cur = self.con.cursor()
        self.comboBox.addItems([el[1] for el in self.cur.execute('select * from roast').fetchall()])
        self.comboBox_2.addItems(["в зёрнах", "молотый"])

    def new_func(self):
        try:
            title = self.lineEdit_3.text()
            roast = self.comboBox.currentText()
            structure = self.comboBox_2.currentText()
            price = int(self.spinBox.text())
            vol = int(self.spinBox_2.text())
            if not title:
                raise Exception
            id = list(self.cur.execute(f"SELECT id FROM coffe_info").fetchall())[-1][0] + 1
            roast_id = int(list(self.cur.execute(f"SELECT id from roast where '{roast}' = roasted").fetchall())[0][0])
            msg = QMessageBox.information(self, 'Успешно!', f'Добавлен элемент', QMessageBox.Ok)
            if structure == "молотый":
                structure = 1
            else:
                structure = 0
            self.cur.execute(f"""INSERT INTO coffe_info("id", "title", "roasted", "structure", "price", "volume") 
            VALUES({id}, '{title}', {roast_id}, {structure}, {price}, {vol})""")
            self.close()
            self.con.commit()
            self.cur.close()
            self.obj.table_run()
        except Exception as e:
            print("Ошибка")
            self.close()


class Update_coffee(QDialog, Ui_k):
    def __init__(self, obj, id):
        self.obj = obj
        self.title = id
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(611, 373)
        self.con = sqlite3.connect("data/coffee.db")
        self.add.clicked.connect(self.new_func)
        self.cur = self.con.cursor()
        self.comboBox.addItems([el[1] for el in self.cur.execute('select * from roast').fetchall()])
        self.comboBox_2.addItems(["в зёрнах", "молотый"])

    def new_func(self):
        try:
            title = self.lineEdit_3.text()
            roast = self.comboBox.currentText()
            structure = self.comboBox_2.currentText()
            price = int(self.spinBox.text())
            vol = int(self.spinBox_2.text())
            if not title:
                raise Exception
            roast_id = int(list(self.cur.execute(f"SELECT id from roast where '{roast}' = roasted").fetchall())[0][0])
            msg = QMessageBox.information(self, 'Успешно!', f'Обновлен элемент', QMessageBox.Ok)
            if structure == "молотый":
                structure = 1
            else:
                structure = 0
            self.cur.execute(f"""UPDATE coffe_info SET title = '{title}', roasted = {roast_id}, structure = {structure},
             price = {price}, volume = {vol} WHERE title = '{self.title}'""")
            self.close()
            self.con.commit()
            self.cur.close()
            self.obj.table_run()
        except Exception as e:
            print("Ошибка")
            print(e)
            self.close()


class Main_Table_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("data/coffee.db")
        self.cur = con.cursor()
        self.setupUi(self)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.edit_co)
        self.add.clicked.connect(self.add_co)
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

    def add_co(self):
        self.add_window = Add_Coffee(self)
        self.add_window.show()

    def edit_co(self, row, col):
        self.update_co = Update_coffee(self, self.table.item(row, 0).text())
        self.update_co.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main_Table_Window()
    w.show()
    sys.exit(app.exec_())
