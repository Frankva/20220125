import mariadb
import datetime

conn_params = {}
conn_params["user"] = "root"
conn_params["password"] = ""
conn_params["host"] = "localhost"
conn_params["database"] = "timbreuse2022"

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()


now = datetime.datetime.today()
print("insert into log(id, datetime) values(2, '{now}');")
cursor.execute(f"insert into log(id, datetime) values(1, '{now}');")
connection.commit()
cursor.execute("select * from log;")


class model:
        def __init__(self) -> None:
            self.conn_params = {}
            self.conn_params["user"] = "admin"
            self.conn_params["password"] = "1806"
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "timbreuse2022"
            self.connection = mariadb.connect(**self.conn_params)
            self.cursor = self.connection.cursor()

        #def createLog(self, ):
        #    self.cursor.execute(f"insert into log(id, datetime) values(1, '{now}');")
        #    self.connection.commit()

        def insert(self, table, **dict) -> None:
            print(self.format_name_column(dict), self.format_value_column(dict))
            self.cursor.execute(f"insert into {table}({self.format_name_column(dict)}) values({self.format_value_column(dict)})")
        
        @staticmethod
        def format_name_column(**dict) -> str:
            txt = ""
            for i in dict:
                txt += i + ", "
            return txt[0:-2]

        @staticmethod    
        def format_value_column(**dict) -> str:
            txt = ""
            for i in dict:
                txt += dict[i] + ", "
            return txt[0:-2]