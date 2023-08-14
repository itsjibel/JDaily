import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QScrollArea, QListWidget, QListWidgetItem

class JDailyWindow(QMainWindow):
    def __init__(self):
        self.jobs = []
        super().__init__()

        self.setWindowTitle("JDaily")
        self.setGeometry(100, 100, 400, 300)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.job_list_widget = QListWidget()
        self.scroll_area.setWidget(self.job_list_widget)
        self.layout.addWidget(self.scroll_area)

        self.new_job_button = QPushButton("Add new job")
        self.layout.addWidget(self.new_job_button)

        self.new_job_button.clicked.connect(self.add_new_job_widget)

        self.main_widget.setLayout(self.layout)

        self.stacked_widget.addWidget(self.main_widget)

    def add_new_job_widget(self):
        new_job_widget = QWidget()
        new_job_layout = QVBoxLayout()

        description_label = QLabel("Description:")
        new_job_layout.addWidget(description_label)

        self.description_input = QLineEdit()
        new_job_layout.addWidget(self.description_input)

        new_job_layout.addStretch(1)

        order_label = QLabel("Order:")
        new_job_layout.addWidget(order_label)

        self.order_input = QLineEdit()
        new_job_layout.addWidget(self.order_input)

        new_job_layout.addStretch(7)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.return_to_main)
        new_job_layout.addWidget(submit_button)

        new_job_widget.setLayout(new_job_layout)

        self.stacked_widget.addWidget(new_job_widget)
        self.stacked_widget.setCurrentWidget(new_job_widget)

    def return_to_main(self):
        job_name = self.description_input.text()
        job_order = self.order_input.text()
        self.jobs.append({"description": job_name, "order": job_order})

        job_item = QListWidgetItem(f"Description: {job_name}, Order: {job_order}")
        self.job_list_widget.addItem(job_item)

        self.stacked_widget.setCurrentWidget(self.main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JDailyWindow()
    window.show()
    sys.exit(app.exec_())