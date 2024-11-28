from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QDialog, QLineEdit, QHBoxLayout,
    QFileDialog, QCalendarWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import os
import subprocess


class AppLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS Launcher - Beta 1")
        self.setGeometry(100, 100, 600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add buttons for apps
        self.add_buttons()

    def add_buttons(self):
        """Create buttons for launching separate windows."""
        browser_button = QPushButton("Launch Web Browser")
        browser_button.clicked.connect(self.launch_browser)
        self.layout.addWidget(browser_button)

        text_editor_button = QPushButton("Launch Text Editor")
        text_editor_button.clicked.connect(self.launch_text_editor)
        self.layout.addWidget(text_editor_button)

        command_prompt_button = QPushButton("Launch Command Prompt")
        command_prompt_button.clicked.connect(self.launch_command_prompt)
        self.layout.addWidget(command_prompt_button)

        file_manager_button = QPushButton("Launch File Manager")
        file_manager_button.clicked.connect(self.launch_file_manager)
        self.layout.addWidget(file_manager_button)

        calendar_button = QPushButton("Launch Calendar")
        calendar_button.clicked.connect(self.launch_calendar)
        self.layout.addWidget(calendar_button)

        settings_button = QPushButton("Launch Settings")
        settings_button.clicked.connect(self.launch_settings)
        self.layout.addWidget(settings_button)

    def launch_browser(self):
        """Open a new window with the Web Browser."""
        browser_window = WebBrowser()
        browser_window.exec_()

    def launch_text_editor(self):
        """Open a new window with the Text Editor."""
        text_editor_window = TextEditor()
        text_editor_window.exec_()

    def launch_command_prompt(self):
        """Open a new window with a basic command prompt."""
        command_prompt_window = CommandPrompt()
        command_prompt_window.exec_()

    def launch_file_manager(self):
        """Open a new window with the File Manager."""
        file_manager_window = FileManager()
        file_manager_window.exec_()

    def launch_calendar(self):
        """Open a new window with the Calendar."""
        calendar_window = Calendar()
        calendar_window.exec_()

    def launch_settings(self):
        """Open a new window with the Settings app."""
        settings_window = Settings()
        settings_window.exec_()


class WebBrowser(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - Web Browser")
        self.setGeometry(150, 150, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add browser widget and navigation controls
        self.browser = QWebEngineView()
        self.browser.setUrl("https://www.google.com")
        self.layout.addWidget(self.browser)

        nav_layout = QHBoxLayout()
        self.layout.addLayout(nav_layout)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.browser.back)
        nav_layout.addWidget(back_button)

        forward_button = QPushButton("Forward")
        forward_button.clicked.connect(self.browser.forward)
        nav_layout.addWidget(forward_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.browser.reload)
        nav_layout.addWidget(refresh_button)


class TextEditor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - Text Editor")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add text editor widget
        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)

        # Add save and open buttons
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)
        button_layout.addWidget(open_button)

        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        button_layout.addWidget(save_button)

    def open_file(self):
        """Open a file and load its contents into the text editor."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.setText(file.read())

    def save_file(self):
        """Save the contents of the text editor to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.toPlainText())


class CommandPrompt(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - Command Prompt")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add command input and output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        self.command_input = QLineEdit()
        self.command_input.returnPressed.connect(self.execute_command)
        self.layout.addWidget(self.command_input)

    def execute_command(self):
        """Execute a command and display the output."""
        command = self.command_input.text()
        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        self.output_area.append(f"> {command}\n{output}")
        self.command_input.clear()


class FileManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - File Manager")
        self.setGeometry(150, 150, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(2)
        self.file_table.setHorizontalHeaderLabels(["File Name", "Type"])
        self.layout.addWidget(self.file_table)

        self.load_files()

    def load_files(self):
        """Load files from the user's home directory into the table."""
        path = os.path.expanduser("~")
        files = os.listdir(path)
        self.file_table.setRowCount(len(files))
        for row, file_name in enumerate(files):
            self.file_table.setItem(row, 0, QTableWidgetItem(file_name))
            file_type = "Directory" if os.path.isdir(os.path.join(path, file_name)) else "File"
            self.file_table.setItem(row, 1, QTableWidgetItem(file_type))


class Calendar(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - Calendar")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.calendar = QCalendarWidget()
        self.layout.addWidget(self.calendar)


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SierraOS - Settings")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        theme_label = QLabel("Change Theme (placeholder)")
        self.layout.addWidget(theme_label)


def main():
    app = QApplication(sys.argv)
    launcher = AppLauncher()
    launcher.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
