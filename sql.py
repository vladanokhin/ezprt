import pymysql
from pymysql.cursors import DictCursor


class Sql():

    __cursor = None
    __status_connection = False

    def __init__(self, host, user, password, db_name):
        try:
            connection = pymysql.connect(
                host = host, #'ps-tool.mindysupport.com',
                user = user, #'admin',
                password = password, #'Lbvrf2011!!',
                db = db_name, #'photoshop_tool',
                charset='utf8mb4',
                autocommit=True,
                cursorclass=DictCursor
            )

            self.__cursor = connection.cursor()
            self.__status_connection = True

        except:
           self.__cursor = None
           self.__status_connection = False
    
    def execute(self, command=None):
        if len(command) < 3 or command == None:
            # QMassegeBox(error)
            return False
        
    
    def getStatusConnection(self):
        return self.__status_connection
    
    def setStatusConnection(self, status):
        if status == True or status == False:
            self.__status_connection = status
        else:
            # QMassegeBox(error)
            return False
        