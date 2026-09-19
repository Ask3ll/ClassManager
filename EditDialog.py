from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, \
    QDialog, QLineEdit, QListWidget, QInputDialog, QHBoxLayout, QListWidgetItem, QCheckBox, \
     QComboBox, QMessageBox, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from utils import *
from Prefers import *

# TODO
# 1. Add sex change
class EditStudentDialog(QDialog):
    def __init__(self, student, students, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Редактировать ученика")
        self.setGeometry(*get_pos(400, 400))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.student = student
        self.students = students

        layout = QVBoxLayout(self)

        # Поле для редактирования имени
        self.name_input = QLineEdit(self.student.name, self)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Друзья:")) # провеит


        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        self.friends_layout = QVBoxLayout(scroll_widget)
        # noinspection PyUnresolvedReferences
        self.friends_layout.setAlignment(Qt.AlignTop)
        # Добавляем чекбоксы для выбора друзей
        self.friend_checkboxes = []
        for other_student in self.students:
            if other_student != self.student:  # Исключаем текущего ученика
                checkbox = QCheckBox(other_student.name, self)
                checkbox.setChecked(other_student in self.student.friends)
                self.friend_checkboxes.append((checkbox, other_student))
                self.friends_layout.addWidget(checkbox)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Выпадающий список для пожеланий
        layout.addWidget(QLabel("Пожелания:"))
        self.prefers_combo = QComboBox(self)

        items = list(map(str, all_prefers))
        items.insert(0, "-")
        self.prefers_combo.addItems(items)

        self.prefers_combo.currentTextChanged.connect(self.handle_prefer_change)  # Обработчик изменения

        # Если учеников меньше двух, отключаем пункт "Нельзя сажать с этим учеником"
        if len(self.students) <= 1:
            index = self.prefers_combo.findText(DoNotSeatWithPrefer().text)
            if index != -1:
                # noinspection PyUnresolvedReferences
                self.prefers_combo.setItemData(index, QColor(Qt.gray), Qt.TextColorRole)  # Серый цвет
                self.prefers_combo.model().item(index).setEnabled(False)  # Отключаем пункт

        layout.addWidget(self.prefers_combo)

        # Кнопка "Добавить пожелание"
        self.add_prefer_button = QPushButton("Добавить пожелание", self)
        self.add_prefer_button.clicked.connect(self.add_prefer)
        layout.addWidget(self.add_prefer_button)

        # Список текущих пожеланий
        self.prefers_list = QListWidget(self)
        layout.addWidget(QLabel("Текущие пожелания:"))
        layout.addWidget(self.prefers_list)

        # Кнопки "Сохранить" и "Отмена"
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_changes)
        buttons_layout.addWidget(save_button)
        layout.addLayout(buttons_layout)

        # Обновляем списки друзей и пожеланий
        self.update_prefers_list()
        self.update_prefers_combo()  # Обновляем состояние выпадающего списка
    def disable_prefer(self, prefer):
        index = self.prefers_combo.findText(prefer().text)
        if index != -1:
            self.prefers_combo.setItemData(index, QColor(Qt.gray), Qt.TextColorRole)
            self.prefers_combo.model().item(index).setEnabled(False)
    def update_prefers_combo(self):
        """Обновляет состояние выпадающего списка на основе уже выбранных пожеланий."""
        self.prefers_combo.blockSignals(True)
        for i in range(self.prefers_combo.count()):
            text = self.prefers_combo.itemText(i)
            if text in self.student.prefers:
                # Если пожелание уже выбрано, делаем его серым и отключаем
                self.prefers_combo.setItemData(i, QColor(Qt.gray), Qt.TextColorRole)
                self.prefers_combo.model().item(i).setEnabled(False)
            else:
                # Если пожелание не выбрано, включаем его
                self.prefers_combo.setItemData(i, QColor(Qt.black), Qt.TextColorRole)
                self.prefers_combo.model().item(i).setEnabled(True)

        # Если учеников меньше двух, убедимся, что пункт "Нельзя сажать с этим учеником" отключен
        if len(self.students) <= 1:
            self.disable_prefer(DoNotSeatWithPrefer)

        if SeatNextToMalePrefer in self.student.prefers:
            self.disable_prefer(SeatNextToFemalePrefer)

        if SeatNextToFemalePrefer in self.student.prefers:
            self.disable_prefer(SeatNextToMalePrefer)

        if VisionPrefer in self.student.prefers:
            self.disable_prefer(SeatInBackPrefer)
            self.disable_prefer(SeatInMiddlePrefer)
            self.disable_prefer(SeatInFrontPrefer)

        if SeatInBackPrefer in self.student.prefers:
            self.disable_prefer(VisionPrefer)
            self.disable_prefer(SeatInMiddlePrefer)
            self.disable_prefer(SeatInFrontPrefer)

        if SeatInMiddlePrefer in self.student.prefers:
            self.disable_prefer(VisionPrefer)
            self.disable_prefer(SeatInBackPrefer)
            self.disable_prefer(SeatInFrontPrefer)

        if SeatInFrontPrefer in self.student.prefers:
            self.disable_prefer(VisionPrefer)
            self.disable_prefer(SeatInBackPrefer)
            self.disable_prefer(SeatInMiddlePrefer)

        others = []
        for prefer in self.student.prefers:
            if isinstance(prefer, DoNotSeatWithPrefer):
                others.append(prefer.other_student)
        if len(others) == len(self.student.window.students) - 1:
            self.disable_prefer(DoNotSeatWithPrefer)

        self.prefers_combo.setCurrentIndex(0)
        self.prefers_combo.blockSignals(False)
    def handle_prefer_change(self, text):
        if text != "-":
            prefer = prefers_dict[text]
            if prefer is DoNotSeatWithPrefer:
                # Создаем QInputDialog
                dialog = QInputDialog(self)
                dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Убираем вопросительный знак
                dialog.setWindowTitle("Выберите ученика")
                dialog.setLabelText("Ученик:")

                exclude = [self.student]
                for prefer in self.student.prefers:
                    if isinstance(prefer, DoNotSeatWithPrefer):
                        exclude.append(prefer.other_student)

                dialog.setComboBoxItems([s.name for s in self.students if s not in exclude])
                dialog.setOption(QInputDialog.UseListViewForComboBoxItems)  # Используем список вместо выпадающего меню
                if dialog.exec_() == QDialog.Accepted:
                    student = dialog.textValue()
                    if student:
                        other_student = self.parent().get_student_by_name(student)

                        self.student.prefers.append(DoNotSeatWithPrefer, other_student.id)
                        other_student.prefers.append(DoNotSeatWithPrefer, self.student.id)

                        self.update_prefers_list()
                        self.update_prefers_combo()  # Обновляем состояние выпадающего списка

    def add_prefer(self):
        if self.prefers_combo.currentText() != "-":
            prefer = prefers_dict[self.prefers_combo.currentText()]

            if isinstance(prefer, DoNotSeatWithPrefer):
                # Если выбрано это пожелание, вызываем handle_prefer_change
                self.handle_prefer_change(prefer.__str__())
            elif prefer and prefer not in self.student.prefers:
                # Добавляем обычное пожелание
                self.student.prefers.append(prefer)
                self.update_prefers_list()
                self.update_prefers_combo()  # Обновляем состояние выпадающего списка

    def update_prefers_list(self):
        """Обновляет список пожеланий с кнопками удаления."""
        self.prefers_list.clear()
        for prefer in self.student.prefers:
            item = QListWidgetItem()
            self.prefers_list.addItem(item)

            # Создаем виджет для отображения пожелания и кнопки удаления
            widget = QWidget()
            layout = QHBoxLayout(widget)

            # Метка с текстом пожелания
            prefer_label = QLabel(str(prefer))
            layout.addWidget(prefer_label)

            # Кнопка "Удалить"
            delete_button = QPushButton("Удалить", self)
            delete_button.clicked.connect(lambda _, p=prefer: self.delete_prefer(p))
            layout.addWidget(delete_button)

            # Устанавливаем виджет для элемента списка
            self.prefers_list.setItemWidget(item, widget)

            # Устанавливаем высоту элемента списка
            item.setSizeHint(widget.sizeHint())

    def delete_prefer(self, prefer):
        """Удаляет пожелание из списка."""
        if prefer in self.student.prefers:
            if isinstance(prefer, DoNotSeatWithPrefer):
                self.student.prefers.remove(DoNotSeatWithPrefer, prefer.other_student_id)
                name = prefer.other_student.name
                for student in self.students:
                    if name == student.name:
                        student.prefers.remove(DoNotSeatWithPrefer, self.student.id)
                        break
            else:
                self.student.prefers.remove(prefer)
            self.update_prefers_list()  # Обновляем список пожеланий
            self.update_prefers_combo()  # Обновляем состояние выпадающего списка

    def save_changes(self):
        # Обновляем список друзей
        self.student.friends = []
        for checkbox, other_student in self.friend_checkboxes:
            if checkbox.isChecked():
                self.student.add_to_friends(other_student)
                if self.student not in other_student.friends:
                    other_student.add_to_friends(self.student)
            elif not checkbox.isChecked():
                if self.student in other_student.friends:
                    other_student.del_from_friends(self.student)
        # Сохраняем новое имя
        if (self.name_input.text() != "" and self.name_input.text() not in list(
                map(str, self.students))) or self.name_input.text() == self.student.name:
            self.student.name = self.name_input.text()
            self.accept()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)  # Стандартная иконка "Critical"
            msg.setWindowTitle("Имя не сохранено")
            msg.setText("Некорректное имя")

            # Устанавливаем стандартную иконку Qt
            msg.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))

            # Показываем сообщение
            msg.exec_()