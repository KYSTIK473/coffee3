import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
from form import Ui_MainWindow
from form1 import Ui_Form
import sqlite3


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        self.pushButton.clicked.connect(self.run)
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def run(self):
        self.second_form = SecondForm(self)
        self.second_form.show()
        SecondForm(self)


class SecondForm(QWidget, Ui_Form):
    def __init__(self, args):
        super().__init__()
        self.initUI()
        self.arg = args

    def initUI(self):
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        self.comboBox.addItems(["Молотый", "Зёрна"])
        self.pushButton.clicked.connect(self.run)

    def run(self):
        arr = ["Молотый", "Зёрна"]
        cur = self.con.cursor()
        try:
                cur.execute(
                    f"""INSERT INTO coffee(title, level, mol, label, cost, v) VALUES ('{self.lineEdit.text()}',
        {self.lineEdit_2.text()}, '{arr[self.comboBox.currentIndex()]}', '{self.lineEdit_3.text()}', {self.lineEdit_4.text()}, {self.lineEdit_5.text()})""")
                self.con.commit()
                self.arg.initUI()
        except Exception:
            self.label_5.setText('Неккоркетный ввод')
            return
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
