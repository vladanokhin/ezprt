from PyQt5 import QtGui
import sql
from string import punctuation
from PyQt5.QtWidgets import QMessageBox

class Error(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("i.ico"))
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        
    def showMessage(self,text, title='Ошибка!'):
        self.setWindowTitle(title)
        self.setText(text)
        self.exec_()



class Mindy(sql.Sql):
    
    logined = False # Статус, залогинен ли юзер
    id_adder = None # Id эдера

    def __init__(self, mainwindow):
        super().__init__(
            'ps-tool.mindysupport.com', 
            'admin', 
            'Lbvrf2011!!', 
            'photoshop_tool')

        self.window = mainwindow
        self.stoplist = ''.join([p for p in punctuation if p != '.'])
        self.error = Error()

    def loginIn(self, login):
        login = str(login)
        
        login = ''.join([k.strip() for k in login if k not in self.stoplist]) # Убираем все лишние символы
        self.window.inputLogin.setText(login) # Вставляем правильный логин в виджет инпута
        self.login = login
        if len(login) < 3:
            self.error.showMessage(f'Не вернный ввод.\nЛоигн должен быть больше 3 символов и не содержать символов: {self.stoplist}', 'Не верный логин')
        else:
            q = f"SELECT list_adder_id FROM list_adder WHERE list_adder_login = '{self.login}'"
            ressult_query = self.query(q)
            if ressult_query != None and 'list_adder_id' in str(ressult_query):
                self.logined = True
                self.id_adder = ressult_query['list_adder_id']

            # list_adder_id