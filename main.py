import sys
from PyQt5.QtWidgets import QApplication
from ui_main import EncryptionApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec_())