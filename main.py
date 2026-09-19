import sys

from MainWindow import *

# set QT_QPA_PLATFORM_PLUGIN_PATH=C:\Users\Максим\Desktop\Программы\class_manager\.venv\Lib\site-packages\PyQt5\Qt5\plugins

# to-build: .\.venv\Scripts\pyinstaller.exe -D -w main.py
# .venv\Scripts\pyinstaller.exe -D -w -n ClassManager --icon="latest-build\app.ico" --distpath="latest-build" main.py && rmdir /s /q build && del /q ClassManager.spec

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
