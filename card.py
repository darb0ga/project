import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from datetime import *
PROD = ['простоквашино']


class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)  # Загружаем дизайн
        self.comboBox.addItems(PROD)
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
        self.dat = str(self.calendarWidget.selectedDate().day()) + \
                   str(self.calendarWidget.selectedDate().month()) +\
                   str(self.calendarWidget.selectedDate().year())
        self.date_object = datetime.strptime(str(self.dat), '%d%m%Y')
        print(self.amount)


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
        name, ok_pressed = QInputDialog.getText(self, "Введите изготовителя",
                                                "Изготовитель:")
        if ok_pressed:
            global PROD
            PROD.append(name)

    def new_product(self):
        self.name = self.line1.text()
        self.produce = self.comboBox.currentText()

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
            WHERE data = ?""", (str('.'.join(str(date.today()).split('-')[::-1])),)).fetchall()
        print(self.result,  '.'.join(str(date.today()).split('-')[::-1]))
        if self.result:
            self.tableWidget.setColumnCount(len(self.result[0]))
            self.tableWidget.setRowCount(len(self.result))
            self.tableWidget.setHorizontalHeaderLabels(('1', '2', '3', '4', '5'))
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
        print(self.result)
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(('1', '2', '3', '4', '5'))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.result) + 1)])
        for i, row in enumerate(self.result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
