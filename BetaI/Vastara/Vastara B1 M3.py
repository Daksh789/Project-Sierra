from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog, QLineEdit, QTableWidget,
    QTableWidgetItem, QFileDialog, QTextEdit, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# Instructions for installing dependencies
# Ensure PyQt5 and PyQtWebEngine are installed:
# pip install PyQt5 PyQtWebEngine

# Define themes
THEMES = {
    "XP": {
        "color": "#B0C4DE", "font": "Tahoma", "browser_homepage": "https://www.bing.com",
        "button_style": "border: 1px solid black; background-color: lightblue;"
    },
    "7": {
        "color": "#4682B4", "font": "Segoe UI", "browser_homepage": "https://www.google.com",
        "button_style": "border: 1px solid gray; background-color: steelblue;"
    },
    "10": {
        "color": "#F0F0F0", "font": "Segoe UI", "browser_homepage": "https://www.microsoft.com/edge",
        "button_style": "border-radius: 5px; background-color: lightgray;"
    },
    "11": {
        "color": "#FFFFFF", "font": "Segoe UI Variable", "browser_homepage": "https://www.microsoft.com/edge",
        "button_style": "border-radius: 10px; background-color: white;"
    },
    "MacOS": {
        "color": "#EAEAEA", "font": "San Francisco", "browser_homepage": "https://www.apple.com/safari",
        "button_style": "border-radius: 12px; background-color: silver;"
    },
    "Ubuntu": {
        "color": "#E95420", "font": "Ubuntu", "browser_homepage": "https://www.mozilla.org/firefox",
        "button_style": "border: 1px solid black; background-color: orange;"
    }
}

CURRENT_THEME = "XP"  # Initial theme for testing purposes


def apply_theme(widget):
    """Apply the current theme to a given widget."""
    theme = THEMES[CURRENT_THEME]
    widget.setStyleSheet(f"background-color: {theme['color']}; font-family: {theme['font']};")


class ThemedApp(QDialog):
    """Base class for theme-adapted apps."""
    def __init__(self, title, size=(600, 400)):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(150, 150, *size)
        self.theme = THEMES.get(CURRENT_THEME, THEMES["XP"])

        # Apply theme styles
        self.setStyleSheet(f"""
            background-color: {self.theme['color']};
            font-family: {self.theme['font']};
        """)


class WebBrowser(ThemedApp):
    """Theme-adapted Web Browser."""
    def __init__(self):
        super().__init__("Web Browser", size=(800, 600))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.browser = QWebEngineView()
        self.browser.setUrl(self.theme["browser_homepage"])
        self.layout.addWidget(self.browser)

        nav_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.browser.back)
        forward_button = QPushButton("Forward")
        forward_button.clicked.connect(self.browser.forward)
        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(self.browser.reload)

        for button in [back_button, forward_button, reload_button]:
            button.setStyleSheet(self.theme["button_style"])
            nav_layout.addWidget(button)

        self.layout.addLayout(nav_layout)


class FileManager(ThemedApp):
    """Theme-adapted File Manager."""
    def __init__(self):
        super().__init__("File Manager")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(2)
        self.file_table.setHorizontalHeaderLabels(["Name", "Type"])
        self.layout.addWidget(self.file_table)

        self.load_directory(os.path.expanduser("~"))

    def load_directory(self, directory_path):
        files = os.listdir(directory_path)
        self.file_table.setRowCount(len(files))
        for row, file_name in enumerate(files):
            self.file_table.setItem(row, 0, QTableWidgetItem(file_name))
            file_type = "Directory" if os.path.isdir(os.path.join(directory_path, file_name)) else "File"
            self.file_table.setItem(row, 1, QTableWidgetItem(file_type))


class OfficeSuite(ThemedApp):
    """Theme-adapted Office Suite."""
    def __init__(self):
        super().__init__("Office Suite")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        word_processor_button = QPushButton("Word Processor")
        word_processor_button.clicked.connect(self.launch_word_processor)
        self.layout.addWidget(word_processor_button)

        spreadsheet_button = QPushButton("Spreadsheet")
        spreadsheet_button.clicked.connect(self.launch_spreadsheet)
        self.layout.addWidget(spreadsheet_button)

        presentation_tool_button = QPushButton("Presentation Tool")
        presentation_tool_button.clicked.connect(self.launch_presentation_tool)
        self.layout.addWidget(presentation_tool_button)

    def launch_word_processor(self):
        WordProcessor().exec_()

    def launch_spreadsheet(self):
        Spreadsheet().exec_()

    def launch_presentation_tool(self):
        PresentationTool().exec_()


class WordProcessor(ThemedApp):
    """Theme-adapted Word Processor."""
    def __init__(self):
        super().__init__("Word Processor")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)


class Spreadsheet(ThemedApp):
    """Theme-adapted Spreadsheet."""
    def __init__(self):
        super().__init__("Spreadsheet")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget(10, 5)
        self.layout.addWidget(self.table)


class PresentationTool(ThemedApp):
    """Theme-adapted Presentation Tool."""
    def __init__(self):
        super().__init__("Presentation Tool")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Presentation Tool Placeholder"))


class Launcher(QMainWindow):
    """Launcher for SierraOS."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS Launcher")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.add_buttons()

    def add_buttons(self):
        apps = [
            ("Web Browser", WebBrowser),
            ("File Manager", FileManager),
            ("Office Suite", OfficeSuite),
        ]

        for name, app_class in apps:
            button = QPushButton(name)
            button.clicked.connect(lambda _, app=app_class: app().exec_())
            button.setStyleSheet(THEMES[CURRENT_THEME]["button_style"])
            self.layout.addWidget(button)


def main():
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
