# -*- coding:utf-8 -*-

__author__ = 'yangyuenan'
__time__ = '2024/1/9 17:31'

from PyQt5.QtWidgets import QMenu, QTableWidget
from PyQt5.QtCore import Qt, pyqtSignal
from tools import delete_code


class TableWidget(QTableWidget):
    delete_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.delete = []
        # 设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu()

        # 获取当前单元格
        item = self.itemAt(pos)
        if item is None:
            return

        # 添加操作
        delete_action = menu.addAction('删除')

        # 执行操作
        action = menu.exec_(self.viewport().mapToGlobal(pos))
        if action == delete_action:
            print(f'Delete {item.row()}')
            row_num = item.row()
            self.delete.append(row_num)
            self.delete_signal.emit()
            delete_code(row_num)
