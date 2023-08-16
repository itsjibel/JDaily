import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QFormLayout,
                             QScrollArea, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout, QToolBar, QAction, QFileDialog, QMessageBox)

class JDailyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jobs = []
        self.current_filename = ""
        self.modified = False

        self.setWindowTitle("JDaily")
        self.setGeometry(100, 100, 350, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_main_widget()
        self.setup_toolbar()

    def setup_main_widget(self):
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.setup_job_list_widget()

        self.new_job_button = QPushButton("Add new job")
        self.new_job_button.clicked.connect(self.add_new_job_widget)
        self.layout.addWidget(self.new_job_button)

        self.main_widget.setLayout(self.layout)
        self.stacked_widget.addWidget(self.main_widget)

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_jobs)
        toolbar.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_jobs)
        toolbar.addAction(load_action)

        new_action = QAction("New", self)
        new_action.triggered.connect(self.create_new_jobs_set)
        toolbar.addAction(new_action)

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
        self.setup_back_button(new_job_layout)

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

    def setup_back_button(self, layout):
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        layout.addWidget(back_button)

    def return_to_main(self, new_job_widget):
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
        self.modified = True  # Update the modified flag

        self.stacked_widget.setCurrentWidget(self.main_widget)


    def sort_jobs_by_order(self):
        self.jobs.sort(key=lambda x: int(x["order"]))

    def update_job_list_widget(self):
        self.job_list_widget.clear()
        for index, job in enumerate(self.jobs):
            description = job["description"]
            order = job["order"]

            item_text = f"{order}. {description}"
            job_item = QListWidgetItem()

            layout = QHBoxLayout()

            # Add trash icon button
            trash_icon = QIcon("path_to_your_trash_icon.png")  # Replace with the path to your trash icon image
            trash_button = QPushButton("Remove")
            trash_button.setIcon(trash_icon)
            trash_button.setFixedSize(trash_button.sizeHint())  # Set a fixed size for the remove button
            layout.addWidget(trash_button)

            # Add checkbox
            check_box = QCheckBox(item_text)
            layout.addWidget(check_box)

            widget = QWidget()
            widget.setLayout(layout)
            job_item.setSizeHint(widget.sizeHint())

            self.job_list_widget.addItem(job_item)
            self.job_list_widget.setItemWidget(job_item, widget)

            if job.get("checked", False):
                check_box.setChecked(True)

            check_box.stateChanged.connect(self.on_checkbox_changed)

            # Connect the trash button click to delete the job
            trash_button.clicked.connect(lambda _, index=index: self.delete_job(index))

    def delete_job(self, index):
        removed_job = self.jobs.pop(index)
        self.modified = True
        self.update_order_after_removal(index)
        self.update_job_list_widget()

    def update_order_after_removal(self, removed_index):
        for index, job in enumerate(self.jobs):
            if int(job["order"]) > removed_index + 1:
                job["order"] = str(int(job["order"]) - 1)

    def on_checkbox_changed(self, state):
        sender = self.sender()
        for job in self.jobs:
            widget = self.job_list_widget.itemWidget(self.job_list_widget.item(self.jobs.index(job)))
            checkbox = widget.findChild(QCheckBox)
            if sender == checkbox:
                job["checked"] = state == Qt.Checked
                self.modified = True

    def save_jobs(self):
        if not self.current_filename:
            self.current_filename, _ = QFileDialog.getSaveFileName(self, "Save Jobs", "new_routine.jdaily", "JDaily Files (*.jdaily)")
            if not self.current_filename:
                return

        with open(self.current_filename, "w") as file:
            for job in self.jobs:
                description = job["description"]
                order = job["order"]
                checked = job.get("checked", False)
                file.write(f"{description},{order},{checked}\n")

        self.modified = False

    def load_jobs(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Jobs", "", "JDaily Files (*.jdaily)")
        if file_name:
            self.jobs.clear()
            self.job_list_widget.clear()
            with open(file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        description, order = parts[:2]
                        checked = parts[2].lower() == 'true' if len(parts) >= 3 else False
                        self.jobs.append({"description": description, "order": order, "checked": checked})

            self.update_job_list_widget()
            self.stacked_widget.setCurrentWidget(self.main_widget)

    def create_new_jobs_set(self):
        if self.modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new set?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.save_jobs()
            elif reply == QMessageBox.Cancel:
                return

        self.jobs.clear()
        self.job_list_widget.clear()
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.modified = False

    def closeEvent(self, event):
        if self.modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.save_jobs()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return

        event.accept()

def run():
    app = QApplication(sys.argv)
    window = JDailyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()