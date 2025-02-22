import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class SpeedrunTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TimeTimer")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 窗口置顶
        self.setGeometry(100, 100, 400, 300)

        # 初始化变量
        self.start_time = None
        self.elapsed_time = datetime.timedelta(0)
        self.is_running = False
        self.key_bindings = {
            "start": Qt.Key_F10,  # F10
            "pause": Qt.Key_F9,   # F9
            "reset": Qt.Key_F8    # F8
        }
        self.languages = {
            "English": {
                "title": "Timer",
                "start": "Start",
                "pause": "Pause",
                "reset": "Reset",
                "key_bindings": "Key Bindings",
                "language": "Language"
            },
            "Chinese": {
                "title": "计时器",
                "start": "开始",
                "pause": "暂停",
                "reset": "清零",
                "key_bindings": "按键绑定",
                "language": "语言"
            }
        }
        self.current_language = "English"  # 默认语言设置为英文(设置为中文会有BUG)

        # 创建主窗口布局
        self.create_ui()

        # 定时器更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def create_ui(self):
        # 主窗口布局
        main_layout = QGridLayout()

        # 时间显示
        self.time_label = QLabel("00:00:00.00")
        self.time_label.setFont(QFont("Arial", 24))
        self.time_label.setAlignment(Qt.AlignCenter)

        # 按钮
        self.start_button = QPushButton(self.get_text("start"))
        self.pause_button = QPushButton(self.get_text("pause"))
        self.reset_button = QPushButton(self.get_text("reset"))

        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        # 按键绑定显示
        self.key_label = QLabel(self.get_text("key_bindings"))
        self.key_start_label = QLabel(f"Start: F10")
        self.key_pause_label = QLabel(f"Pause: F9")
        self.key_reset_label = QLabel(f"Reset: F8")

        # 语言选择
        self.language_label = QLabel(self.get_text("language"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(self.languages.keys())
        self.language_combo.currentTextChanged.connect(self.change_language)

        # 布局
        main_layout.addWidget(self.time_label, 0, 0, 1, 3)
        main_layout.addWidget(self.start_button, 1, 0)
        main_layout.addWidget(self.pause_button, 1, 1)
        main_layout.addWidget(self.reset_button, 1, 2)
        main_layout.addWidget(self.key_label, 2, 0, 1, 3)
        main_layout.addWidget(self.key_start_label, 3, 0)
        main_layout.addWidget(self.key_pause_label, 4, 0)
        main_layout.addWidget(self.key_reset_label, 5, 0)
        main_layout.addWidget(self.language_label, 6, 0)
        main_layout.addWidget(self.language_combo, 6, 1, 1, 2)

        # 设置中心窗口
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_text(self, key):
        return self.languages[self.current_language][key]

    def change_language(self, language):
        self.current_language = language
        self.time_label.setText("00:00:00.00")
        self.start_button.setText(self.get_text("start"))
        self.pause_button.setText(self.get_text("pause"))
        self.reset_button.setText(self.get_text("reset"))
        self.key_label.setText(self.get_text("key_bindings"))
        self.language_label.setText(self.get_text("language"))
        QMessageBox.information(self, "Language Changed", "Language has been changed!")

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = datetime.datetime.now() - self.start_time
            self.time_label.setText(self.format_time(self.elapsed_time))

    def format_time(self, time_delta):
        # 将时间转换为秒和微秒
        total_seconds = int(time_delta.total_seconds())
        microseconds = time_delta.microseconds

        # 计算小时、分钟、秒
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # 计算毫秒，并限制为两位数
        milliseconds = int(microseconds / 1000) % 100

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"

    def start_timer(self):
        if not self.is_running:
            self.start_time = datetime.datetime.now() - self.elapsed_time
            self.timer.start(1)  # 每秒更新一次
            self.is_running = True

    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = datetime.timedelta(0)
        self.time_label.setText("00:00:00.00")
        self.is_running = False

    def keyPressEvent(self, event):
        key = event.key()
        if key == self.key_bindings["start"]:
            self.start_timer()
        elif key == self.key_bindings["pause"]:
            self.pause_timer()
        elif key == self.key_bindings["reset"]:
            self.reset_timer()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedrunTimer()
    window.show()
    sys.exit(app.exec_())
