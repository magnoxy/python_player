from PyQt5.QtWidgets import QApplication
# from src.gui.main_window import MainWindow
from src.gui.main import MainWindow as MW
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec_())
