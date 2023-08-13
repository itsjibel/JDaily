import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

def window():
   app = QApplication(sys.argv)
   widget = QWidget()

   textLabel = QLabel(widget)
   textLabel.setText("Welcome to JDaily!")
   textLabel.move(95, 240)

   widget.setGeometry(50, 50, 320, 520)
   widget.setWindowTitle("JDaily")
   widget.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()