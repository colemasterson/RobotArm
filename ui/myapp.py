import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QLabel
from ServosTabContent import ServosTabContent
from MacrosTabContent import MacrosTabContent
from DiagnosticsTabContent import DiagnosticsTabContent
from BottomWidget import BottomWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        screen_geometry = self.screen().geometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setWindowTitle('Robot Arm Control')

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create tabs and add them to the tab widget
        servos_tab = ServosTabContent()
        macro_tab = MacrosTabContent()
        diagnostics_tab = DiagnosticsTabContent()

        self.tab_widget.addTab(servos_tab, 'Servos Control')
        self.tab_widget.addTab(macro_tab, 'Macro Control')
        self.tab_widget.addTab(diagnostics_tab, 'Diagnostics')

        # Specify the file names and names for each photo

        # Create widgets for the top-left and top-right sections
        self.top_left_widget = QWidget(self)
        self.top_left_layout = QVBoxLayout(self.top_left_widget)

        self.top_right_widget = QWidget(self)
        self.top_right_layout = QVBoxLayout(self.top_right_widget)

        # Create bottom widget
        bottom_widget = BottomWidget()

        # Connect the tabChanged signal to a custom slot
        self.tab_widget.currentChanged.connect(self.updateTopLeft)

        # Create a layout for the main window
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.top_left_widget)
        main_layout.addWidget(self.top_right_widget)
        main_layout.addWidget(bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Robot Arm Control')
        self.show()

    def updateTopLeft(self, index):
        # Clear the existing content in the top-left section
        self.top_left_layout.removeWidget(self.top_left_widget)
        self.top_left_widget.deleteLater()

        
        self.top_left_widget = QWidget(self)
        self.top_left_layout = QVBoxLayout(self.top_left_widget)
        #self.top_left_layout.addWidget(current_tab.getLeftContent())

        # Add the new widget to the layout
        #self.top_left_layout.addWidget(self.top_left_widget)

        self.update()

def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
