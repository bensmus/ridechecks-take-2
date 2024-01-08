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
    QComboBox,
)
from util import Day
from typing import get_args, List
from PySide6.QtCore import Signal

# Standard
app = QApplication([])

# TODO Add comments and fix atrocious variable names, use Dropdown class


class SingleElementWidget(QWidget):
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


class Dropdown(QWidget):
    def __init__(self, parent, elem_name: str, elems: List[str]):
        super().__init__(parent)

        label = QLabel(self)
        label.setText(f"{elem_name.capitalize()}...")
        self.combo_box = QComboBox(self)
        for elem in elems:
            self.add_elem(elem)
        
        layout = QVBoxLayout(self)
        layout.add(label)
        layout.add(self.combo_box)
        
    def remove_elem(self, elem: str) -> None:
        for i in range(self.combo_box.count()):
            if elem == self.combo_box.itemText(i):
                self.combo_box.removeItem(i)
                break

    def add_elem(self, elem: str) -> None:
        self.combo_box.addItem(elem)
    
    def current_elem(self) -> str:
        return self.combo_box.currentText()
    
    def is_empty(self) -> bool:
        return self.combo_box.currentIndex() < 0
    

class ElementSelectorWidget(QWidget):
    """
    Given a set of all elements, this widgets allows the selection
    of a subset of those elements.

    For example, a set of rides is given. Using this widget, it is 
    possible to select a subset of those rides to be unavailable.

    Consists of: 
    - Dropdown selector
    - Add element button
    - List view of selected elements 
    """
    def __init__(self, parent, elem_name, selected_elems, all_elems):
        super().__init__(parent)

        self.task_widgets = []

        dropdown_label = QLabel(self)
        dropdown_label.setText(f"{elem_name.capitalize()}...")
        dropdown = QComboBox(self)
        for elem in all_elems:
            dropdown.addItem(elem)

        task_add_button = QPushButton(self)  # Submit the task

        task_add_button.setText(f"Add {elem_name}")

        task_holder = QWidget(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True) # This is critical, otherwise no tasks can be added.
        scroll_area.setWidget(task_holder)

        layout = QVBoxLayout(self)  # `self` argument is critical
        layout.addWidget(dropdown_label)
        layout.addWidget(dropdown)
        layout.addWidget(task_add_button)
        layout.addWidget(scroll_area)  # QScrollArea is a widget

        task_layout = QVBoxLayout(task_holder)
        task_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        def add_task(task_text):
            # Ensure that we cannot add the task again: remove it from dropdown
            for i in range(dropdown.count()):
                text = dropdown.itemText(i)
                if text == task_text:
                    dropdown.removeItem(i)
            task_widget = SingleElementWidget(self, task_text)
            self.task_widgets.append(task_widget)
            task_layout.addWidget(task_widget)

            def delete_task():
                self.task_widgets.remove(task_widget)
                current = task_widget.read_task()
                dropdown.addItem(current)
                task_widget.deleteLater()

            task_widget.task_deleted.connect(delete_task)
        
        def add_task_from_dropdown():
            if dropdown.currentIndex() >= 0: # If there is a task to add:
                current = dropdown.currentText()
                add_task(current)

        task_add_button.clicked.connect(add_task_from_dropdown)

        for selected_elem in selected_elems:
            add_task(selected_elem)

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
    def __init__(self, parent, day_data, rides, workers):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.time_edit_widget = TimeEditWidget(self, day_data["time"])
        self.closed_rides_widget = ElementSelectorWidget(
            self, "closed ride", day_data["uarides"], rides
        )
        self.absent_workers_widget = ElementSelectorWidget(
            self, "absent worker", day_data["uaworkers"], workers
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
    def __init__(self, parent, days_data, rides, workers):
        super().__init__(parent)
        self.day_widgets = {}
        tab_widget = QTabWidget(self)
        for day in get_args(Day):
            day_widget = DayWidget(self, days_data[day], rides, workers)
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
            days_info = yaml.safe_load(f)
        with open("input/rides_time.yaml", "r") as f:
            rides_time = yaml.safe_load(f)
        with open("input/workers_cannot_check.yaml", "r") as f:
            workers_time = yaml.safe_load(f)
        rides = list(rides_time.keys())
        workers = list(workers_time.keys())
        self.days_widget = DaysWidget(self, days_info, rides, workers)
        self.setCentralWidget(self.days_widget)
        self.setGeometry(400, 400, 400, 600) # Increase default size and default position on desktop.

    def closeEvent(self, event):
        with open("input/days_info.yaml", "w") as f:
            yaml.safe_dump(self.days_widget.read_days(), f, sort_keys=False)


window = yamlLoadDump()
window.show()
app.exec()
