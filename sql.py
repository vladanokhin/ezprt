import pymysql
from pymysql.cursors import DictCursor


class Sql():

    def __init__(self, host, user, password, db_name):
        try:
            self.__connection = pymysql.connect(
                host = host, 
                user = user, #'admin',
                password = password, #'Lbvrf2011!!',
                db = db_name, #'photoshop_tool',
                charset='utf8mb4',
                autocommit=True,
                cursorclass=DictCursor
            )

            self.__cursor = self.__connection.cursor()
            self.__status_connection = True
        except:
           self.__cursor = None
           self.__status_connection = False
    
    def __del__(self):
        # Если есть подключения, то  закрываем его
        if self.__status_connection:
            self.__connection.close()

    # Гетер статуса подключения
    def getStatusConnection(self):
        return self.__status_connection 

    # Сетер для статуса подключения
    def setStatusConnection(self, status):
        if status == True or status == False:
            self.__status_connection = status
        else:
            return False
    # Метод для отправки запросов
    def query(self, query):

        if len(query) < 5:
            return {'error': 'query is not correct'}
        else:
            if self.getStatusConnection():
                try: self.__cursor.execute(query=query)
                except Exception as e: return {'error': str(e)}
                
                return self.__cursor.fetchall() # Попробрувати fetchall() 
    
    # ПРОТЕСТИРУВАТИ!!!
    def checkConnection(self):
        ress = self.__connection.open()
        try: print(ress)
        except Exception as e: print(str(e))