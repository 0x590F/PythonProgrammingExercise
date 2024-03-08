import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import win32gui
import win32con

# 获取命令行窗口句柄
hwnd = win32gui.GetForegroundWindow()

# 隐藏窗口
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口
        self.setWindowTitle("Start Window")
        self.setGeometry(100, 100, 400, 200)

        # 创建按钮
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.show_hello_window)

        # 创建新窗口
        self.hello_window = None

    def show_hello_window(self):
        if self.hello_window:
            # 如果 hello_window 已经存在，关闭它
            self.hello_window.close()

        # 创建新窗口
        self.hello_window = QWidget()
        self.hello_window.setWindowTitle("Hello Window")
        self.hello_window.setGeometry(200, 200, 300, 150)

        # 添加文本标签
        hello_label = QLabel("Hello, World!", self.hello_window)
        hello_label.setAlignment(Qt.AlignCenter)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(hello_label)
        self.hello_window.setLayout(layout)

        # 显示新窗口
        self.hello_window.show()

    def reset_hello_window(self):
        # 重置 hello_window
        self.hello_window = None

    def closeEvent(self, event):
        # 重写默认的关闭事件处理
        if self.hello_window:
            self.hello_window.close()
        event.accept()  # 接受关闭事件

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
