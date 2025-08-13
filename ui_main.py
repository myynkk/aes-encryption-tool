from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout,
    QHBoxLayout, QMessageBox, QProgressBar, QListWidget, QListWidgetItem,
    QStackedWidget, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
import threading
from crypto_utils import encrypt_file, decrypt_file

def blue_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(33, 47, 60))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(44, 62, 80))
    palette.setColor(QPalette.AlternateBase, QColor(52, 73, 94))
    palette.setColor(QPalette.ToolTipBase, QColor(236, 240, 241))
    palette.setColor(QPalette.ToolTipText, QColor(44, 62, 80))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(41, 128, 185))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(41, 128, 185))
    palette.setColor(QPalette.Highlight, QColor(41, 128, 185))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    return palette

class Sidebar(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(180)
        self.setFrameShape(QFrame.NoFrame)
        self.setSpacing(2)
        items = ["Encrypt File", "Decrypt File", "About"]
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFont(QFont("Segoe UI", 12))
            list_item.setForeground(QColor(255,255,255))
            self.addItem(list_item)
        self.setCurrentRow(0)
        self.setStyleSheet("""
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #6dd5fa);
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 2px solid #34495e;
            }
            QListWidget::item:selected {
                background: #1abc9c;
                color: #fff;
                border-left: 4px solid #3498db;
            }
        """)

class EncryptPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.file_path = ""
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #1abc9c; font-weight: bold; margin: 8px;")
        self.label = QLabel("Select a file to encrypt:")
        self.label.setStyleSheet("color: #3498db; font-size: 16px; font-weight: bold;")
        self.file_display = QLabel("")
        self.file_display.setStyleSheet("color: #fff; padding: 6px; background: #34495e; border-radius: 6px;")
        self.select_btn = QPushButton("Browse File")
        self.select_btn.setStyleSheet(
            "background-color: #2980b9; color: #fff; border-radius: 8px; padding: 7px 14px; font-size: 14px;")
        self.select_btn.setFont(QFont("Segoe UI", 11))
        self.select_btn.clicked.connect(self.browse_file)

        self.pass_label = QLabel("Enter password:")
        self.pass_label.setStyleSheet("color: #3498db; font-size: 16px; font-weight: bold;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(
            "background: #34495e; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.setStyleSheet(
            "background-color: #1abc9c; color: #fff; border-radius: 8px; padding: 10px 20px; font-size: 15px; font-weight: bold;")
        self.encrypt_btn.setFont(QFont("Segoe UI", 12))
        self.encrypt_btn.clicked.connect(self.encrypt_file_action)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet("QProgressBar { background: #34495e; color: #fff; border-radius: 6px; } QProgressBar::chunk { background: #3498db; }")
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_display)
        file_layout.addWidget(self.select_btn)
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.encrypt_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addStretch()
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if file_path:
            self.file_path = file_path
            self.file_display.setText(file_path)
            self.status_label.setText("")

    def encrypt_file_action(self):
        self.status_label.setText("")
        if not self.file_path or not self.pass_input.text():
            self.status_label.setText("Please select a file and enter a password.")
            return
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File")
        if not output_path:
            return
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        def run():
            try:
                encrypt_file(self.file_path, output_path, self.pass_input.text())
                self.status_label.setText("Encryption completed successfully!")
            except Exception as e:
                self.status_label.setText(f"Encryption failed: {str(e)}")
            finally:
                self.progress.setVisible(False)
        threading.Thread(target=run).start()

class DecryptPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.file_path = ""
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #1abc9c; font-weight: bold; margin: 8px;")
        self.label = QLabel("Select an encrypted file to decrypt:")
        self.label.setStyleSheet("color: #3498db; font-size: 16px; font-weight: bold;")
        self.file_display = QLabel("")
        self.file_display.setStyleSheet("color: #fff; padding: 6px; background: #34495e; border-radius: 6px;")
        self.select_btn = QPushButton("Browse File")
        self.select_btn.setStyleSheet(
            "background-color: #2980b9; color: #fff; border-radius: 8px; padding: 7px 14px; font-size: 14px;")
        self.select_btn.setFont(QFont("Segoe UI", 11))
        self.select_btn.clicked.connect(self.browse_file)

        self.pass_label = QLabel("Enter password:")
        self.pass_label.setStyleSheet("color: #3498db; font-size: 16px; font-weight: bold;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(
            "background: #34495e; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.setStyleSheet(
            "background-color: #1abc9c; color: #fff; border-radius: 8px; padding: 10px 20px; font-size: 15px; font-weight: bold;")
        self.decrypt_btn.setFont(QFont("Segoe UI", 12))
        self.decrypt_btn.clicked.connect(self.decrypt_file_action)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet("QProgressBar { background: #34495e; color: #fff; border-radius: 6px; } QProgressBar::chunk { background: #3498db; }")
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_display)
        file_layout.addWidget(self.select_btn)
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.decrypt_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addStretch()
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt")
        if file_path:
            self.file_path = file_path
            self.file_display.setText(file_path)
            self.status_label.setText("")

    def decrypt_file_action(self):
        self.status_label.setText("")
        if not self.file_path or not self.pass_input.text():
            self.status_label.setText("Please select a file and enter a password.")
            return
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted File")
        if not output_path:
            return
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        def run():
            try:
                decrypt_file(self.file_path, output_path, self.pass_input.text())
                self.status_label.setText("Decryption completed successfully!")
            except Exception as e:
                self.status_label.setText(f"Decryption failed: {str(e)}")
            finally:
                self.progress.setVisible(False)
        threading.Thread(target=run).start()

class AboutPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        about_text = QLabel(
            "<h2 style='color:#3498db'>AES-256 Encryption Tool</h2>"
            "<p style='color:#fff'>Encrypt and decrypt files securely.<br>"
            "AES-256 for strong protection.<br>"
            "Modern blue UI inspired by system preferences.<br><br>"
            "<b>How to use:</b><br>"
            "Choose 'Encrypt File' or 'Decrypt File' from the sidebar.<br>"
            "Select a file, enter a password, and proceed.</p>"
        )
        about_text.setWordWrap(True)
        about_text.setStyleSheet("font-size: 15px; color: #fff; margin: 16px;")
        layout.addWidget(about_text)
        layout.addStretch()
        self.setLayout(layout)

class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-256 Encryption Tool")
        self.resize(700, 430)
        self.setPalette(blue_palette())
        self.sidebar = Sidebar()
        self.stacked_panel = QStackedWidget()
        self.stacked_panel.addWidget(EncryptPanel())
        self.stacked_panel.addWidget(DecryptPanel())
        self.stacked_panel.addWidget(AboutPanel())
        main_layout = QHBoxLayout(self)
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)
        frame.setStyleSheet("background: #2c3e50; border-radius: 16px;")
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(0,0,0,0)
        frame_layout.addWidget(self.sidebar)
        frame_layout.addWidget(self.stacked_panel)
        main_layout.addWidget(frame)
        self.sidebar.currentRowChanged.connect(self.stacked_panel.setCurrentIndex)