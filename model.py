import mariadb
import os

class Model:
    def __init__(self) -> None:
        self.conn_params = dict()
        if os.name != "nt":
           
            self.conn_params["user"] = "admin"
            self.conn_params["password"] = "1806"
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "timbreuse2022"
        else:
            self.conn_params["user"] = "root"
            self.conn_params["password"] = ""
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "timbreuse2022"
        self.connection = mariadb.connect(**self.conn_params)
        self.cursor = self.connection.cursor()

    #def createLog(self, ):
    #    self.cursor.execute(f"insert into log(id, datetime) values(1, '{now}');")
    #    self.connection.commit()

    def insert(self, table, dict) -> None:
        print(f"insert into {table}({self.format_name_column(dict)}) values({self.format_value_column(dict)})")
        self.cursor.execute(f"insert into {table}({self.format_name_column(dict)}) values({self.format_value_column(dict)})")
        self.connection.commit()

    @staticmethod
    def format_name_column(dict) -> str:
        '''
        format a dictionary key in a, b, c
        '''
        txt = ""
        for i in dict:
            txt += str(i) + ", "
            txt = "'" + txt + "'"
        return txt[0:-2]

    @staticmethod    
    def format_value_column(dict) -> str:
        '''
        format a dictionary value in a, b, c
        '''
        txt = ""
        for i in dict:
            txt += str(dict[i]) + ", "
            txt = "'" + txt + "'"
        return txt[0:-2]


