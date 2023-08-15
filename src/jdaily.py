import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QFormLayout, QScrollArea, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout, QSizePolicy, QFileDialog, QAction, QToolBar, QMessageBox

class JDailyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jobs = []

        self.setWindowTitle("JDaily")
        self.setGeometry(100, 100, 350, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_main_widget()

        self.setup_toolbar()

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_jobs)
        toolbar.addAction(new_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_jobs)
        toolbar.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_jobs)
        toolbar.addAction(load_action)

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
        submit_button.clicked.connect(lambda: self.return_to_main())
        layout.addWidget(submit_button)

    def return_to_main(self):
        job_name = self.description_input.text()
        job_order = self.order_input.text()
        
        if not job_name:
            QMessageBox.critical(self, "Error", "Job description cannot be empty.")
            return

        if not job_order:
            job_order = str(len(self.jobs) + 1)

        self.jobs.append({"description": job_name, "order": job_order})

        self.sort_jobs_by_order()
        self.update_job_list_widget()

        self.stacked_widget.setCurrentWidget(self.main_widget)

    def sort_jobs_by_order(self):
        self.jobs.sort(key=lambda x: int(x["order"]))

    def update_job_list_widget(self):
        self.job_list_widget.clear()
        for job in self.jobs:
            description = job["description"]
            order = job["order"]
            item_text = f"{order}. {description}"
            job_item = QListWidgetItem()
            check_box = QCheckBox(item_text)
            layout = QHBoxLayout()
            layout.addWidget(check_box)
            widget = QWidget()
            widget.setLayout(layout)
            job_item.setSizeHint(widget.sizeHint())
            self.job_list_widget.addItem(job_item)
            self.job_list_widget.setItemWidget(job_item, widget)

            if job.get("checked", False):
                check_box.setChecked(True)

            check_box.stateChanged.connect(self.on_checkbox_changed)

    def on_checkbox_changed(self, state):
        sender = self.sender()
        for job in self.jobs:
            widget = self.job_list_widget.itemWidget(self.job_list_widget.item(self.jobs.index(job)))
            checkbox = widget.findChild(QCheckBox)
            if sender == checkbox:
                job["checked"] = state == Qt.Checked

    def new_jobs(self):
        self.jobs.clear()
        self.update_job_list_widget()

    def save_jobs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Jobs", "", "JDaily Files (*.jdaily)")
        if file_path:
            self.save_jobs_to_file(file_path)
            QMessageBox.information(self, "Save Jobs", "Jobs have been saved.")

    def load_jobs(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Jobs", "", "JDaily Files (*.jdaily)")
        if file_path:
            jobs = self.load_jobs_from_file(file_path)
            self.jobs.clear()
            self.jobs.extend(jobs)
            self.update_job_list_widget()
            QMessageBox.information(self, "Load Jobs", "Jobs have been loaded.")

    def save_jobs_to_file(self, file_path):
        with open(file_path, "w") as file:
            json.dump(self.jobs, file)

    def load_jobs_from_file(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

def run():
    app = QApplication(sys.argv)
    window = JDailyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()