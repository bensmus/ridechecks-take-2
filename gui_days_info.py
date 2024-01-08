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


class Dropdown(QWidget):
    """
    Consists of Qlabel and QComboBox.
    For choosing from a list of unique strings.
    """
    def __init__(self, parent, elem_name: str, elems: List[str]):
        super().__init__(parent)

        label = QLabel(self)
        label.setText(f"{elem_name.capitalize()}:")
        self.combo_box = QComboBox(self)
        for elem in elems:
            self.add_elem(elem)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        layout.addWidget(self.combo_box)
        
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
    

class ChosenWidget(QWidget):
    """
    Given a set of all elements, this widgets allows the user
    to choose a subset of those elements.

    For example, a set of rides is given. Using this widget, it is 
    possible to choose some of those rides to be unavailable.

    Consists of: 
    - Dropdown
    - Add button
    - List view of chosen elements 
    """
    def __init__(self, parent, elem_name, chosen_elems, all_elems):
        super().__init__(parent)

        self.elem_widgets = []

        dropdown = Dropdown(self, elem_name, all_elems)

        add_button = QPushButton(self)  # Button to choose element.

        add_button.setText(f"Add {elem_name}")

        chosen_holder = QWidget(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True) # This is critical, otherwise no elements can be chosen.
        scroll_area.setWidget(chosen_holder)
        scroll_area.setFrameStyle(0)

        layout = QVBoxLayout(self)  # `self` argument is critical
        layout.addWidget(dropdown)
        layout.addWidget(add_button)
        layout.addWidget(scroll_area)  # QScrollArea is a widget

        chosen_layout = QVBoxLayout(chosen_holder)
        chosen_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        def add_elem(elem):
            dropdown.remove_elem(elem)
            elem_widget = ElementWidget(self, elem)
            self.elem_widgets.append(elem_widget)
            chosen_layout.addWidget(elem_widget)

            def delete_elem():
                self.elem_widgets.remove(elem_widget)
                current = elem_widget.read()
                dropdown.add_elem(current)
                elem_widget.deleteLater()

            elem_widget.element_unchoose.connect(delete_elem)
        
        def add_elem_from_dropdown():
            if dropdown.is_empty():
                return
            add_elem(dropdown.current_elem())

        add_button.clicked.connect(add_elem_from_dropdown)

        for chosen_elem in chosen_elems:
            add_elem(chosen_elem)

    def read_chosen(self):
        return [elem_widget.read() for elem_widget in self.elem_widgets]


class ElementWidget(QWidget):
    """
    Consists of QPushButton for unchoosing element and QLabel
    """
    element_unchoose = Signal(bool)

    def __init__(self, parent, text):
        super().__init__(parent)

        unchoose_button = QPushButton(self)
        unchoose_button.setText("-")
        unchoose_button.setFixedSize(30, 20)
        unchoose_button.clicked.connect(lambda: self.element_unchoose.emit(True))
        self.label = QLabel(self)
        self.label.setText(text)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove spacing
        layout.addWidget(unchoose_button)
        layout.addWidget(self.label)

    def read(self):
        return self.label.text()
    

class TimeEditWidget(QWidget):
    def __init__(self, parent, time):
        super().__init__(parent)

        self.time = time

        layout = QVBoxLayout(self)
        time_edit_widget = QLineEdit(self)
        time_edit_widget.setPlaceholderText("Time:")
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
    """
    Edit time, unavailable rides, and unavailable workers for a given day.
    """
    def __init__(self, parent, day_data, rides, workers):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.time_edit_widget = TimeEditWidget(self, day_data["time"])
        self.closed_rides_widget = ChosenWidget(
            self, "closed ride", day_data["uarides"], rides
        )
        self.absent_workers_widget = ChosenWidget(
            self, "absent worker", day_data["uaworkers"], workers
        )

        layout.addWidget(self.time_edit_widget)
        layout.addWidget(self.closed_rides_widget)
        layout.addWidget(self.absent_workers_widget)

    def read_day(self):
        return {
            "time": self.time_edit_widget.read_time(),
            "uaworkers": self.absent_workers_widget.read_chosen(),
            "uarides": self.closed_rides_widget.read_chosen(),
        }


class DaysWidget(QWidget):
    def __init__(self, parent, days_data, rides, workers):
        super().__init__(parent)
        self.day_widgets = {}
        layout = QHBoxLayout(self)
        for day in get_args(Day):
            container = QWidget(self)
            container_layout = QVBoxLayout(container)
            day_label = QLabel(container)
            day_label.setText(day.capitalize())
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_widget = DayWidget(container, days_data[day], rides, workers)
            self.day_widgets[day] = day_widget
            container_layout.addWidget(day_label)
            container_layout.addWidget(day_widget)
            layout.addWidget(container)

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
