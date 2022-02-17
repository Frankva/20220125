
import mariadb
import os


import datetime  # to remove


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

    # def createLog(self, ):
    #    self.cursor.execute(f"insert into log(id, datetime) values(1, '{now}');")
    #    self.connection.commit()

    def insert_old(self, table, dict) -> None:
        '''
        depreciated
        '''

        print(
            f"insert into {table}({self.format_name_column(dict)}) values({self.format_value_column(dict)})")
        self.cursor.execute(
            f"insert into {table}({self.format_name_column(dict)}) values({self.format_value_column(dict)})")
        self.connection.commit()

    def insert(self, table_name: str, d: dict) -> None:
        '''
        execute insert sql
        '''
        sql = f"insert into {table_name}({self.format_name_column(d)}) values({self.give_quationmark(d)})"
        self.cursor.execute(sql, tuple(d.values()))
        self.connection.commit()

    @staticmethod
    def give_quationmark(d: dict) -> str:
        return (len(d) * "?, ")[0:-2]

    @staticmethod
    def format_name_column(d: dict) -> str:
        '''
        format a dictionary key in a, b, c
        '''
        txt = ""
        for i in d:
            txt += str(i) + ", "
        return txt[0:-2]

    @staticmethod
    def format_value_column(d: dict) -> str:
        '''
        format a dictionary value in a, b, c
        '''
        txt = ""
        for i in d:
            txt += str(d[i]) + ", "
        return txt[0:-2]

    @staticmethod
    def format_date_dict(d: dict, key):
        d[key] = "'" + d[key] + "'"


def test():
    model = Model()
    d = dict()
    d["id"] = 2
    d["date"] = datetime.datetime.today()
    d["inside"] = True

    model.insert("log", d)


if __name__ == "__main__":
    test()
