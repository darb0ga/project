import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from datetime import *
PROD = ['простоквашино']


class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)  # Загружаем дизайн
        print(1)
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
        self.amount = self.line2.text()
        self.dat = str(self.calendarWidget.selectedDate().day()) + \
                   str(self.calendarWidget.selectedDate().month()) +\
                   str(self.calendarWidget.selectedDate().year())
        self.date_object = datetime.strptime(str(self.dat), '%d%m%Y')
        print(self.date_object - datetime.today())

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
        pass

    def check(self):
        self.checkprod = Check()
        self.checkprod.show()

class Check(QWidget):
    def __init__(self):
        super().__init__()
        self.now = date.today()
        uic.loadUi('checking.ui', self)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

#connect = sqlite3.connect('database.db')
#cursor = connect.cursor()
#sqlite3.connect('database.db').commit()
