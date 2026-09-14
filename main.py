import sys

from MainWindow import *

# set QT_QPA_PLATFORM_PLUGIN_PATH=C:\Users\Максим\Desktop\Программы\class_manager\.venv\Lib\site-packages\PyQt5\Qt5\plugins


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
