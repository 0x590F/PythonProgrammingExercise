import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.run_program)
        layout.addWidget(start_button)

        self.setLayout(layout)
        self.setWindowTitle('GRM Tools')
        self.show()

    def run_program(self):
        current_dir = os.path.dirname(os.path.abspath(sys.executable))
        main_script_path = os.path.join(current_dir, 'grmtools-main', 'grmtools', 'console_scripts', 'pipeline', 'main.py')
        conf_file_path = os.path.join(current_dir, 'grmtools-main', 'grmtools', 'console_scripts', 'pipeline', 'conf.json')

        if os.path.exists(main_script_path) and os.path.exists(conf_file_path):
            command = f'python "{main_script_path}" "{conf_file_path}"'
            os.system(command)
        else:
            QMessageBox.warning(self, 'Error', 'Unable to locate main.py or conf.json file.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())

