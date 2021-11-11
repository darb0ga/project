import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from datetime import *


class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.connect = sqlite3.connect('data.sqlite')
        self.cursor = self.connect.cursor()
        self.result = self.cursor.execute("""SELECT name, amount, student_id 
                FROM product, made 
                WHERE students.group_id = groups.group_id""").fetchall()
        print(self.result)
        self.comboBox.addItems(list(self.result))
        self.pushb1.clicked.connect(self.importir)
        self.pushb2.clicked.connect(self.back)
        self.pushb3.clicked.connect(self.add)

    def back(self):
        self.hide()

    def importir(self):
        pass

    def add(self):
        self.name = self.line1.text()
        self.pro = self.comboBox.currentText()
        self.amount = self.spinBox.value()
        self.dat = str(self.calendarWidget.selectedDate().year()) + '-' +\
                   str(self.calendarWidget.selectedDate().month()) + '-' +\
                   str(self.calendarWidget.selectedDate().day())

        self.cursor.execute("""INSERT INTO product(name, amount, prodused, data) VALUES(?, ?)""",
                       (self.name, self.amount,  self.pro, self.dat))
        self.hide()



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ghjtrn.ui', self)  # Загружаем дизайн
        self.pixmap = QPixmap('s.jpg')
        self.x = self.pixmap.size()
        self.label.resize(self.x)
        self.label.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.produce)
        self.pushButton_3.clicked.connect(self.table)
        self.pushButton_4.clicked.connect(self.check)

    def add(self):
        self.groups = AddProduct()
        self.groups.show()

    def produce(self):
        self.p = MadeBy()
        self.p.show()

    def table(self):
        self.table = Table()
        self.table.show()

    def check(self):
        self.checkprod = Check()
        self.checkprod.show()


class Check(QWidget):
    def __init__(self):
        super().__init__()
        self.now = date.today()
        uic.loadUi('checking.ui', self)
        self.pushButton.clicked.connect(self.back)
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT * FROM product
            WHERE data < ?""", (str(date.today()),)).fetchall()
        print(self.result,  date.today())
        if self.result:
            self.tableWidget.setColumnCount(len(self.result[0]))
            self.tableWidget.setRowCount(len(self.result))
            self.tableWidget.setHorizontalHeaderLabels(('id', 'название', 'колличество', 'изготовитель', 'срок годности'))
            self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.result) + 1)])
            for i, row in enumerate(self.result):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
            self.lab.setText('У этих товаров истек срок годности!' '\n'
                             'Они будут удалены из базы данных.')
            self.lab.setStyleSheet("color: rgb(0, 80, 220)")
        else:
            self.tableWidget.hide()
            self.lab.setText('Сегодня просроченных продуктов нет')
            self.lab.setStyleSheet("color: rgb(0, 27, 68)")

    def back(self):
        self.hide()


class Table(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.pushback.clicked.connect(self.back)
        self.loadtable()

    def back(self):
        self.hide()

    def loadtable(self):
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute('''SELECT * FROM product''').fetchall()
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(('id', 'название', 'колличество', 'изготовитель', 'срок годности'))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.result) + 1)])
        for i, row in enumerate(self.result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


class MadeBy(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('produse.ui', self)
        self.pushback.clicked.connect(self.back)
        self.pushadd.clicked.connect(self.addd)
        self.loadtable()

    def back(self):
        self.hide()

    def loadtable(self):
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute('''SELECT * FROM made''').fetchall()
        print(self.result)
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(('id', 'название'))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.result) + 1)])
        for i, row in enumerate(self.result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def addd(self):
        self.cur.execute("""INSERT INTO made(title) VALUES(?)""", (self.lineEdit.text(),))
        print(self.lineEdit.text())
        self.con.commit()
        self.con.close()
        self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

#connect = sqlite3.connect('database.db')
#cursor = connect.cursor()
#sqlite3.connect('database.db').commit()
#self.date_object - datetime.today()