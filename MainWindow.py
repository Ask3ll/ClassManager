import os
import winsound
from PyQt5.QtWidgets import QMainWindow, QRadioButton, QButtonGroup
from pathlib import Path

from ClassroomUI import *
from EditDialog import *
from Student import *


# TODO
# 1. Отображение у кого есть prefers а у кого есть

# to-build: .\.venv\Scripts\pyinstaller.exe -D -w main.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление учениками")
        self.setGeometry(*get_pos(900, 900))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # горизонтальный layout для поля ввода и кнопки
        self.input_layout = QHBoxLayout()
        self.qle = QLineEdit(self)
        self.qle.setPlaceholderText("Фамилия Имя")
        self.add_button = QPushButton("Добавить ученика", self)
        self.add_button.clicked.connect(self.add_student)
        self.input_layout.addWidget(self.qle)
        self.input_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save)
        self.input_layout.addWidget(self.save_button)

        # students counter
        self.counter_layout = QHBoxLayout()
        # noinspection PyUnresolvedReferences
        self.counter_layout.setAlignment(Qt.AlignLeft)
        self.text_counter = QLabel(self)
        self.text_counter.setText("Пустой класс")
        self.counter_layout.addWidget(self.text_counter)

        # радиокнопки для выбора пола
        self.sex_layout = QHBoxLayout()
        # noinspection PyUnresolvedReferences
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

        self.mix_layout = QHBoxLayout()
        self.mix_layout.addLayout(self.counter_layout)
        self.mix_layout.addLayout(self.sex_layout)
        self.layout.addLayout(self.mix_layout)

        # self.layout.addLayout(self.sex_layout)
        # self.layout.addLayout(self.counter_layout)

        self.student_list = QListWidget(self)
        self.layout.addWidget(self.student_list)

        self.start_button = QPushButton("Рассадить учеников", self)
        self.start_button.clicked.connect(self._sort)
        self.layout.addWidget(self.start_button)

        self.students = []
        self.new_stud_id = 0
        self.check_save()

        # rows и lines, можно изменять
        self.rows = 3
        self.lines = 6

    def updateCounter(self):
        n = len(self.students)

        n100 = n % 100
        n10 = n % 10
        if n == 0:
            self.text_counter.setText("Пустой класс")
            return

        if 11 <= n100 <= 14:
            self.text_counter.setText(f"{n} учеников")
            return
        if n10 == 1:
            self.text_counter.setText(f"{n} ученик")
            return
        if 2 <= n10 <= 4:
            self.text_counter.setText(f"{n} ученика")
            return

        self.text_counter.setText(f"{n} учеников")

    def save(self, mute=False):

        save_dir = Path(os.path.expandvars(r"%appdata%\ClassManager"))

        save_dir.mkdir(parents=True, exist_ok=True)

        studs_file_path = save_dir / "classman_save.jsonl"
        studs_file_path.touch(exist_ok=True)
        studs_file_path.write_text("\n".join(map(lambda student: student.convert_to_str(), self.students)), "utf-8")

        data_file_path = save_dir / "classman_settings.ini"
        data_file_path.touch(exist_ok=True)
        data_file_path.write_text(str(self.new_stud_id), "utf-8")
        if not mute:
            winsound.MessageBeep(winsound.MB_OK)

    def check_save(self):

        save_dir = Path(os.path.expandvars(r"%appdata%\ClassManager"))
        save_dir.mkdir(parents=True, exist_ok=True)
        # classman_save_*.jsonl
        settings_file = None
        for file in save_dir.glob("classman_settings.ini"):
            settings_file = file
            self.new_stud_id = int(file.read_text(encoding="utf-8"))

        for file in save_dir.glob("classman_save.jsonl"):
            for line in file.read_text(encoding="utf-8").split("\n"):
                if line.strip():
                    # noinspection PyBroadException
                    try:
                        data = json.loads(line)

                        self.students.append(Student(self, **data))
                    except Exception:
                        self.new_stud_id = 0
                        self.students.clear()
                        file.unlink(missing_ok=True)
                        if settings_file:
                            settings_file.unlink(missing_ok=True)
                        return
            self.update_student_list()
            break

    def _sort(self):
        classroom = []
        seats = []

        for row in range(self.rows):
            classroom.append([])

            for line in range(self.lines):
                classroom[row].append([[0, "-"], [0, "-"]])

                seats.append((row, line, 0))
                seats.append((row, line, 1))

        lstudents = self.students.copy()

        # random.shuffle(seats)
        seated = 0
        while seated != len(self.students):

            for column, row, seat in seats:
                highest = [0, "-"]
                for student in lstudents:
                    score = student.seat(classroom, row, column, seat)
                    if score >= highest[0]:
                        highest = [score, student]
                        continue
                classroom[column][row][seat] = highest
                if highest[1] != "-":
                    lstudents.remove(highest[1])
                    seated += 1
            print(seated)

        print(classroom, )
        swindow = Classroom(classroom, self, self.rows, self.lines)
        self.hide()
        swindow.show()

    def add_student(self):
        if self.qle.text() != "" and self.qle.text() not in list(map(str, self.students)) and set(
                self.qle.text().lower()) <= set(rus + " "):
            sex = "Мальчик" if self.male_radio.isChecked() else "Девочка"
            student = Student(self, self.qle.text(), sex)
            self.students.append(student)
            self.update_student_list()
            self.qle.clear()  # Очищаем поле ввода после добавления
        else:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

    @property
    def students_sorted(self):
        if not self.students:
            return self.students
        return sorted(self.students, key=get_surname)

    def closeEvent(self, a0, QCloseEvent=None):
        self.save(mute=True)

    def update_student_list(self):
        self.updateCounter()
        if not self.students:
            self.new_stud_id = 0

        scroll_bar = self.student_list.verticalScrollBar()
        # noinspection PyUnresolvedReferences
        scroll_position = scroll_bar.value()

        self.student_list.clear()

        for student in self.students_sorted:
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
        # noinspection PyUnresolvedReferences
        scroll_bar.setValue(scroll_position)

    def edit_student(self, student):
        # Открываем окно редактирования ученика
        dialog = EditStudentDialog(student, self.students, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_student_list()

    def get_student(self, student_id):
        student_id = int(student_id)
        for student in self.students:
            if student.id == student_id:
                return student
        raise Exception(f"Student not found, id: {student_id}")

    def get_student_by_name(self, student_name):
        for student in self.students:
            if student.name == student_name:
                return student
        raise Exception(f"Student not found, name: {student_name}")

    def delete_student(self, student):
        for _student in student.friends:
            _student.del_from_friends(student)

        for _student in self.students:
            for prefer in _student.prefers:
                if isinstance(prefer, DoNotSeatWithPrefer):
                    if prefer.other_student == self:
                        _student.prefers.remove(prefer, student.id)
        self.students.remove(student)
        self.update_student_list()
