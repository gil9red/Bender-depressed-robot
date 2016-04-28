#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


#     def transform_input(city_map, correct):
#         city_map = [list(row.strip()) for row in city_map.strip().split('\n')]
#         correct = [i.strip() for i in correct.strip().split('\n')]
#
#         return city_map, correct
#
#     def bender_run(self, city_map, correct, max_count=None):
#         city_map, correct = self.transform_input(city_map, correct)
#
#         b = bender.Bender(city_map)
#
#         if max_count is None:
#             max_count = len(correct) + 5
#
#         # Ходим, пока не встретим символ '$'
#         while True:
#             max_count -= 1
#             if max_count <= 0:
#                 break
#
#             cell = b.step()
#             bender.log('cell: "{}"'.format(cell))
#             if cell == '$':
#                 break
#
#         bender.log(b.steps, correct, sep='\n')
#         self.assertEqual(b.steps, correct)
#
#     def test_Simple_moves(self):
#         city_map = """
# #####
# #@  #
# #   #
# #  $#
# #####
#         """
#
#         correct = """
# SOUTH
# SOUTH
# EAST
# EAST
#         """
#


import sys

from PySide.QtGui import *
from PySide.QtCore import *

import bender


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        import os.path
        self.setWindowTitle(os.path.basename(os.path.dirname(__file__)))

        dock_map = QDockWidget()
        dock_map.setWindowTitle('City Map')
        self.new_game_button = QPushButton('New Game')
        self.new_game_button.clicked.connect(self.new_game)

        self.next_step_button = QPushButton('Next Step')
        self.next_step_button.clicked.connect(self.next_step)

        self.city_map_editor = QPlainTextEdit()
        self.city_map_editor.setPlainText(
            """\
###############
#      IXXXXX #
#  @          #
#E S          #
#             #
#  I          #
#  B          #
#  B   S     W#
#  B   T      #
#             #
#         T   #
#         B   #
#N          W$#
#        XXXX #
###############
            """
        )
        dock_map_layout = QVBoxLayout()
        dock_map_buttons_layout = QHBoxLayout()
        dock_map_buttons_layout.addWidget(self.new_game_button)
        dock_map_buttons_layout.addWidget(self.next_step_button)
        dock_map_layout.addLayout(dock_map_buttons_layout)
        dock_map_layout.addWidget(self.city_map_editor)
        dock_map_contents = QWidget()
        dock_map_contents.setLayout(dock_map_layout)
        dock_map.setWidget(dock_map_contents)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_map)

        dock_steps = QDockWidget()
        dock_steps.setWindowTitle('Steps')
        self.steps_log = QPlainTextEdit()
        dock_steps_layout = QVBoxLayout()
        dock_steps_layout.addWidget(self.steps_log)
        dock_steps_contents = QWidget()
        dock_steps_contents.setLayout(dock_steps_layout)
        dock_steps.setWidget(dock_steps_contents)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_steps)

        self.bender = None
        self.steps_log_list = list()

        self.view = QTableWidget()
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().hide()
        self.setCentralWidget(self.view)

        self.update_states()

    def new_game(self):
        self.steps_log_list = list()

        city_map = [list(row.strip()) for row in self.city_map_editor.toPlainText().strip().split('\n')]
        self.bender = bender.Bender(city_map)

        self.update_view()
        self.update_states()

    def next_step(self):
        cell = self.bender.step()
        print('cell: "{}"'.format(cell))

        log = self.bender.direction_name, self.bender.pos, self.bender.invert, self.bender.breaker
        if log in self.steps_log_list:
            # QMessageBox.information(self, 'LOOP', 'LOOP')
            pass
        self.steps_log_list.append(log)

        text = '\n'.join(['\t'.join(list(map(str, log))) for log in self.steps_log_list])
        self.steps_log.setPlainText(text)

        self.update_view()

        if cell == '$':
            self.bender = None
            QMessageBox.information(self, 'Finish', 'Finish')

        self.update_states()

    def update_states(self):
        self.next_step_button.setEnabled(self.bender is not None)

    def update_view(self):
        self.view.clear()
        self.view.setRowCount(self.bender.rows)
        self.view.setColumnCount(self.bender.cols)

        city_map = self.bender.city_map()
        for i in range(self.bender.rows):
            for j in range(self.bender.cols):
                cell = city_map[i][j]

                self.view.setItem(i, j, QTableWidgetItem(cell))

        cell_size = 20
        for i in range(self.bender.rows):
            self.view.setRowHeight(i, cell_size)

        for j in range(self.bender.cols):
            self.view.setColumnWidth(j, cell_size)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(500, 300)
    mw.show()

    app.exec_()
