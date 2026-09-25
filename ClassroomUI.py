from typing import Any

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QFrame, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

from utils import *
from styles import (
    back_button, classroom_content, classroom_scroll, classroom_window,
    desk as style_desk, desk_title, scroll_bar, smooth_scroll, student_slot,
)


class Classroom(QWidget):
    def __init__(self, classroom, window, rows, lines):
        super().__init__()
        classroom_window(self)
        self.classroom = classroom
        self.w = window
        self.rows = rows
        self.lines = lines
        self.desks = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Рассадка учеников")
        self.setGeometry(*get_pos(1000, 900, 0, -25))

        print(self.geometry())
        main_layout = QVBoxLayout()

        # Создаем 3 вертикальных ряда по 6 парт
        scroll = QScrollArea()
        classroom_scroll(scroll)
        scroll_bar(scroll.verticalScrollBar())
        scroll_bar(scroll.horizontalScrollBar())
        smooth_scroll(scroll)

        # noinspection PyUnresolvedReferences
        scroll.setAlignment(Qt.AlignCenter)

        content = QWidget()
        classroom_content(content)

        grid = QGridLayout(content)
        grid.setHorizontalSpacing(100)
        grid.setVerticalSpacing(15)

        self.desks = []
        for col in range(self.rows):
            for row in range(self.lines):  #
                desk = Desk(row, col, self)
                self.desks.append(desk)
                grid.addWidget(desk, row, col)

        scroll.setWidget(content)

        button = QPushButton("<-- Назад")
        button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: black;

                border-radius: 2px;
                padding: 2px 4px;
                font-size: 10px;
                min-width: 20px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        button.setFixedSize(60, 20)
        back_button(button)
        button.clicked.connect(self.back)

        main_layout.addWidget(button)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.arrange_students()

    def find_child_desk(self, row, col) -> Any | None:
        for desk in self.desks:
            if desk.row == row and desk.col == col:
                return desk
        return None

    def back(self):
        self.w.show()
        self.destroy()

    def arrange_students(self):
        # Очищаем все парты
        for desk in self.desks:
            desk.slot1.setText("")
            desk.slot2.setText("")

        desk_id = 0
        for row in range(self.rows):
            for line in range(self.lines):
                desk = self.desks[desk_id]

                desk.slot1.setText(str(self.classroom[row][line][0][1]))
                desk.slot2.setText(str(self.classroom[row][line][1][1]))

                desk_id += 1


class Desk(QFrame):
    def __init__(self, row, col, classroom):
        super().__init__()
        style_desk(self)
        self.slot1 = None
        self.slot2 = None

        self.row = row
        self.col = col
        self.classroom = classroom
        self.setup_ui()
        self.setAcceptDrops(True)  # Разрешаем перетаскивание на парту



    def setup_ui(self):
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setStyleSheet("background-color: #f0f0f0;")
        style_desk(self)

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(50, 5, 50, 5)

        title = QLabel(f"Ряд {self.col + 1}\nПарта {self.row + 1}")
        # noinspection PyUnresolvedReferences
        title.setAlignment(Qt.AlignCenter)
        desk_title(title)

        self.slot1 = StudentLabel(rparent=self)
        self.slot1.slot_index = 0
        self.slot2 = StudentLabel(rparent=self)
        self.slot2.slot_index = 1

        layout.addWidget(title)
        layout.addWidget(self.slot1)
        layout.addWidget(self.slot2)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText("Desk")  # Указываем, что перетаскиваем парту

            # Сохраняем информацию о текущей парте
            mime.setData("desk_pos", f"{self.row},{self.col}".encode())

            drag.setMimeData(mime)
            # noinspection PyUnresolvedReferences
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "Desk":
            event.acceptProposedAction()  # Разрешаем перетаскивание
            # noinspection PyUnresolvedReferences
            QApplication.setOverrideCursor(Qt.OpenHandCursor)  # Курсор "можно"

    def dragLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()  # Восстанавливаем курсор

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasText() and mime.text() == "Desk":
            try:
                # Получаем информацию об источнике
                desk_pos = mime.data("desk_pos").data().decode()
                src_row, src_col = map(int, desk_pos.split(','))

                # Находим исходную парту
                src_desk = self.classroom.find_child_desk(src_row, src_col)

                # Меняем местами парты
                self.swap_desks(src_desk)

                event.acceptProposedAction()
            except Exception as e:
                print(f"Error: {e}")

        QApplication.restoreOverrideCursor()  # Восстанавливаем курсор

    def swap_desks(self, other_desk):
        # Меняем местами учеников между партами
        temp_student1 = self.slot1.text()
        temp_student2 = self.slot2.text()

        self.slot1.setText(other_desk.slot1.text())
        self.slot2.setText(other_desk.slot2.text())

        other_desk.slot1.setText(temp_student1)
        other_desk.slot2.setText(temp_student2)


class StudentLabel(QLabel):
    def __init__(self, rparent: Desk, text=""):
        super().__init__(text, rparent)
        self.rparent: Desk = rparent
        # noinspection PyUnresolvedReferences
        self.setAlignment(Qt.AlignCenter)
        student_slot(self)
        self.setStyleSheet("""
            QLabel {
                border: 1px solid gray;
                padding: 5px;
                margin: 2px;
                background-color: white;
            }
        """)
        self.setMinimumSize(80, 30)
        student_slot(self)
        self.setAcceptDrops(True)  # Разрешаем перетаскивание на лейбл

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        if event.button() == Qt.LeftButton and self.text():
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.text())

            # Сохраняем информацию о текущей парте и слоте
            mime.setData("desk_pos", f"{self.rparent.row},{self.rparent.col}".encode())
            mime.setData("slot_idx", str(self.slot_index).encode())

            drag.setMimeData(mime)

            # noinspection PyUnresolvedReferences
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            # Разрешаем перетаскивание
            # noinspection PyUnresolvedReferences
            QApplication.setOverrideCursor(Qt.OpenHandCursor)  # Курсор "можно"

    def dragLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()  # Восстанавливаем курсор

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasText():
            try:
                # Получаем информацию об источнике
                desk_pos = mime.data("desk_pos").data().decode()
                src_row, src_col = map(int, desk_pos.split(','))
                if event.mimeData().text() == "Desk":
                    target_desk = self.rparent.classroom.find_child_desk(src_row, src_col)
                    self.rparent.swap_desks(target_desk)
                    event.acceptProposedAction()
                else:
                    src_slot = int(mime.data("slot_idx").data().decode())

                    # Находим исходную парту
                    src_desk = self.rparent.classroom.find_child_desk(src_row, src_col)

                    # Ученик, которого перетаскивают
                    dragged_student = mime.text()

                    # Ученик, на которого перетаскивают
                    target_student = self.text()

                    # Меняем местами учеников
                    if src_slot == 0:
                        src_desk.slot1.setText(target_student)
                    else:
                        src_desk.slot2.setText(target_student)

                    self.setText(dragged_student)

                    event.acceptProposedAction()
            except Exception as e:
                print(f"Error: {e}")

        QApplication.restoreOverrideCursor()  # Восстанавливаем курсор
