import datetime
import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from datetime import *


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


class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.connect = sqlite3.connect('data.sqlite')
        self.cursor = self.connect.cursor()
        self.result = self.cursor.execute("""SELECT title FROM made""").fetchall()
        self.l = []
        for el in self.result:
            a = el[0]
            self.l.append(a)
        self.comboBox.addItems(self.l)
        self.pushb1.clicked.connect(self.importir)
        self.pushb2.clicked.connect(self.back)
        self.pushb3.clicked.connect(self.add)

    def back(self):
        self.hide()

    def importir(self):
        file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        try:
            connect = sqlite3.connect('data.sqlite')
            cursor = connect.cursor()
            with open(file, encoding='utf8') as csvf:
                reader = csv.DictReader(csvf, delimiter=';')
                for row in reader:
                    print(row['name'], row['amount'], row['prodused'], row['data'])
                    cursor.execute("""INSERT INTO students((name, amount, prodused, data)) VALUES(?, ?, ?, ?)""",
                                   (row['name'], row['amount'], row['prodused'], row['data']))
                    connect.commit()
            self.loadTable()
        except:
            message = QMessageBox()
            message.setIcon(3)
            message.setText('Ошибка файла')
            message.exec()

    def add(self):
        self.name = self.line1.text()
        self.pro = self.cursor.execute('''SELECT id FROM made WHERE title = (?)''',
                                       (str(self.comboBox.currentText()),)).fetchall()
        self.amount = self.spinBox.value()
        self.dat = str(self.calendarWidget.selectedDate().year()) + '-' +\
                   str(self.calendarWidget.selectedDate().month()) + '-' +\
                   str(self.calendarWidget.selectedDate().day())
        if self.name:
            self.lab.setText('')
            self.cursor.execute("""INSERT INTO product(name, amount, prodused, data) VALUES(?, ?, ?, ?)""",
                            (self.name, self.amount,  self.pro[0][0], self.dat))
            self.connect.commit()
            self.hide()
        else:
            self.lab.setText('Название не указано')


class Check(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('checking.ui', self)
        self.pushButton.clicked.connect(self.back)
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.x = self.cur.execute('''SELECT * FROM product''').fetchall()
        self.result = []
        for i, row in enumerate(self.x):
            for j, elem in enumerate(row):
                if j == 4:
                    y = elem.split('-')
                    a, b, c = y[0], y[1], y[2]
                    d = datetime(int(a), int(b), int(c))
                    if d < datetime.now():
                        self.result.append(self.cur.execute("""SELECT * FROM product 
                        WHERE id = ? """, (int(row[0]), )).fetchall())
        if self.result:
            self.result = self.result[0]
            self.tableWidget.setColumnCount(len(self.x[0]))
            self.tableWidget.setRowCount(len(self.result))
            self.tableWidget.setHorizontalHeaderLabels(('id', 'название',
                                                        'колличество', 'изготовитель', 'срок годности'))
            self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.x) + 1)])
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
        if self.result:
            for i, row in enumerate(self.result):
                self.cur.execute("""DELETE FROM product WHERE id=(?)""", (int(row[0]), ))
                self.con.commit()
        self.hide()


class Table(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.filter)
        self.pushback.clicked.connect(self.back)
        self.pushButton2.clicked.connect(self.delite)
        self.result = self.cur.execute("""SELECT title FROM made""").fetchall()
        self.l = []
        self.l.append('Без фильтра')
        for el in self.result:
            a = el[0]
            self.l.append(a)
        self.comboBox.addItems(self.l)
        self.loadtable()

    def back(self):
        self.hide()

    def filter(self):
        self.izg = self.comboBox.currentText()
        if self.izg == 'Без фильтра':
            self.loadtable()
        else:
            try:
                self.prod = self.cur.execute("""SELECT * FROM product
                WHERE prodused = (
                SELECT id FROM made 
                WHERE title = ?)""", (str(self.izg),)).fetchall()
                self.tableWidget.setColumnCount(len(self.prod[0]))
                self.tableWidget.setRowCount(len(self.prod))
                self.tableWidget.setHorizontalHeaderLabels(
                    ('id', 'название', 'колличество', 'изготовитель', 'срок годности'))
                self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.prod) + 1)])
                for i, row in enumerate(self.prod):
                    for j, elem in enumerate(row):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                self.tableWidget.resizeColumnsToContents()
            except Exception as e:
                self.prod = []
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setRowCount(len(self.prod))
                self.tableWidget.setHorizontalHeaderLabels(
                    ('id', 'название', 'колличество', 'изготовитель', 'срок годности'))



    def delite(self):
        if self.tableWidget.currentIndex().row():
            message = QMessageBox.question(self, 'Удалить товар', "Вы уверены?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                result = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 0).data()
                self.cur.execute("""DELETE FROM product WHERE id=(?)""", (result,))
                self.con.commit()
                self.lab.setText('')
                self.loadtable()
        else:
            self.lab.setText('Продукт для удаления не выбран')

    def loadtable(self):
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
        self.pushdel.clicked.connect(self.delite)
        self.loadtable()

    def back(self):
        self.hide()

    def delite(self):
        if self.tableWidget.currentIndex().row():
            message = QMessageBox.question(self, 'Удалить товар', "Вы уверены?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                result = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 0).data()
                self.cur.execute("""DELETE FROM made WHERE id=(?)""", (result,))
                self.con.commit()
                self.lab.setText('')
                self.loadtable()
        else:
            self.lab.setText('Продукт для удаления не выбран')

    def loadtable(self):
        self.con = sqlite3.connect("data.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute('''SELECT * FROM made''').fetchall()
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(('id', 'название'))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.result) + 1)])
        for i, row in enumerate(self.result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def addd(self):
        if self.lineEdit.text():
            self.lab.setText('')
            self.cur.execute("""INSERT INTO made(title) VALUES(?)""", (self.lineEdit.text(),))
            self.con.commit()
            self.con.close()
            self.hide()
        else:
            self.lab.setText('Изготовитель не указан')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

#connect = sqlite3.connect('database.db')
#cursor = connect.cursor()
#sqlite3.connect('database.db').commit()
#self.date_object - datetime.today()
