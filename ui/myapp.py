import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QLabel, QStyleFactory
from ui.ServosTabContent import ServosTabContent
from ui.MacrosTabContent import MacrosTabContent
from ui.DiagnosticsTabContent import DiagnosticsTabContent
from ui.BottomWidget import BottomWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set the screen geometry and window title
        screen_geometry = self.screen().geometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setWindowTitle('Robot Arm Control')

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create tabs and add them to the tab widget
        servos_tab = ServosTabContent()
        macro_tab = MacrosTabContent()
        diagnostics_tab = DiagnosticsTabContent()

        # Add tabs for different pages of the application
        self.tab_widget.addTab(servos_tab, 'Servos Control')
        self.tab_widget.addTab(macro_tab, 'Macro Control')
        self.tab_widget.addTab(diagnostics_tab, 'Diagnostics')
        
        # Set styling for labels for the application
        style = """
            QLabel {
                padding: 0;
                margin: 0;
                font-family: Arial, sans-serif; /* Change the font family */
                font-size: 16px; /* Change the font size */
                font-weight: bold; /* Change the font weight */
            }
        """
        self.setStyleSheet(style)

        # Create a layout for the main window
        main_layout = QVBoxLayout()

        # Add widgets to the main layout
        main_layout.addWidget(self.tab_widget)

        # Display the application
        self.setLayout(main_layout)
        self.setWindowTitle('Robot Arm Control')
        self.show()

def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
