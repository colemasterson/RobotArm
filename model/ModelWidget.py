import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from model.OpenGLWidget import OpenGLWidget  # Make sure this is accessible

class ModelWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyOpenGL Integration with PyQt5')
        self.setGeometry(100, 100, 800, 600)  # Position and size of the window

        # Initialize our OpenGLWidget and set it as the central widget
        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)
        
            # app = QApplication(sys.argv)
        window = OpenGLWidget()
        window.show()
        # sys.exit(app.exec_())

# def main():

# if __name__ == "__main__":
#     main()
