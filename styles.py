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
    _set(widget, "QWidget { background-color: #f1f5f9; }")


def classroom_scroll(widget):
    """Прокручиваемая область, содержащая сетку парт в окне рассадки."""
    _set(widget, """
           QScrollArea { border: none; background: transparent; }
           QScrollBar:vertical {
               border: none;
               background: #e2e8f0;
               width: 8px;
               border-radius: 4px;
           }
           QScrollBar::handle:vertical {
               background: #cbd5e1;
               border-radius: 4px;
           }
           QScrollBar::handle:vertical:hover {
               background: #94a3b8;
           }
       """)


# ClassroomUI.py: окно рассадки, прокрутка и её содержимое.
def classroom_window(widget):
    """Окно ClassroomUI.py с итоговой схемой рассадки учеников."""
    _set(widget, "QWidget { background-color: #f1f5f9; }")


def classroom_scroll(widget):
    """Прокручиваемая область, содержащая сетку парт в окне рассадки."""
    _set(widget, """
        QScrollArea { border: none; background: transparent; }
        QScrollBar:vertical {
            border: none;
            background: #e2e8f0;
            width: 8px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #cbd5e1;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #94a3b8;
        }
        QScrollBar:horizontal {
            height: 0px; /* Отключаем горизонтальный скроллбар */
        }
    """)
    # Включаем подгонку содержимого под ширину окна
    widget.setWidgetResizable(True)


def classroom_content(widget):
    """Внутренний виджет сетки парт с единым фоном окна рассадки."""
    _set(widget, "QWidget { background: transparent; }")


# ClassroomUI.py: кнопка возврата из окна рассадки.
def back_button(widget):
    """Кнопка возврата с оптимальным размером."""
    _set(widget, """
        QPushButton {
            background-color: #ffffff;
            color: #475569;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 600;
            min-width: 60px;
            min-height: 22px;
        }
        QPushButton:hover {
            background-color: #f8fafc;
            color: #0f172a;
            border-color: #94a3b8;
        }
        QPushButton:pressed {
            background-color: #e2e8f0;
        }
    """)


# ClassroomUI.py: рамка одной парты и заголовок с номером ряда/парты.
def desk(widget):
    """Компактная рамка парты."""
    _set(widget, """
        QFrame {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 2px;
        }
    """)


def desk_title(widget):
    """Заголовок парты с номером ряда и номером парты."""
    _set(widget, """
        QLabel {
            color: #64748b;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.3px;
            padding-bottom: 1px;
        }
    """)


# ClassroomUI.py: подпись ученика на месте за партой (drag-and-drop).
def student_slot(widget):
    """Компактное место ученика, отлично вмещающееся в 3 колонки."""
    _set(widget, """
        QLabel {
            border: 1.5px dashed #cbd5e1;
            border-radius: 5px;
            padding: 3px 4px;
            margin: 1px;
            background-color: #f8fafc;
            color: #1e293b;
            font-size: 10px;
            font-weight: 500;
            min-width: 90px;
            qproperty-wordWrap: true;
            qproperty-alignment: 'AlignCenter';
        }
        QLabel:hover {
            background-color: #eff6ff;
            border: 1.5px solid #3b82f6;
            color: #1d4ed8;
        }
    """)