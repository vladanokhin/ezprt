import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
    def keyPressEvent(self, event):
        try:
            print(chr(event.key()))
        except:
            pass

    def test_method(self):
        print('Space key pressed')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    demo = MainWindow()
    demo.show()
    demo.close()
    sys.exit(app.exec_())