import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QDialog
from ui.CameraManager import CameraManager
from ui.ServosTabContent import ServosTabContent
from ui.MacrosTabContent import MacrosTabContent
from ui.DiagnosticsTabContent import DiagnosticsTabContent
from ui.CameraSelectionDialog import   CameraSelectionDialog

from arm_control.interfaces.arm_interface import ArmInterface

class MyApp(QMainWindow):  # Inherit from QMainWindow
    def __init__(self):
        super().__init__()
        self.camera_manager = CameraManager()  # Set the camera_manager attribute here
        #self.camera_manager.reset()  # Now safe to call reset
        self.initUI()
       

    def initUI(self):
        
        # Initialize CameraManager
        
        #self.camera_manager.reset()
        # Create a central widget and layout for the QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tabs
        self.tab_widget = QTabWidget()
        servos_tab = ServosTabContent(ArmInterface(), self.camera_manager)  # Assuming ArmInterface() is initialized correctly
        macro_tab = MacrosTabContent(self.camera_manager)
        diagnostics_tab = DiagnosticsTabContent(self.camera_manager)

        # Add tabs
        self.tab_widget.addTab(servos_tab, 'Servos Control')
        self.tab_widget.addTab(macro_tab, 'Macro Control')
        self.tab_widget.addTab(diagnostics_tab, 'Diagnostics')
        
        # Add the tab widget to the main layout
        main_layout.addWidget(self.tab_widget)

        # Set the window title
        self.setWindowTitle('Robot Arm Control')

    def closeEvent(self, event):
        # Clean up camera resources
        self.camera_manager.release()
        super(MyApp, self).closeEvent(event)  # Corrected super call

def main():
    app = QApplication(sys.argv)
    
    camera_selection_dialog = CameraSelectionDialog()
    if camera_selection_dialog.exec_() == QDialog.Accepted:
        mainWindow = MyApp()
        mainWindow.show()
    else:
        sys.exit()  # Exit the application if the dialog is closed without confirmation

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
