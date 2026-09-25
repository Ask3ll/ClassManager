from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, \
    QDialog, QLineEdit, QListWidget, QInputDialog, QHBoxLayout, QListWidgetItem, QCheckBox, \
    QComboBox, QMessageBox, QStyle, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


from utils import *
from Prefers import *
from styles import (
    action_button, dialog_name_input, edit_dialog, friend_checkbox,
    input_dialog, message_box, preference_label, preference_row,
    preferences_combo, preferences_list, scroll_bar, smooth_scroll, scroll_content, section_label,
    delete_button as style_delete_button,
    scroll_area as style_scroll_area, radio_button
)


# TODO
# 1. Add sex change

class EditStudentDialog(QDialog):
    def __init__(self, student, students, parent=None):
        super().__init__(parent)
        edit_dialog(self)

        self.setWindowTitle("Редактировать ученика")
        self.setGeometry(*get_pos(400, 600))
        # noinspection PyUnresolvedReferences
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.student = student
        self.students = students

        layout = QVBoxLayout(self)

        # Поле для редактирования имени
        self.name_input = QLineEdit(self.student.name, self)
        dialog_name_input(self.name_input)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)

        # радиокнопки для выбора пола
        self.sex_layout = QHBoxLayout()
        # noinspection PyUnresolvedReferences
        self.sex_layout.setAlignment(Qt.AlignLeft)
        self.male_radio = QRadioButton("Мальчик", self)
        self.female_radio = QRadioButton("Девочка", self)
        if student.sex == "Мальчик":
            self.male_radio.setChecked(True)
        else:
            self.female_radio.setChecked(True)
        radio_button(self.male_radio)


        self.sex_group = QButtonGroup(self)
        self.sex_group.addButton(self.male_radio)
        self.sex_group.addButton(self.female_radio)
        radio_button(self.female_radio)
        self.sex_layout.addWidget(self.male_radio)
        self.sex_layout.addWidget(self.female_radio)

        layout.addLayout(self.sex_layout)

        layout.addWidget(QLabel("Друзья:"))  # провеит

        scroll_area = QScrollArea(self)
        style_scroll_area(scroll_area)
        scroll_bar(scroll_area.verticalScrollBar())
        scroll_bar(scroll_area.horizontalScrollBar())
        smooth_scroll(scroll_area)
        scroll_widget = QWidget()
        scroll_content(scroll_widget)
        self.friends_layout = QVBoxLayout(scroll_widget)
        # noinspection PyUnresolvedReferences
        self.friends_layout.setAlignment(Qt.AlignTop)
        # Добавляем чекбоксы для выбора друзей
        self.friend_checkboxes = []
        for other_student in self.students:
            if other_student != self.student:  # Исключаем текущего ученика
                checkbox = QCheckBox(other_student.name, self)
                friend_checkbox(checkbox)
                checkbox.setChecked(other_student in self.student.friends)
                self.friend_checkboxes.append((checkbox, other_student))
                self.friends_layout.addWidget(checkbox)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Выпадающий список для пожеланий
        layout.addWidget(QLabel("Пожелания:"))
        self.prefers_combo = QComboBox(self)
        preferences_combo(self.prefers_combo)

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
                # noinspection PyUnresolvedReferences
                self.prefers_combo.model().item(index).setEnabled(False)  # Отключаем пункт

        layout.addWidget(self.prefers_combo)

        # Кнопка "Добавить пожелание"
        self.add_prefer_button = QPushButton("Добавить пожелание", self)
        self.add_prefer_button.clicked.connect(self.add_prefer)
        action_button(self.add_prefer_button)
        layout.addWidget(self.add_prefer_button)

        # Список текущих пожеланий
        self.prefers_list = QListWidget(self)
        preferences_list(self.prefers_list)
        scroll_bar(self.prefers_list.verticalScrollBar())
        smooth_scroll(self.prefers_list)
        layout.addWidget(QLabel("Текущие пожелания:"))
        layout.addWidget(self.prefers_list)

        # Кнопки "Сохранить" и "Отмена"
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_changes)
        action_button(save_button)
        buttons_layout.addWidget(save_button)
        layout.addLayout(buttons_layout)

        # Обновляем списки друзей и пожеланий
        self.update_prefers_list()
        self.update_prefers_combo()  # Обновляем состояние выпадающего списка

        for label in self.findChildren(QLabel):
            section_label(label)

    # noinspection PyUnresolvedReferences
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
                # noinspection PyUnresolvedReferences
                # Если пожелание уже выбрано, делаем его серым и отключаем
                self.prefers_combo.setItemData(i, QColor(Qt.gray), Qt.TextColorRole)

                # noinspection PyUnresolvedReferences
                self.prefers_combo.model().item(i).setEnabled(False)
            else:
                # noinspection PyUnresolvedReferences
                # Если пожелание не выбрано, включаем его
                self.prefers_combo.setItemData(i, QColor(Qt.black), Qt.TextColorRole)

                # noinspection PyUnresolvedReferences
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
                input_dialog(dialog)
                dialog.setOkButtonText("Выбрать")
                dialog.setCancelButtonText("Отмена")
                # noinspection PyUnresolvedReferences
                dialog.setWindowFlags(
                    dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Убираем вопросительный знак
                dialog.setWindowTitle("Выберите ученика")
                dialog.setLabelText("Ученик:")

                exclude = [self.student]
                for prefer in self.student.prefers:
                    if isinstance(prefer, DoNotSeatWithPrefer):
                        exclude.append(prefer.other_student)

                dialog.setComboBoxItems([s.name for s in self.students if s not in exclude])
                combo_box = dialog.findChild(QComboBox)
                if combo_box:
                    smooth_scroll(combo_box.view(), duration=180)
                dialog.setOption(QInputDialog.UseListViewForComboBoxItems)  # Используем список вместо выпадающего меню
                if dialog.exec_() == QDialog.Accepted:
                    student = dialog.textValue()
                    if student:
                        # noinspection PyUnresolvedReferences
                        other_student = self.parent().get_student_by_name(student)
                        # noinspection PyUnresolvedReferences
                        self.student.prefers.append(DoNotSeatWithPrefer, other_student.id)
                        # noinspection PyUnresolvedReferences
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
            preference_row(widget)
            layout = QHBoxLayout(widget)

            # Метка с текстом пожелания
            prefer_label = QLabel(str(prefer))
            preference_label(prefer_label)
            layout.addWidget(prefer_label)

            # Кнопка "Удалить"
            delete_button = QPushButton("Удалить", self)
            delete_button.clicked.connect(lambda _, p=prefer: self.delete_prefer(p))
            style_delete_button(delete_button)
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
            if self.male_radio.isChecked():
                self.student.sex = "Мальчик"
            else:
                self.student.sex = "Девочка"
            self.accept()
        else:
            msg = QMessageBox(self)
            message_box(msg)
            msg.setIcon(QMessageBox.Critical)  # Стандартная иконка "Critical"
            msg.setWindowTitle("Имя не сохранено")
            msg.setText("Некорректное имя")

            # Устанавливаем стандартную иконку Qt
            # noinspection PyUnresolvedReferences
            msg.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))

            # Показываем сообщение
            msg.exec_()
