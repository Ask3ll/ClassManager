import json
import os
import random
import winsound
from PyQt5.QtWidgets import QMainWindow, QDialog, QLineEdit, QListWidget, QHBoxLayout, QListWidgetItem, QRadioButton,  QButtonGroup
from pathlib import Path

from ClassroomUI import *
from EditDialog import *
from Student import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление учениками")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Горизонтальный layout для поля ввода и кнопки
        self.input_layout = QHBoxLayout()
        self.qle = QLineEdit(self)
        self.qle.setPlaceholderText("Имя Ученика")
        self.add_button = QPushButton("Добавить ученика", self)
        self.add_button.clicked.connect(self.add_student)
        self.input_layout.addWidget(self.qle)
        self.input_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save)
        self.input_layout.addWidget(self.save_button)

        # Радиокнопки для выбора пола
        self.sex_layout = QHBoxLayout()
        self.sex_layout.setAlignment(Qt.AlignRight)
        self.male_radio = QRadioButton("Мальчик", self)
        self.male_radio.setChecked(True)
        self.female_radio = QRadioButton("Девочка", self)
        self.sex_group = QButtonGroup(self)
        self.sex_group.addButton(self.male_radio)
        self.sex_group.addButton(self.female_radio)
        self.sex_layout.addWidget(self.male_radio)
        self.sex_layout.addWidget(self.female_radio)
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.sex_layout)

        self.student_list = QListWidget(self)
        self.layout.addWidget(self.student_list)

        self.start_button = QPushButton("Рассадить учеников", self)
        self.start_button.clicked.connect(self._sort)
        self.layout.addWidget(self.start_button)

        self.students = []
        self.check_save()

    def save(self, mute=False):

        save_dir = Path(os.path.expandvars(r"%appdata%\ClassManager"))
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / "classman_save.jsonl"
        file_path.touch(exist_ok=True)

        file_path.write_text("\n".join(map(lambda x: x.convert_to_str(), self.students)), "utf-8")
        if not mute:
            winsound.MessageBeep(winsound.MB_OK)

    def check_save(self):
        save_dir = Path(os.path.expandvars(r"%appdata%\ClassManager"))
        save_dir.mkdir(parents=True, exist_ok=True)
        # classman_save_*.jsonl
        for file in save_dir.glob("classman_save.jsonl"):
            for line in file.read_text(encoding="utf-8").split("\n"):
                if line.strip():
                    try:
                        data = json.loads(line)
                        print(data)
                        self.students.append(Student(self, **data))
                    except Exception:
                        self.students.clear()
                        file.unlink(missing_ok=True)
                        return
            self.update_student_list()
            break

    def _sort(self):
        classroom = [[], [], []]
        # while len(classroom[0]) + len(classroom[1]) + len(classroom[2]) != len(self.students):
        classroom[0] = [[[0, "-"], [0, "-"]] for _ in range(6)]
        classroom[1] = [[[0, "-"], [0, "-"]] for _ in range(6)]
        classroom[2] = [[[0, "-"], [0, "-"]] for _ in range(6)]
        lstudents = self.students.copy()

        seats = []

        for column in range(3):
            for row in range(6):
                for seat in range(0, 2):
                    seats.append((column, row, seat))

        random.shuffle(seats)

        for column, row, seat in seats:
            if not lstudents:
                break
            highest = [0, None]
            if lstudents:
                for student in lstudents:
                    st = student.seat(row, column, seat, classroom)
                    if st >= highest[0]:
                        highest = [st, student]
                classroom[column][row][seat] = highest
                if highest[1] is not None:
                    lstudents.remove(highest[1])
            else:
                break
        swindow = Classroom(classroom, self)
        self.hide()
        swindow.show()

    def add_student(self):
        if self.qle.text() != "" and self.qle.text() not in list(map(str, self.students)):
            sex = "Мальчик" if self.male_radio.isChecked() else "Девочка"
            student = Student(self, self.qle.text(), len(self.students), sex)
            self.students.append(student)
            self.update_student_list()
            self.qle.clear()  # Очищаем поле ввода после добавления
        else:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

    def closeEvent(self, a0, QCloseEvent=None):
        self.save(mute=True)

    def update_student_list(self):
        self.student_list.clear()
        for student in self.students:
            item = QListWidgetItem()
            self.student_list.addItem(item)
            # Создаем виджет для отображения имени и кнопок
            widget = QWidget()
            layout = QHBoxLayout(widget)

            # Метка с именем ученика
            name_label = QLabel(f"{student.name} ({student.sex})")
            layout.addWidget(name_label)

            # Кнопка "Редактировать"
            edit_button = QPushButton("Редактировать")
            edit_button.clicked.connect(lambda _, s=student: self.edit_student(s))
            layout.addWidget(edit_button)

            # Кнопка "Удалить"
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda _, s=student: self.delete_student(s))
            layout.addWidget(delete_button)

            # Устанавливаем виджет для элемента списка
            self.student_list.setItemWidget(item, widget)

            # Устанавливаем высоту элемента списка
            item.setSizeHint(widget.sizeHint())

    def edit_student(self, student):
        # Открываем окно редактирования ученика
        dialog = EditStudentDialog(student, self.students, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_student_list()

    def delete_student(self, student):
        for _student in student.friends:
            _student.del_from_friends(student)
        for _student in self.students:
            for prefer in _student.prefers:
                if prefer[len("Нельзя сажать с "):] == f"{student.name}":
                    _student.prefers.remove(prefer)
        self.students.remove(student)
        self.update_student_list()