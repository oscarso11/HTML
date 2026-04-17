import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QScrollArea, QGroupBox,
    QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QSize


class TagAdderApp(QMainWindow):
    AVAILABLE_TAGS = ["Slowing", "Stun", "DPS", "Booster", "KnockBack", "Meta"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tag Adder")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: azure;
            }
            QGroupBox {
                color: azure;
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: azure;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
            QCheckBox {
                color: azure;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #00D7FF;
                border: 1px solid #00D7FF;
                border-radius: 3px;
            }
            QLabel {
                color: azure;
            }
        """)

        self.json_data = {}
        self.json_file_path = None
        self.tag_checkboxes = {} 

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        header_layout = QHBoxLayout()
        header_layout.addStretch()

        load_btn = QPushButton("Load JSON")
        load_btn.clicked.connect(self.load_json)
        load_btn.setMaximumWidth(150)
        header_layout.addWidget(load_btn)

        main_layout.addLayout(header_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                background-color: #0a0a0a;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #1a1a1a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #444;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666;
            }
        """)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10)
        scroll_area.setWidget(self.scroll_widget)

        main_layout.addWidget(scroll_area, 1)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()

        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_json)
        save_btn.setMaximumWidth(150)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        footer_layout.addWidget(save_btn)

        main_layout.addLayout(footer_layout)

    def load_json(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Load JSON File", "", "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                self.json_data = json.load(f)
            self.json_file_path = file_path
            self.display_units()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON: {str(e)}")

    def display_units(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        self.tag_checkboxes.clear()

        for unit_name, unit_data in self.json_data.items():
            group_box = QGroupBox(unit_name)
            group_layout = QHBoxLayout()

            existing_tags = unit_data.get("Tags", [])

            self.tag_checkboxes[unit_name] = {}
            for tag in self.AVAILABLE_TAGS:
                checkbox = QCheckBox(tag)
                checkbox.setChecked(tag in existing_tags)
                self.tag_checkboxes[unit_name][tag] = checkbox
                group_layout.addWidget(checkbox)

            group_layout.addStretch()
            group_box.setLayout(group_layout)
            self.scroll_layout.addWidget(group_box)

        self.scroll_layout.addStretch()

    def save_json(self):
        """Save the JSON file with updated tags"""
        if not self.json_file_path:
            QMessageBox.warning(self, "Warning", "No file loaded. Please load a JSON file first.")
            return

        for unit_name, tags_dict in self.tag_checkboxes.items():
            selected_tags = [tag for tag, checkbox in tags_dict.items() if checkbox.isChecked()]
            self.json_data[unit_name]["Tags"] = selected_tags

        try:
            with open(self.json_file_path, 'w') as f:
                json.dump(self.json_data, f, indent=2)
            QMessageBox.information(self, "Success", "File saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save JSON: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TagAdderApp()
    window.show()
    sys.exit(app.exec())
