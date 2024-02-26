import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ModelWidget import OpenGLWidget  # Make sure this is accessible

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyOpenGL Integration with PyQt5')
        self.setGeometry(100, 100, 800, 600)  # Position and size of the window

        # Initialize our OpenGLWidget and set it as the central widget
        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
