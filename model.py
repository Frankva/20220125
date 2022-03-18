
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
            f"""insert into {table}({self.format_name_column(dict)}) values({
                self.format_value_column(dict)})""")
        self.cursor.execute(
            f"""insert into {table}({self.format_name_column(dict)}) values({
                self.format_value_column(dict)})""")
        self.connection.commit()

    def insert(self, table_name: str, d: dict) -> None:
        '''
        execute insert sql
        '''
        sql = f"""insert into {table_name}({self.format_name_column(d)
            }) values({self.give_quationmark(d)})"""
        self.cursor.execute(sql, tuple(d.values()))
        self.connection.commit()

    def read_name_log(self, pipe: dict) -> None:
        id_user = self.select_one(
            'id_user', 'badge', 'id_badge', (pipe['id_badge'], ))
        if id_user is not None:
            pipe['name'], pipe['surname'] = self.select(
                ('name', 'surname'), 'user', 'id_user', (id_user, ))
            clog = self.select_log(('date', 'inside'), 'log',
                                'id_badge', (pipe['id_badge'], ), 'date', 5)
            pipe['log'] = self.cursor_to_dict_in_list(('date', 'inside'), clog)
            self.read_work_time(pipe)

    def read_work_time(self, pipe: dict) -> None:
        old_monday = self.find_last_monday(datetime.date.today(), 1)
        log2week = self.select_log_date(('date', 'inside'), 'log',
                                        'id_badge', (pipe['id_badge'],
                                                        old_monday), 'date')
        l_log2week = self.cursor_to_list(log2week)
        last_week, current_week = self.isolate_week(l_log2week)
        pipe['time_last_week'] = self.calcul_work_time(last_week)
        pipe['time_current_week'] = self.calcul_work_time(current_week)
    





    def select_one(self, select_name, table_name: str, where_name: str, 
                   value: tuple):
        #sql = f"select id_user from badge where id_badge=483985410385;"
        sql = f"select {select_name} from {table_name} where {where_name}=?;"
        self.cursor.execute(sql, value)
        try:
            return self.cursor.next()[0]
        except TypeError:
            return self.cursor.next()

    def select(self, select_name: tuple, table_name: str, where_name: str, 
               value: tuple) -> tuple:
        sql = f"""select {self.format_tuple(select_name)} from {table_name
            } where {where_name}=?;"""
        self.cursor.execute(sql, value)
        return self.cursor_to_tuple(self.cursor)

    def select_log(self, select_name: tuple, table_name: str, where_name: str,
                   value: tuple, order: str, limit: int):
        sql = f"""select {self.format_tuple(select_name)} from {table_name
            } where {where_name}=? order by {order} desc limit {limit}"""
        self.cursor.execute(sql, value)
        return self.cursor

    def select_log_date(self, select_name: tuple, table_name: str,
                        where_name: str, value: tuple, order: str):
        sql = f"""select {self.format_tuple(select_name)} from {table_name
            } where {where_name}=? and date >=? order by {order} desc"""
        self.cursor.execute(sql, value)
        return self.cursor

    @staticmethod
    def cursor_to_dict_in_list(select_name: tuple,
                               cursor: mariadb.connection.cursor) -> list:
        l = list()
        for t in cursor:
            l.append(dict(zip(select_name, t)))
        return l

    @staticmethod
    def cursor_to_tuple(cursor: mariadb.connection.cursor) -> tuple:
        l = list()
        for i in cursor:
            for j in i:
                l.append(j)
        return tuple(l)

    @staticmethod
    def cursor_to_list(cursor: mariadb.connection.cursor) -> list:
        l = list()
        for i in cursor:
            l.append(i)
        return l

    @staticmethod
    def format_tuple(t: tuple) -> str:
        txt = ""
        for i in t:
            txt += str(i) + ", "
        return txt[0:-2]

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


    @staticmethod
    def calcul_work_time(logs: tuple):
        print('calcul_work_time')
        time = datetime.timedelta()
        date_in = None
        for log in logs[::-1]:
            if bool(log[1]):
                if date_in is None:
                    date_in = log[0]
            elif date_in is not None:
                if date_in.day == log[0].day: # ignore time with forgeting 
                    # outlog in the end of last day
                    time += log[0] - date_in
                date_in = None
        return time
    
    @classmethod
    def isolate_week(cls, logs: list)-> tuple:
        print('isolate_week')
        current_week = list()
        last_week = list()
        last_monday = cls.find_last_monday(datetime.date.today())

        for log in logs:
            if cls.find_last_monday(log[0]) == last_monday:
                current_week.append(log)
            else:
                last_week.append(log)
        return last_week, current_week

    @staticmethod
    def find_last_monday(date, n=0) -> datetime.date:
        print('find_last_monday', date)
        try:
            return date.date() - datetime.timedelta(date.weekday() + 7*n)
        except:
            return date - datetime.timedelta(date.weekday() + 7*n)



def test():
    model = Model()
    d = dict()
    d["id"] = 2
    d["date"] = datetime.datetime.today()
    d["inside"] = True

    model.insert("log", d)


def testselect():
    model = Model()
    #f"select id_user from badge where id_badge=483985410385;"

    txt = model.select_one("id_user", "badge", "id_badge", (483985410385, ))
    print(txt)
    txt2 = model.select(("name", "surname"), "user", "id_user", (1,))
    print(txt2)
    txt3 = model.select_log(("date", "inside"), "log",
                            "id_badge", (483985410385,), "date", 10)
    txt4 = model.cursor_to_dict_in_list(("date", "inside"), txt3)
    print(txt4)


def text2():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    model.read_name_log(d)
    print(d)

def text3():
    model = Model()
    d = dict()
    d['id_badge'] = 283985410380
    model.read_name_log(d)
    print(d)

def text4():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    today = datetime.date.today()
    day_old_monday = model.find_last_monday(today, 1)
    print('day_old_monday', day_old_monday)
    log = model.select_log_date(('date', 'inside'), 'log', 'id_badge',
                                (d['id_badge'], day_old_monday), 'date', )
    l = list()
    for i in log:
        l.append(i)
    last_week, current_week = model.isolate_week(l)
    print(model.calcul_work_time(last_week))
    print(model.calcul_work_time(current_week))

def text5():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    model.read_work_time(d)
    print(d)

if __name__ == "__main__":
    text5()
