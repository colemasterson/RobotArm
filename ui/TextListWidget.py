import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem

class TextListWidget(QWidget):
    def __init__(self, text_list):
        super(TextListWidget, self).__init__()

        self.setWindowTitle('Text List Widget')
        self.setGeometry(100, 100, 400, 300)

        # Create a QListWidget
        self.list_widget = QListWidget(self)

        # Populate the QListWidget with items from the text list
        for text in text_list:
            item = QListWidgetItem(text)
            self.list_widget.addItem(item)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Example list of text
    example_text_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

    widget = TextListWidget(example_text_list)
    widget.show()

    sys.exit(app.exec_())
