# -*- coding:utf-8 -*-

__author__ = 'yangyuenan'
__time__ = '2024/1/4 14:26'

import sys
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidgetItem, QApplication
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from tools import spider, flush_conf, init
from tableWidget import TableWidget

executor = ThreadPoolExecutor(3)


class gui(QMainWindow):
    init_signal = pyqtSignal(list)
    flush_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.exit = False
        self.setWindowTitle(u'基金估值')
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        self.mainLayout = QVBoxLayout()
        self.widgetInit()
        executor.submit(self.init_data)

    def widgetInit(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        wordLayout = QHBoxLayout()
        wordLabel = QLabel(u'输入基金代码：')
        self.wordInput = QLineEdit()
        self.jjInfo = TableWidget()
        self.jjInfo.setColumnCount(4)
        self.jjInfo.setHorizontalHeaderLabels(['基金代码', '基金名称', '现价', '涨跌幅（%）'])
        self.jjInfo.delete_signal.connect(self.delete_slot)
        addButton = QPushButton(u'添加')
        wordLayout.addWidget(wordLabel)
        wordLayout.addWidget(self.wordInput)
        self.mainLayout.addLayout(wordLayout)
        self.mainLayout.addWidget(addButton)
        self.mainLayout.addWidget(self.jjInfo)
        widget.setLayout(self.mainLayout)
        addButton.clicked.connect(self.add)

    def init_data(self):
        jj_infos = init()
        if jj_infos is not None:
            self.init_signal.emit(jj_infos)

    @pyqtSlot(list)
    def deal_data(self, jj_infos):
        for jj_info in jj_infos:
            self.jjInfo.setRowCount(self.jjInfo.rowCount() + 1)
            self.view_item(jj_info)
        executor.submit(self.flush_info)

    @pyqtSlot(list)
    def flush_data(self, jj_infos):
        self.jjInfo.setRowCount(0)
        if jj_infos:
            for jj_info in jj_infos:
                self.jjInfo.setRowCount(self.jjInfo.rowCount() + 1)
                self.view_item(jj_info)

    @pyqtSlot()
    def delete_slot(self):
        for index in self.jjInfo.delete:
            self.jjInfo.removeRow(index)
        self.jjInfo.delete.clear()

    def add(self):
        code = self.wordInput.text()
        jj_info = spider(code)
        self.jjInfo.setRowCount(self.jjInfo.rowCount() + 1)
        self.view_item(jj_info)
        flush_conf(code)
        self.wordInput.setText('')

    def view_item(self, jj_info: dict):
        table_count = self.jjInfo.rowCount() - 1
        code = QTableWidgetItem(jj_info['jj_code'])
        code.setFlags(Qt.ItemIsEnabled)
        name = QTableWidgetItem(jj_info['jj_name'])
        name.setFlags(Qt.ItemIsEnabled)
        self.jjInfo.setItem(table_count, 0, code)
        self.jjInfo.setItem(table_count, 1, name)
        if '-' in jj_info['jj_chg']:
            price = QTableWidgetItem(jj_info['jj_price'])
            price.setForeground(QBrush(QColor("green")))
            price.setFlags(Qt.ItemIsEnabled)
            chg = QTableWidgetItem(jj_info['jj_chg'])
            chg.setForeground(QBrush(QColor("green")))
            chg.setFlags(Qt.ItemIsEnabled)
            self.jjInfo.setItem(table_count, 2, price)
            self.jjInfo.setItem(table_count, 3, chg)
        else:
            price = QTableWidgetItem(jj_info['jj_price'])
            price.setForeground(QBrush(QColor("red")))
            price.setFlags(Qt.ItemIsEnabled)
            chg = QTableWidgetItem(jj_info['jj_chg'])
            chg.setForeground(QBrush(QColor("red")))
            chg.setFlags(Qt.ItemIsEnabled)
            self.jjInfo.setItem(table_count, 2, price)
            self.jjInfo.setItem(table_count, 3, chg)

    def flush_info(self):
        count = 0
        while True:
            sleep(1)
            count += 1
            if self.exit:
                break
            if count == 60:
                jj_infos = init()
                self.flush_signal.emit(jj_infos)
                count = 0

    def closeEvent(self, event):
        self.destroy()  # 窗口关闭销毁
        self.exit = True
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = gui()
    m.init_signal.connect(m.deal_data)
    m.flush_signal.connect(m.flush_data)
    m.show()
    app.exec_()
