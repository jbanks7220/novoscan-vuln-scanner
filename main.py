import sys
from PyQt5.QtWidgets import QApplication
from gui.gui_scanner import ScannerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScannerGUI()
    window.show()
    sys.exit(app.exec())
