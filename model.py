
import mariadb
import os


import datetime

import warnings
import api_client
import sys


class Model:
    def __init__(self) -> None:
        self.conn_params = dict()
        self.api_client = api_client.APIClient()
        if os.name != "nt":

            self.conn_params["user"] = "root"
            self.conn_params["password"] = "0"
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "timbreuse2022"
        else:
            self.conn_params["user"] = "root"
            self.conn_params["password"] = "0"
            #self.conn_params["password"] = ""
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "db20221007"
            self.conn_params["port"] = 4002
            #self.conn_params["database"] = "timbreuse2022"
        try:
            self.connect()
        except mariadb.ProgrammingError as E:
            if E.errno == 1049: # Unknown database
                self.create_structure()
                self.connect()

    def create_structure(self):
        database = self.conn_params['database']
        del self.conn_params['database']
        self.connection = mariadb.connect(**self.conn_params)
        self.cursor = self.connection.cursor()
        with open('sql/createDB.sql') as sql:
            for line in sql.readlines():
                self.cursor.execute(line)
        self.conn_params['database'] = database

    # def createLog(self, ):
    #    self.cursor.execute(f"insert into log(id, datetime) values(1, '{now}');")
    #    self.connection.commit()
    def connect(self):
        self.connection = mariadb.connect(**self.conn_params)
        self.cursor = self.connection.cursor()
        print('connect', file=sys.stderr)
    
    def disconnect(self):
        self.connection.commit()
        self.connection.close()
        print('disconnect')
        

    def insert_old(self, table, dict) -> None:
        '''
        depreciated
        '''
        warnings.warn("deprecated", DeprecationWarning)
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
        self.execute_and_commit(sql, tuple(d.values()))

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
        last_week, current_week = self.select_log_2_week(pipe)
        pipe['time_last_week'] = self.calcul_work_time(last_week)
        pipe['time_current_week'] = self.calcul_work_time(current_week)
        self.read_work_time_day(pipe, last_week, current_week)

    def select_one(self, select_name:str, table_name: str, where_name: str, 
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
        if limit == 0:
            sql = f"""select {self.format_tuple(select_name)} from {table_name
                } where {where_name}=? order by {order} desc"""
        else:
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
    
    def insert_user(self, select_name:str, table_name:str, value:tuple):
        warnings.warn("deprecated", DeprecationWarning)
        sql = f'''INSERT INTO {table_name} ({self.format_tuple(select_name)
        }) VALUES (NULL, ?, ?);'''
        self.cursor.execute(sql, value)
        self.connection.commit()
    
    def call_insert_user(self, value:tuple):
        sql = 'CALL `insert_user`(?, ?);'
        self.execute_and_commit(sql, value)
    
    def select_new_user(self, value):
        sql = 'SELECT `id_user` FROM `user` WHERE name=? AND surname=? ORDER \
            BY `id_user` DESC;'
        self.cursor.execute(sql, value)
        return self.cursor.next()[0]

    def insert_badge(self, select_name:str, table_name:str, value:tuple):
        warnings.warn("deprecated", DeprecationWarning)
        sql = f'''INSERT INTO {table_name} ({self.format_tuple(select_name)
        }) VALUES (?, ?);'''
        self.execute_and_commit(sql, value)

    def call_insert_badge(self, value:tuple):
        '''
        call a stored procedure that insert badge
        '''
        sql = 'CALL `insert_badge`(?, ?);'
        self.execute_and_commit(sql, value)

    def call_insert_log(self, value:tuple):
        '''
        call a stored procedure that insert log with datetime of the database
        '''
        print('call_insert_log')
        sql = 'CALL `insert_log`(?, ?);'
        self.execute_and_commit(sql, value)
    
    def call_insert_sync_log(self, value):
        '''
        call a stored procedure that insert log in the sync_log table, 
        all fiel are need
        '''
        print('call_insert_sync_log')
        sql = 'CALL `insert_sync_log`(?, ?, ?, ?);'
        print(value)
        self.execute_and_commit(sql, value)

    def call_insert_sync_user_badge(self, data:tuple):
        '''
        call a stored procedure that insert badge in the sync_badge table, 
        >>> model = Model()
        >>> model.call_insert_sync_user_badge(tuple([49, 8, 'a', 'b']))
        test
        '''
        print('call_insert_sync_badge', file=sys.stderr)
        sql = 'CALL `insert_users_and_badges`(?, ?, ?, ?);'
        self.execute_and_commit(sql, data)

    # will be renamed in select_unsync_logs
    def call_get_unsync_log(self) -> mariadb.connection.cursor:
        '''
        select all logs in write table that is not in sync table,
        the return is like a tuple
        '''
        print('call_get_unsync_log', file=sys.stderr)
        # sql = 'CALL `get_unsync_log`;'
        sql = ('SELECT `date`, `id_badge`, `inside`'
        'FROM `log_write`'
        'WHERE (`date`, `id_badge`, `inside`)'
        'NOT IN (SELECT `date`, `id_badge`, `inside` FROM `log_sync`);')
        self.cursor.execute(sql)
        return self.cursor

    def select_unsync_badges_and_users(self) -> mariadb.connection.cursor:
        '''
        select all badge id and user's names attach to badge id
        >>> model = Model()
        >>> cursor = model.select_unsync_badges_and_users()
        >>> type(cursor)
        <class 'mariadb.connection.cursor'>
        '''
        print('select_unsync_badges_and_users', file=sys.stderr)
        sql = ('SELECT `id_badge`, `name`, `surname` '
               'FROM `badge_write` LEFT OUTER JOIN `user_write` '
               'ON `badge_write`.`id_user` = `user_write`.`id_user` '
               'WHERE `id_badge` '
               'NOT IN (SELECT `id_badge` FROM `badge_sync`);')
        self.cursor.execute(sql)
        return self.cursor
    
    def send_logs(self):
        '''
        send all logs from the local database to the remote server
        '''
        print('send_logs', file=sys.stderr)
        for log in self.call_get_unsync_log():
            print(self.api_client.send_log(*log))
        print('end invoke_send_logs', file=sys.stderr)

    def send_unsync_badges_and_users(self):
        '''
        send all badge and user from the local database to the remote server
        >>> model = Model()
        >>> ids = model.test_add_user()
        >>> model.send_unsync_badges_and_users()
        201
        '''
        print('send_unsync_badges_and_users', file=sys.stderr)
        for badge_and_names in self.select_unsync_badges_and_users():
            _, code = self.api_client.send_badge_and_user(*badge_and_names)
            print(code)

            
    def insert_and_send_logs(self, value:tuple):
        print('insert_and_send_logs')
        self.call_insert_log(value)
        self.send_logs()
    
    def get_last_log_id(self) -> int:
        print('get_last_log_id')
        sql = 'SELECT MAX(`id_log`) FROM log_sync;'
        self.cursor.execute(sql)
        return self.cursor.next()[0]

    def get_last_badge_id(self) -> int:
        '''
        get the last id badge,
        maybe better to use last id user

        >>> model = Model()
        >>> isinstance(model.get_last_badge_id(), int)
        True
        '''
        print('get_last_badge_id', file=sys.stderr)
        sql = 'SELECT COUNT(`id_badge`) FROM badge_sync;'
        self.cursor.execute(sql)
        count = self.cursor.next()[0]
        print(count, file=sys.stderr)
        sql2 = f'SELECT `id_badge` FROM badge_sync LIMIT {count-1}, 1;'
        print(sql2, file=sys.stderr)
        self.cursor.execute(sql2, count)
        tmp = self.cursor.next()[0]
        print(tmp, file=sys.stderr)
        return tmp
    
    def get_last_badge_id_via_last_user(self) -> int:
        '''
        get the last id badge,
        that is correct if the last user have the last badge
        >>> model = Model()
        >>> isinstance(model.get_last_badge_id_via_last_user(), int)
        True
        '''
        print('get_last_badge_id_via_last_user', file=sys.stderr)
        sql = ('SELECT id_badge '
        'FROM badge_sync '
        'WHERE id_user '
        'IN (SELECT MAX(`id_user`) FROM user_sync);')
        self.cursor.execute(sql)
        return self.cursor.next()[0]


    def invoke_receive_logs(self) -> None:
        '''
        receive all logs from remote server and insert in local database
        '''
        print('model.invoke_receive_logs', file=sys.stderr)
        for log in self.api_client.receive_logs(self.get_last_log_id()):
            print(log, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_log(tuple(log.values()))
        
    def invoke_receive_users_and_badges(self) -> None:
        '''
        receive all users and badges from remote server and insert in local
        database
        '''
        print('invoke_receive_users_and_badges', file=sys.stderr)
        for badge_and_user in self.api_client.receive_users_and_badges(
                self.get_last_badge_id_via_last_user()):
            print(badge_and_user, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_user_badge(badge_and_user)
            
        



    def execute_and_commit(self, sql, value:tuple):
        self.cursor.execute(sql, value)
        self.connection.commit()


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
                    # to text day on multi day with forteing the last
                    # first log of next day can bug
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
        return tuple(last_week), tuple(current_week)

    @staticmethod
    def find_last_monday(date, n=0) -> datetime.date:
        print('find_last_monday', date)
        try:
            return date.date() - datetime.timedelta(date.weekday() + 7*n)
        except:
            return date - datetime.timedelta(date.weekday() + 7*n)
    
    @staticmethod
    def is_same_day(date: datetime.date, date2: datetime.date) -> bool:
        print('is_same_day')
        return ((date.day == date2.day) and (date.month == date2.month) and
                (date.year == date2.year))
        
    @classmethod
    def isolate_day(cls, logs:list()) -> list:
        '''
        return a list with a list for each day
        '''
        logs_per_day = list()
        logs_per_day.append(list())
        for log in logs:
            if len(logs_per_day[0]) == 0:
                logs_per_day[0].append(log)
            elif cls.is_same_day(log[0], logs_per_day[-1][0][0]):
                logs_per_day[-1].append(log)
            else:
                logs_per_day.append(list())
                logs_per_day[-1].append(log)
        return tuple(logs_per_day)

    @classmethod
    def map_work_time(cls, day_logs):
        try:
            return day_logs[0][0].date(), cls.calcul_work_time(day_logs)
        except IndexError:
            return None


    def read_work_time_day(self, pipe:dict, last_week, current_week) -> None:
        '''
        add in dictionary in arg the date and sum work
        is a tuple. in each index there are a tuple with date [0] and sum time 
        work of the day [1]
        '''
        last_week = self.isolate_day(last_week)
        current_week = self.isolate_day(current_week)
        pipe['last_week'], pipe['current_week'] = last_week, current_week
        last_week = tuple(map(self.map_work_time, last_week))
        current_week = tuple(map(self.map_work_time, current_week))
        pipe['day_last_week'] = last_week
        pipe['day_current_week'] = current_week

    def select_log_2_week(self, pipe: dict) -> tuple:
        old_monday = self.find_last_monday(datetime.date.today(), 1)
        log2week = self.select_log_date(('date', 'inside'), 'log', 'id_badge',
                                        (pipe['id_badge'], old_monday), 'date')
        log2week = tuple(self.cursor_to_list(log2week))
        return self.isolate_week(log2week)

    def old__invoke_new_user(self, pipe: dict):
        warnings.warn("deprecated", DeprecationWarning)
        model = Model()
        select_name = ('id_user', 'name', 'surname')
        table_name = 'user'
        value = (pipe['name'], pipe['surname'])
        model.insert_user(select_name, table_name, value)
        id = model.select_new_user(value)
        print(id)
        select_name = ('id_badge', 'id_user')
        table_name = 'badge'
        value = (pipe['id_badge'], id)
        model.insert_badge(select_name, table_name, value)

    def invoke_new_user(self, pipe: dict):
        value = (pipe['name'], pipe['surname'])
        self.call_insert_user(value)
        id = self.select_new_user(value)
        print(id)
        value = (pipe['id_badge'], id)
        self.call_insert_badge(value)

    def test_add_user(self):
        '''
        just for unit test
        '''
        print('test_add_user', file=sys.stderr)
        value = ('test', 'test')
        self.call_insert_user(value)
        id = self.select_new_user(value)
        value = (50, id)
        self.call_insert_badge(value)
        return value

    def test_del_user(self, user_id, badge_id):
        '''
        just for unit test
        '''
        sql_user = 'DELETE FROM user_write WHERE id_user=?;'
        sql_badge = 'DELETE FROM badge_write WHERE id_badge=?;'
        self.execute_and_commit(sql_user, user_id)
        self.execute_and_commit(sql_badge, badge_id)







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


def test2():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    model.read_name_log(d)
    print(d)

def test3():
    model = Model()
    d = dict()
    d['id_badge'] = 283985410380
    model.read_name_log(d)
    print(d)

def test4():
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

def test5():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    model.read_work_time(d)
    print(d)

def test6():
    d = dict()
    d['id_badge'] = 483985410385
    model = Model()
    clog = model.select_log(('date', 'inside'), 'log',
                            'id_badge', (d['id_badge'], ), 'date', 0)

    l_log = model.cursor_to_list(clog)
    d_log = model.isolate_day(l_log)
    for day_log in d_log:
        print(model.calcul_work_time(day_log))

def test7():
    d = dict()
    d['id_badge'] = 483985410385
    model = Model()
    old_monday = model.find_last_monday(datetime.date.today(), 1)
    log2week = model.select_log_date(('date', 'inside'), 'log',
                            'id_badge', (d['id_badge'], old_monday), 'date')
    t_log2week = tuple(model.cursor_to_list(log2week))
    last_week, current_week = model.isolate_week(t_log2week)
    day_last_week = model.isolate_day(last_week)
    day_current_week = model.isolate_day(current_week)
    print(day_last_week, day_current_week, sep='\n')
    day_last_week = tuple(map(model.map_work_time, day_last_week))
    day_current_week = tuple(map(model.map_work_time, day_current_week))
    print(day_last_week, day_current_week, sep='\n')

def test8():
    model = Model()
    d = dict()
    d['id_badge'] = 483985410385
    model.read_work_time(d)
    print('test8', d)

def test9():
    model = Model()
    select_name = ('id_user', 'name', 'surname')
    table_name = 'user'
    value = ('fakename', 'fakesurname')
    model.insert_user(select_name, table_name, value)
    id = model.select_new_user(value)
    print(id)
    select_name = ('id_badge', 'id_user')
    table_name = 'badge'
    value = (888888888888, id)
    model.insert_badge(select_name, table_name, value)

def test10():
    d = dict()
    d['name'] = 'test'
    d['surname'] = 'man'
    d['id_badge'] = 483985410415
    model = Model()
    model.invoke_new_user(d)

def test11():
    conn_params = dict()
    conn_params["user"] = "root"
    conn_params["password"] = ""
    conn_params["host"] = "localhost"
#    conn_params["database"] = "timbreuse2022"
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    with open('sql/createDB.sql') as sql:
        for line in sql.readlines():
            cursor.execute(line)

def test12():
    conn_params = dict()
    conn_params["user"] = "root"
    conn_params["password"] = ""
    conn_params["host"] = "localhost"
    conn_params["database"] = "aaatimbreuse2022"
    try:
        connection = mariadb.connect(**conn_params)
    except mariadb.ProgrammingError as E:
        if E.errno == 1049: # Unknown database
            print('a')

def test13():    
    model = Model()
    model.invoke_receive_logs()


def doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    #test13()
    doctest()
