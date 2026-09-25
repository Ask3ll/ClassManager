"""Централизованные стили виджетов приложения.

Каждая функция принимает Qt-виджет и сразу применяет к нему stylesheet.
Так внешний вид элемента можно изменить в одном месте, не ища CSS по окнам.
"""


from PyQt5.QtCore import QObject, QEvent, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QAbstractItemView


class SmoothScroolFilter(QObject):
    """анимирует прокрутку колеса вместо резкого перехода между позициями."""

    def __init__(self, scroll_widget, duration=110):
        super().__init__(scroll_widget)
        self.scroll_widget = scroll_widget
        self.duration = duration
        self.animation = None

    def eventFilter(self, watched, event):
        if event.type() != QEvent.Wheel:
            return super().eventFilter(watched, event)

        bar = self.scroll_widget.verticalScrollBar()
        delta = event.angleDelta().y() or event.pixelDelta().y()
        if not delta:
            return False

        # Один импульс колеса не должен перескакивать через весь список.
        step = max(-60, min(60, int(delta * 0.35)))
        base_value = bar.value()
        if self.animation is not None and self.animation.state() == QPropertyAnimation.Running:
            base_value = self.animation.endValue()
            self.animation.stop()
        target = max(bar.minimum(), min(bar.maximum(), int(base_value) - step))

        self.animation = QPropertyAnimation(bar, b"value", self)
        self.animation.setDuration(self.duration)
        self.animation.setStartValue(bar.value())
        self.animation.setEndValue(target)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        event.accept()
        return True


def _set(widget, stylesheet):
    """Общий помощник: применяет переданный stylesheet к одному Qt-виджету."""
    """Общий внутренний помощник: применяет CSS к конкретному виджету."""
    widget.setStyleSheet(stylesheet)


# MainWindow.py: главное окно приложения и его центральный контейнер.
def main_window(widget):
    """Главное окно MainWindow.py, где пользователь добавляет и сортирует учеников."""
    _set(widget, "QMainWindow { background: #f7f8fa; }")


def central_widget(widget):
    """Центральный контейнер главного окна, содержащий все его элементы и layouts."""
    _set(widget, "QWidget { background: #f7f8fa; }")


# MainWindow.py: поле ввода фамилии и имени нового ученика.
def name_input(widget):
    """Поле имени в верхней панели MainWindow.py для добавления нового ученика."""
    _set(widget, """
        QLineEdit { border: 1px solid #b8bec8; border-radius: 4px; padding: 6px; background: white; }
        QLineEdit:focus { border: 1px solid #4b8dcc; }
    """)


# MainWindow.py: основные кнопки действий (добавить, сохранить, рассадить).
def action_button(widget):
    """Основные кнопки действий главного окна и диалога редактирования ученика."""
    _set(widget, """
        QPushButton { background: transparent; color: #111111; border: 1px solid #111111; border-radius: 4px; padding: 7px 12px; }
        QPushButton:hover { background: #eeeeee; }
        QPushButton:pressed { background: #d8d8d8; }
        QPushButton:disabled { border-color: #aaaaaa; color: #aaaaaa; }
    """)


# MainWindow.py: счётчик учеников над списком.
def counter_label(widget):
    """Счётчик учеников над списком класса в главном окне приложения."""
    _set(widget, "QLabel { color: #4d5560; font-weight: bold; padding: 4px; }")


# MainWindow.py: переключатели пола ученика.
def radio_button(widget):
    """Переключатели пола ученика рядом со счётчиком в главном окне."""
    _set(widget, "QRadioButton { spacing: 5px; color: #30343b; }")


# MainWindow.py: список учеников и строка одного ученика внутри него.
def student_list(widget):
    """Список учеников QListWidget в центральной части главного окна."""
    _set(widget, """
        QListWidget { border: 1px solid #c8cdd5; border-radius: 4px; background: white; }
        QListWidget::item { border-bottom: 1px solid #e4e7eb; }
        QListWidget::item:selected { background: #eaf3fc; color: #20242a; }
    """)


def list_row(widget):
    """Прозрачный контейнер одной строки ученика или строки предпочтения."""
    _set(widget, "QWidget { background: transparent; }")


# MainWindow.py: подпись с именем и полом ученика в строке списка.
def student_name_label(widget):
    """Подпись с именем и полом ученика внутри строки списка MainWindow.py."""
    _set(widget, "QLabel { color: #252a31; padding: 5px; }")


# EditDialog.py: окно редактирования ученика.
def edit_dialog(widget):
    """Окно EditStudentDialog.py, открываемое для изменения данных ученика."""
    _set(widget, "QDialog { background: #f7f8fa; }")


# EditDialog.py: обычные подписи разделов диалога.
def section_label(widget):
    """Заголовки разделов диалога: имя, друзья и текущие предпочтения."""
    _set(widget, "QLabel { color: #30343b; font-weight: bold; padding-top: 4px; }")


# EditDialog.py: поле изменения имени ученика.
def dialog_name_input(widget):
    """Поле изменения имени ученика в верхней части диалога редактирования."""
    name_input(widget)


# EditDialog.py: область со списком друзей и её внутренний контейнер.
def scroll_area(widget):
    """Область прокрутки со списком друзей в диалоге редактирования."""
    _set(widget, "QScrollArea { border: 1px solid #c8cdd5; background: white; }")


def scroll_content(widget):
    """Внутренний контейнер области прокрутки, где размещаются флажки друзей."""
    _set(widget, "QWidget { background: white; }")


# EditDialog.py: флажок друга ученика.
def friend_checkbox(widget):
    """Флажок с именем одного друга в списке друзей выбранного ученика."""
    _set(widget, "QCheckBox { spacing: 6px; padding: 3px; color: #30343b; }")


def scroll_bar(widget):
    """Оформляет полосу прокрутки виджета: фон, бегунок, наведение и скрытые стрелки."""
    _set(widget, """
        QScrollBar:vertical { width: 6px; background: #eef1f4; margin: 0; }
        QScrollBar::handle:vertical { min-height: 18px; background: #aeb8c4; border-radius: 3px; }
        QScrollBar::handle:vertical:hover { background: #8d99a6; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QScrollBar:horizontal { height: 6px; background: #eef1f4; margin: 0; }
        QScrollBar::handle:horizontal { min-width: 18px; background: #aeb8c4; border-radius: 3px; }
        QScrollBar::handle:horizontal:hover { background: #8d99a6; }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
    """)


# EditDialog.py: список доступных предпочтений.
def smooth_scroll(widget, duration=110):
    """Включает плавную кинетическую прокрутку для списка или области прокрутки."""
    if isinstance(widget, QAbstractItemView):
        widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
    for bar in (widget.verticalScrollBar(), widget.horizontalScrollBar()):
        bar.setSingleStep(1)
    wheel_filter = SmoothScroolFilter(widget, duration)
    widget.viewport().installEventFilter(wheel_filter)
    widget.setProperty("smooth_wheel_filter", wheel_filter)


def preferences_combo(widget):
    """Выпадающий список выбора нового предпочтения в диалоге ученика."""
    _set(widget, """
        QComboBox { border: 1px solid #b8bec8; border-radius: 4px; padding: 5px; background: white; }
        QComboBox:focus { border: 1px solid #4b8dcc; }
        QComboBox::drop-down { border: 0; width: 22px; }
    """)


# EditDialog.py: список уже добавленных предпочтений.
def preferences_list(widget):
    """Список уже добавленных предпочтений в нижней части диалога."""
    student_list(widget)


# EditDialog.py: строка предпочтения, его подпись и кнопка удаления.
def preference_row(widget):
    """Контейнер строки предпочтения с его текстом и кнопкой удаления."""
    list_row(widget)


def preference_label(widget):
    """Текст конкретного предпочтения внутри строки списка предпочтений."""
    _set(widget, "QLabel { color: #30343b; padding: 4px; }")


def delete_button(widget):
    """Красная кнопка удаления ученика или отдельного предпочтения."""
    _set(widget, """
        QPushButton { background: transparent; color: #111111; border: 1px solid #c62828; border-radius: 4px; padding: 5px 9px; }
        QPushButton:hover { background: #fff0f0; }
        QPushButton:pressed { background: #ffdada; }
    """)


# EditDialog.py: диалог выбора ученика для предпочтения "не сидеть вместе".
def input_dialog(widget):
    """Диалог выбора второго ученика для предпочтения «не сидеть вместе»."""
    _set(widget, "QInputDialog { background: #f7f8fa; }")


# EditDialog.py: сообщение об ошибке при сохранении имени.
def message_box(widget):
    """Сообщение об ошибке, показываемое при попытке сохранить некорректное имя."""
    _set(widget, "QMessageBox { background: #f7f8fa; } QMessageBox QLabel { color: #30343b; }")


# ClassroomUI.py: окно рассадки, прокрутка и её содержимое.
def classroom_window(widget):
    """Окно ClassroomUI.py с итоговой схемой рассадки учеников."""
    _set(widget, "QWidget { background: #f7f8fa; }")


def classroom_scroll(widget):
    """Прокручиваемая область, содержащая сетку парт в окне рассадки."""
    _set(widget, "QScrollArea { border: 0; background: #f7f8fa; }")


def classroom_content(widget):
    """Внутренний виджет сетки парт с единым фоном окна рассадки."""
    _set(widget, "QWidget { background: #f7f8fa; }")


# ClassroomUI.py: кнопка возврата из окна рассадки.
def back_button(widget):
    """Маленькая кнопка возврата из окна рассадки в главное окно."""
    _set(widget, """
        QPushButton { background: transparent; color: #111111; border: 1px solid #111111; border-radius: 2px; padding: 2px 4px; font-size: 10px; min-width: 20px; min-height: 20px; }
        QPushButton:hover { background: #eeeeee; }
        QPushButton:pressed { background: #d8d8d8; }
    """)


# ClassroomUI.py: рамка одной парты и заголовок с номером ряда/парты.
def desk(widget):
    """Рамка одной парты в сетке окна ClassroomUI.py."""
    _set(widget, "QFrame { background: #f0f0f0; }")


def desk_title(widget):
    """Заголовок парты с номером ряда и номером парты."""
    _set(widget, "QLabel { color: #30343b; font-weight: bold; }")


# ClassroomUI.py: подпись ученика на месте за партой (drag-and-drop).
def student_slot(widget):
    """Место ученика на парте с рамкой и подсветкой при наведении."""
    _set(widget, """
        QLabel { border: 1px solid gray; border-radius: 2px; padding: 5px; margin: 2px; background: white; color: #20242a; }
        QLabel:hover { background: #eef6ff; }
    """)
