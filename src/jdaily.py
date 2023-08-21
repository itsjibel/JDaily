import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QFormLayout,
    QScrollArea, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout, QToolBar, QAction, QFileDialog, QMessageBox
)

class JDailyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jobs = []
        self.current_filename = ""
        self.initial_directory = ""
        self.modified = False

        self.setWindowTitle("JDaily")
        self.setGeometry(100, 100, 350, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_ui()

    def setup_ui(self):
        self.setup_main_widget()
        self.setup_toolbar()

    def setup_main_widget(self):
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.setup_job_list_widget()
        self.setup_buttons()

        self.main_widget.setLayout(self.layout)
        self.stacked_widget.addWidget(self.main_widget)

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        actions = [
            ("Save", self.save_jobs),
            ("Save As...", self.save_jobs_as),
            ("Load", self.load_jobs),
            ("New", self.create_new_jobs_set)
        ]

        for label, function in actions:
            action = QAction(label, self)
            action.triggered.connect(function)
            toolbar.addAction(action)

    def setup_job_list_widget(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.job_list_widget = QListWidget()
        self.scroll_area.setWidget(self.job_list_widget)

        self.layout.addWidget(self.scroll_area)
        self.job_list_widget.itemSelectionChanged.connect(self.update_edit_remove_buttons)

    def setup_buttons(self):
        self.new_job_button = QPushButton("Add new job")
        self.new_job_button.clicked.connect(self.add_new_job_widget)
        self.layout.addWidget(self.new_job_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_job)
        self.layout.addWidget(self.edit_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setEnabled(False)
        self.remove_button.clicked.connect(self.remove_selected_job)
        self.layout.addWidget(self.remove_button)

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
        submit_button.clicked.connect(lambda: self.save_new_job(new_job_widget))
        layout.addWidget(submit_button)

    def setup_back_button(self, layout):
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        layout.addWidget(back_button)

    def save_new_job(self, new_job_widget):
        job_name = self.description_input.text()
        job_order = self.order_input.text()

        if not job_name:
            QMessageBox.critical(self, "Error", "Job description cannot be empty.")
            return

        if not job_order:
            job_order = str(len(self.jobs) + 1)
        else:
            try:
                new_order = int(job_order)
                if new_order < 1 or new_order > len(self.jobs) + 1:
                    QMessageBox.critical(self, "Error", "Invalid order. Order must be between 1 and the number of jobs plus 1.")
                    return
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid order. Order must be a valid integer.")
                return

            for job in self.jobs:
                if int(job["order"]) >= new_order:
                    job["order"] = str(int(job["order"]) + 1)

        self.jobs.append({"description": job_name, "order": job_order})
        self.sort_jobs_by_order()
        self.update_job_list_widget()
        self.modified = True
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def sort_jobs_by_order(self):
        self.jobs.sort(key=lambda x: int(x["order"]))

    def update_job_list_widget(self):
        self.job_list_widget.clear()
        for index, job in enumerate(self.jobs):
            item_text = f"{job['order']}. {job['description']}"
            job_item = QListWidgetItem()

            layout = QHBoxLayout()
            check_box = QCheckBox(item_text)
            layout.addWidget(check_box)

            widget = QWidget()
            widget.setLayout(layout)
            job_item.setSizeHint(widget.sizeHint())

            self.job_list_widget.addItem(job_item)
            self.job_list_widget.setItemWidget(job_item, widget)

            if job.get("checked", False):
                check_box.setChecked(True)

            check_box.stateChanged.connect(lambda state, index=index: self.on_checkbox_changed(state, index))

    def on_checkbox_changed(self, state, index):
        self.jobs[index]["checked"] = state == Qt.Checked
        self.update_edit_remove_buttons()

    def update_edit_remove_buttons(self):
        selected_items = self.job_list_widget.selectedItems()
        if selected_items:
            self.edit_button.setEnabled(True)
            self.remove_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)

    def edit_selected_job(self):
        selected_item = self.job_list_widget.selectedItems()[0]
        index = self.job_list_widget.row(selected_item)
        self.edit_job(index)

    def remove_selected_job(self):
        selected_item = self.job_list_widget.selectedItems()[0]
        index = self.job_list_widget.row(selected_item)
        self.delete_job(index)

    def edit_job(self, index):
        job = self.jobs[index]
        description = job["description"]
        order = job["order"]

        self.editing_index = index

        edit_job_widget = QWidget()
        edit_job_layout = QFormLayout()

        self.setup_description_input(edit_job_layout)
        self.setup_order_input(edit_job_layout)
        self.setup_save_button(edit_job_layout, edit_job_widget)
        self.setup_back_button(edit_job_layout)

        edit_job_widget.setLayout(edit_job_layout)

        self.description_input.setText(description)
        self.order_input.setText(order)

        self.stacked_widget.addWidget(edit_job_widget)
        self.stacked_widget.setCurrentWidget(edit_job_widget)

    def setup_save_button(self, layout, edit_job_widget):
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_edited_job(edit_job_widget))
        layout.addWidget(save_button)

    def save_edited_job(self, edit_job_widget):
        job_name = self.description_input.text()
        job_order = self.order_input.text()

        if not job_name:
            QMessageBox.critical(self, "Error", "Job description cannot be empty.")
            return

        if not job_order:
            job_order = str(len(self.jobs) + 1)
        else:
            try:
                new_order = int(job_order)
                if new_order < 1 or new_order > len(self.jobs):
                    QMessageBox.critical(self, "Error", "Invalid order. Order must be between 1 and the number of jobs.")
                    return
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid order. Order must be a valid integer.")
                return

        for index, job in enumerate(self.jobs):
            if index != self.editing_index and int(job["order"]) == new_order:
                QMessageBox.critical(self, "Error", "Another job already has the same order. Choose a different order.")
                return

        edited_job = {"description": job_name, "order": str(new_order), "checked": self.jobs[self.editing_index].get("checked", False)}
        self.jobs[self.editing_index] = edited_job

        self.sort_jobs_by_order()
        self.update_job_list_widget()
        self.modified = True

        self.stacked_widget.setCurrentWidget(self.main_widget)

    def delete_job(self, index):
        removed_job = self.jobs.pop(index)
        self.modified = True
        self.update_order_after_removal(index)
        self.update_job_list_widget()

    def update_order_after_removal(self, removed_index):
        for index, job in enumerate(self.jobs):
            if int(job["order"]) > removed_index + 1:
                job["order"] = str(int(job["order"]) - 1)

    def save_jobs(self):
        if not self.current_filename:
            self.current_filename, _ = QFileDialog.getSaveFileName(
                self, "Save Jobs", "new_routine.jdaily", "JDaily Files (*.jdaily)"
            )
            if not self.current_filename:
                return

            self.initial_directory = self.current_filename

        with open(self.current_filename, "w") as file:
            for job in self.jobs:
                description = job["description"]
                order = job["order"]
                checked = job.get("checked", False)
                file.write(f"{description},{order},{checked}\n")

        self.modified = False

    def save_jobs_as(self):
        self.current_filename, _ = QFileDialog.getSaveFileName(
            self, "Save Jobs As...", "new_routine.jdaily", "JDaily Files (*.jdaily)"
        )
        if not self.current_filename:
            return

        self.initial_directory = self.current_filename

        with open(self.current_filename, "w") as file:
            for job in self.jobs:
                description = job["description"]
                order = job["order"]
                checked = job.get("checked", False)
                file.write(f"{description},{order},{checked}\n")

        self.modified = False

    def load_jobs(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Jobs", self.initial_directory, "JDaily Files (*.jdaily)"
        )
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

            # Update initial directory after successful file loading
            self.current_filename = file_name

    def create_new_jobs_set(self):
        if self.modified or any(job.get("checked", False) for job in self.jobs):
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new set?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.save_jobs()

        self.jobs.clear()
        self.job_list_widget.clear()
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.modified = False
        self.current_filename = ""
        self.initial_directory = ""

    def closeEvent(self, event):
        if self.modified or any(job.get("checked", False) for job in self.jobs):
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