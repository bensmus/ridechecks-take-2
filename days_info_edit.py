# GUI for editing days_info.yaml.

import yaml
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QWidget,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QMainWindow,
)

from PySide6.QtCore import Signal

# Standard
app = QApplication([])


class SingleTaskWidget(QWidget):
    """
    Consists of button for deleting task and
    label describing task.
    """

    task_deleted = Signal(bool)

    def __init__(self, parent, task_text):
        super().__init__(parent)

        task_delete_button = QPushButton(self)
        task_delete_button.setText("-")
        task_delete_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )  # Makes the button small.
        task_delete_button.clicked.connect(lambda: self.task_deleted.emit(True))
        self.task_label = QLabel(self)
        self.task_label.setText(task_text)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove spacing
        layout.addWidget(task_delete_button)
        layout.addWidget(self.task_label)

    def read_task(self):
        return self.task_label.text()


class AllTasksWidget(QWidget):
    def __init__(self, parent, elem_name, elems):
        super().__init__(parent)

        self.task_widgets = []

        task_input = QLineEdit(self)  # Enter the task here
        task_input.setPlaceholderText(f"{elem_name.capitalize()}...")
        task_add_button = QPushButton(self)  # Submit the task

        task_add_button.setText(f"Add {elem_name}")

        task_holder = QWidget(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True) # This is critical, otherwise no tasks can be added.
        scroll_area.setWidget(task_holder)

        layout = QVBoxLayout(self)  # `self` argument is critical
        layout.addWidget(task_input)
        layout.addWidget(task_add_button)
        layout.addWidget(scroll_area)  # QScrollArea is a widget

        task_layout = QVBoxLayout(task_holder)
        task_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        def add_task(task_text):
            task_widget = SingleTaskWidget(self, task_text)
            self.task_widgets.append(task_widget)
            task_layout.addWidget(task_widget)

            def delete_task():
                self.task_widgets.remove(task_widget)
                task_widget.deleteLater()

            task_widget.task_deleted.connect(delete_task)
        
        def add_task_from_input():
            task_input_text = task_input.text()
            if task_input_text != "":  # Do not do anything if no text is entered.
                add_task(task_input_text)
                task_input.clear()  # Clear text

        task_add_button.clicked.connect(add_task_from_input)

        for elem in elems:
            add_task(elem)

    def read_tasks(self):
        return [task_widget.read_task() for task_widget in self.task_widgets]


class TimeEditWidget(QWidget):
    def __init__(self, parent, time):
        super().__init__(parent)

        self.time = time

        layout = QVBoxLayout(self)
        time_edit_widget = QLineEdit(self)
        time_edit_widget.setPlaceholderText("Time...")
        time_view_widget = QLabel(self)

        layout.addWidget(time_edit_widget)
        layout.addWidget(time_view_widget)

        def update_time_view_widget():
            time_view_widget.setText(f"Time: {self.time // 60}h{self.time % 60}m")

        update_time_view_widget()

        def set_time(to):
            try:
                self.time = int(to)
                update_time_view_widget()
            except ValueError:
                pass

        time_edit_widget.textEdited.connect(set_time)

    def read_time(self):
        return self.time


class DayWidget(QWidget):
    def __init__(self, parent, day_data):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.time_edit_widget = TimeEditWidget(self, day_data["time"])
        self.closed_rides_widget = AllTasksWidget(
            self, "closed ride", day_data["uarides"]
        )
        self.absent_workers_widget = AllTasksWidget(
            self, "absent worker", day_data["uaworkers"]
        )

        layout.addWidget(self.time_edit_widget)
        layout.addWidget(self.closed_rides_widget)
        layout.addWidget(self.absent_workers_widget)

    def read_day(self):
        return {
            "time": self.time_edit_widget.read_time(),
            "uaworkers": self.absent_workers_widget.read_tasks(),
            "uarides": self.closed_rides_widget.read_tasks(),
        }


class DaysWidget(QWidget):
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    def __init__(self, parent, days_data):
        super().__init__(parent)
        self.day_widgets = {}
        tab_widget = QTabWidget(self)
        for day in DaysWidget.days_of_week:
            day_widget = DayWidget(self, days_data[day])
            self.day_widgets[day] = day_widget
            tab_widget.addTab(day_widget, day.capitalize())
        layout = QVBoxLayout(self)  # Could have been QHBoxLayout, it doesn't matter.
        layout.addWidget(tab_widget)

    def read_days(self):
        return {
            day: self.day_widgets[day].read_day() for day in self.day_widgets
        }


class yamlLoadDump(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load YAML and use it to init DaysWidget
        with open("input/days_info.yaml", "r") as f:
            days_data = yaml.safe_load(f)
        self.days_widget = DaysWidget(self, days_data)
        self.setCentralWidget(self.days_widget)

    def closeEvent(self, event):
        with open("input/days_info.yaml", "w") as f:
            yaml.safe_dump(self.days_widget.read_days(), f)


window = yamlLoadDump()
window.show()
app.exec()
