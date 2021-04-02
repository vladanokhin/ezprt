import datetime
from string import punctuation
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import sql


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
            self.error.showMessage(f'Не вернный ввод.\nЛоигн должен быть больше 3 символов и не содержать символов:\n{self.stoplist}', 'Не верный логин')
            self.window.buttonGetImages.setEnabled(False)
        else:
            q = f"SELECT list_adder_id FROM list_adder WHERE list_adder_login = '{self.login}'"
            ressult_query = self.query(q) # Отправляем запрос
            if ressult_query != None and 'list_adder_id' in str(ressult_query): # ВЫполняем проверку
                self.logined = True
                self.id_adder = ressult_query[0]['list_adder_id']
                self.window.labelAdderId.setText(f'ID: {self.id_adder}')
                self.window.buttonGetImages.setEnabled(True)
            else:
                self.window.buttonGetImages.setEnabled(False)
                self.error.showMessage(f'Не верный логин.\n{ressult_query}')

    def getListImages(self):
        if not self.logined:
            self.error.showMessage('Вы не авторизованы!')
            return False

        date = self.window.inputDate.dateTime().toString('yyyyMMdd')
        q = f"SELECT * FROM program_time WHERE pt_date = '{date}' AND pt_adder_id = '{self.id_adder}'"
        images = self.query(q)
        if len(images) > 0:
            self.window.tableImages.setRowCount(len(images))
            column = 0
            for image in images:

                image_id = image['pt_image_id']
                info_image = self.query(f'SELECT * FROM image_list WHERE image_list_id = {image_id}')
                qa  = info_image[0]['image_list_quality_control']
                image_name = info_image[0]['image_list_file_name']

                self.window.tableImages.setItem(column, 0, QTableWidgetItem(str(image['pt_image_id'])))
                self.window.tableImages.setItem(column, 1, QTableWidgetItem(str(image_name)))
                self.window.tableImages.setItem(column, 2, QTableWidgetItem(str(image['pt_pt'])))
                self.window.tableImages.setItem(column, 3, QTableWidgetItem(str(qa)))
                if image['pt_type_work_name'] == 'Redo':
                    # image_error = self.query(f'SELECT * FROM images_list_approver_error WHERE image_id = {image_id}')
                    app_id = info_image[0]['image_list_approve_id']
                    app_name = self.query(f'SELECT * FROM list_adder WHERE list_adder_id = {app_id}')
                    app_name = app_name[0]['list_adder_login']
                    self.window.tableImages.setItem(column, 4, QTableWidgetItem(str(app_name)))
                else:
                    self.window.tableImages.setItem(column, 4, QTableWidgetItem(''))

                self.window.tableImages.setItem(column, 5, QTableWidgetItem(str(image['pt_type_work_name'])))
                
                column += 1
        else:
            print(images)

    def changeData(self):
        time = self.window.inputPt.text()

        t = datetime.datetime.strptime(time, '%H:%M:%S')
        sec = ((t.hour * 60) + t.minute) * 60 + t.second
        print(datetime.timedelta(seconds=sec))
        # q = self.window.inputLogin.text()
        # try:
        #     ress = self.query(q)
        #     print(str(ress))
        # except Exception as e:
        #     print(str(e))

    def getItems(self):
        row = self.window.tableImages.currentRow()
        # column = self.window.tableImages.currentColumn()
        image_id = self.window.tableImages.item(row, 0).text()
        # image_name = self.window.tableImages.item(row, 1).text()
        pt = self.window.tableImages.item(row, 2).text()
        qa = self.window.tableImages.item(row, 3).text()
        self.window.inputQa.setValue(int(qa))
        self.window.inputPt.setText(str(pt))
        
        self.current_image_id = image_id
        self.current_pt = pt
        self.current_qa = qa
        
    

#{'pt_id': 167384, 'pt_adder_id': 52, 'pt_image_id': 43896, 'pt_pt': datetime.timedelta(seconds=838), 'pt_date': datetime.date(2021, 3, 24), 'pt_time': datetime.timedelta(seconds=34615), 'pt_comment': ' ', 'pt_type_work_id': 1, 'pt_type_work_name': 'Redo', 'pt_current_edit': 1, 'pt_redo_app': 0, 'pt_reapp': 0}
# images_list_approver_error
# rep_images_pass_fail
# rep_quality
