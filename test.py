import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt
import pytimeparse
import datetime 
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
    # app = QApplication(sys.argv)
    t = '01:05:23'
    t = datetime.datetime.strptime(t, '%H:%M:%S')
    sec = ((t.hour * 60) + t.minute) * 60 + t.second
    print(datetime.timedelta(seconds=sec))

    # s = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    # print(datetime.timedelta(seconds=s.seconds))
    
    # demo = MainWindow()
    # demo.show()
    # demo.close()
    # sys.exit(app.exec_())