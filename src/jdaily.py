import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QFormLayout, QScrollArea, QListWidget, QListWidgetItem

class JDailyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jobs = []

        self.setWindowTitle("JDaily")
        self.setGeometry(100, 100, 350, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_main_widget()

    def setup_main_widget(self):
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.setup_job_list_widget()

        self.new_job_button = QPushButton("Add new job")
        self.new_job_button.clicked.connect(self.add_new_job_widget)
        self.layout.addWidget(self.new_job_button)

        self.main_widget.setLayout(self.layout)
        self.stacked_widget.addWidget(self.main_widget)

    def setup_job_list_widget(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.job_list_widget = QListWidget()
        self.scroll_area.setWidget(self.job_list_widget)

        self.layout.addWidget(self.scroll_area)

    def add_new_job_widget(self):
        new_job_widget = QWidget()
        new_job_layout = QFormLayout()

        self.setup_description_input(new_job_layout)
        self.setup_order_input(new_job_layout)
        self.setup_submit_button(new_job_layout, new_job_widget)

        new_job_widget.setLayout(new_job_layout)

        self.stacked_widget.addWidget(new_job_widget)
        self.stacked_widget.setCurrentWidget(new_job_widget)

    def setup_description_input(self, layout):
        description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        layout.addRow(description_label, self.description_input)

    def setup_order_input(self, layout):
        order_label = QLabel("Order:")
        self.order_input = QLineEdit()
        layout.addRow(order_label, self.order_input)

    def setup_submit_button(self, layout, new_job_widget):
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.return_to_main(new_job_widget))
        layout.addWidget(submit_button)

    def return_to_main(self, new_job_widget):
        job_name = self.description_input.text()
        job_order = self.order_input.text()
        self.jobs.append({"description": job_name, "order": job_order})

        job_item = QListWidgetItem(f"Description: {job_name}, Order: {job_order}")
        self.job_list_widget.addItem(job_item)
        self.stacked_widget.setCurrentWidget(self.main_widget)

def run():
    app = QApplication(sys.argv)
    window = JDailyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()