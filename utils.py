import ctypes


def get_pos(x_size, y_size, x_offset=0, y_offset=0):
    # noinspection PyUnresolvedReferences
    w, h = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    return ((w - x_size) // 2) + x_offset, ((h - y_size) // 2) + y_offset, x_size, y_size


rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def get_surname(std):
    return std.name.split(" ")[0]
