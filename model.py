#!/usr/bin/env python
import mariadb
import os


import datetime

import warnings
import api_client
import sys


class Model:
    def __init__(self) -> None:
        self.check_with_badge_id = False
        self.conn_params = dict()
        self.api_client = api_client.APIClient()
        if os.name != "nt":

            self.conn_params["user"] = "root"
            self.conn_params["password"] = "0"
            self.conn_params["host"] = "localhost"
            self.conn_params["database"] = "timbreuse2022"
        else:
            self.conn_params["user"] = "root"
            self.conn_params["password"] = ""
            #self.conn_params["password"] = ""
            self.conn_params["host"] = "localhost"
            #self.conn_params["database"] = "db20221007"
            self.conn_params["database"] = "tmp"
            self.conn_params["port"] = 3306
            #self.conn_params["database"] = "timbreuse2022"
        try:
            self.connect()
        except mariadb.ProgrammingError as E:
            if E.errno == 1049: # Unknown database
                self.create_structure()
                self.connect()

    def create_structure(self):
        print('Model.create_structure', file=sys.stderr)
        database = self.conn_params['database']
        del self.conn_params['database']
        self.connection = mariadb.connect(**self.conn_params)
        self.cursor = self.connection.cursor()
        with open('sql/createDB.sql') as sql:
            for line in sql.readlines():
                try: 
                    self.cursor.execute(line)
                except mariadb.ProgrammingError:
                    # to ignore error end of file
                    print('Error create DB', file=sys.stderr)
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
        

    # depreciated
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

    # depreciated
    def insert(self, table_name: str, d: dict) -> None:
        '''
        execute insert sql
        '''
        warnings.warn("deprecated", DeprecationWarning)
        sql = f"""insert into {table_name}({self.format_name_column(d)
            }) values({self.give_quationmark(d)})"""
        self.execute_and_commit(sql, tuple(d.values()))

    # depreciated
    def read_name_log(self, pipe: dict) -> None:
        '''
        Deprecation
        '''
        warnings.warn("use find_user_info", DeprecationWarning)
        id_user = self.select_one(
            'id_user', 'badge', 'id_badge', (pipe['id_badge'], ))
        if id_user is not None:
            pipe['name'], pipe['surname'] = self.select(
                ('name', 'surname'), 'user', 'id_user', (id_user, ))
            if self.check_with_badge_id:
                clog = self.select_log(('date', 'inside'), 'log',
                        'id_badge', (pipe['id_badge'], ), 'date', 5)
            else:
                clog = self.select_log(('date', 'inside'), 'log',
                        'id_user', (id_user, ), 'date', 5)
            pipe['log'] = self.cursor_to_dict_in_list(('date', 'inside'), clog)
            self.read_work_time(pipe)

    def get_user_id_with_badge(self, badge_id):
        '''
        >>> model = Model()
        >>> model.get_user_id_with_badge(45)
        116
        '''
        sql = "SELECT `id_user` FROM `badge` WHERE `id_badge` = ?"
        self.cursor.execute(sql, (badge_id, ))
        try:
            return self.cursor.next()[0]
        except TypeError:
            return self.cursor.next()
    
    def get_usernames(self, user_id):
        '''
        >>> model = Model()
        >>> model.get_usernames(116)
        ('Zéro-Six', 'Un-cinq')
        '''
        # to fix if offline and same id between user_write and user_sync
        print('get_usernames', file=sys.stderr)
        sql = 'SELECT `name`, `surname` FROM `user` WHERE `id_user` = ?;'
        self.cursor.execute(sql, (user_id, ))
        return self.cursor_to_tuple(self.cursor)
    
    def get_5_last_logs(self, badge_id):
        '''
        >>> model = Model()
        >>> type(model.get_5_last_logs(116))
        <class 'mariadb.connection.cursor'>
        '''
        user_id = self.get_user_id_with_badge(badge_id)
        sql = ('SELECT `date`, `inside`, `date_badge`, `date_modif`, '
               '`date_delete` FROM `log` WHERE `id_user` = ? OR '
               '`id_badge` = ? ORDER BY `date` DESC LIMIT 5;')
        self.cursor.execute(sql, (user_id, badge_id))
        return self.cursor

    def find_user_info(self, pipe: dict) -> None:
        user_id = self.get_user_id_with_badge(pipe['id_badge'])
        if user_id is None:
            return
        pipe['name'], pipe['surname'] = self.get_usernames(user_id)
        five_logs = self.get_5_last_logs(pipe['id_badge'])
        pipe['log'] = self.cursor_to_dict_in_list(('date', 'inside',
                'date_badge', 'date_modif', 'date_delete'), five_logs)
        

        # to refactory
        self.read_work_time(pipe)
    
    # depreciated
    @staticmethod
    def get_dict_log_list(log:list) -> dict:
       
        log_dict = dict()
        log_dict['date'] = log[0]
        log_dict['inside'] = log[1]
        log_dict['date_badge'] = log[2]
        log_dict['date_modif'] = log[3]
        log_dict['date_delete'] = log[4]
        return log_dict

    @classmethod
    def is_deleted_log(cls, log):
        return log['date_delete'] is not None

    def read_work_time(self, pipe: dict) -> None:
        '''
        >>> model = Model()
        >>> pipe = dict()
        >>> pipe['id_badge'] = 47
        >>> model.read_work_time(pipe)
        '''
        print('read_work_time', file=sys.stderr)
        last_week, current_week = self.get_2_week_log(pipe)
        pipe['time_last_week'] = self.calcul_work_time(tuple(filter(
            lambda x:not self.is_deleted_log(x), last_week)))
        pipe['time_current_week'] = self.calcul_work_time(tuple(filter(
            lambda x:not self.is_deleted_log(x), current_week)))

        self.read_work_time_day(pipe, last_week, current_week)

    # depreciated
    def select_one(self, select_name:str, table_name: str, where_name: str, 
                   value: tuple):
        warnings.warn('depreciated', DeprecationWarning)
        #sql = f"select id_user from badge where id_badge=483985410385;"
        sql = f"SELECT {select_name} FROM {table_name} WHERE {where_name}=?;"
        self.cursor.execute(sql, value)
        try:
            return self.cursor.next()[0]
        except TypeError:
            return self.cursor.next()

    # depreciated
    def select(self, select_name: tuple, table_name: str, where_name: str, 
               value: tuple) -> tuple:
        warnings.warn('depreciated', DeprecationWarning)
        sql = f"""select {self.format_tuple(select_name)} from {table_name
            } where {where_name}=?;"""
        self.cursor.execute(sql, value)
        return self.cursor_to_tuple(self.cursor)

    # depreciated
    def select_log(self, select_name: tuple, table_name: str, where_name: str,
                   value: tuple, order: str, limit: int):
        warnings.warn('depreciated', DeprecationWarning)
        if limit == 0:
            sql = f"""SELECT {self.format_tuple(select_name)} FROM {table_name
                } WHERE {where_name}=? ORDER BY {order} DESC"""
        else:
            sql = f"""SELECT {self.format_tuple(select_name)} FROM {table_name
                } WHERE {where_name}=? ORDER BY {order} DESC LIMIT {limit}"""
        self.cursor.execute(sql, value)
        return self.cursor

    # depreciated
    def select_log_date(self, select_name: tuple, table_name: str,
                        where_name: str, value: tuple, order: str):
        warnings.warn('depreciated', DeprecationWarning)
        sql = f"""select {self.format_tuple(select_name)} from {table_name
            } where {where_name}=? and date >=? order by {order} desc"""
        self.cursor.execute(sql, value)
        return self.cursor
    
    # depreciated
    def insert_user(self, select_name:str, table_name:str, value:tuple):
        warnings.warn("deprecated", DeprecationWarning)
        sql = f'''INSERT INTO {table_name} ({self.format_tuple(select_name)
        }) VALUES (NULL, ?, ?);'''
        self.cursor.execute(sql, value)
        self.connection.commit()
    
    def call_insert_user(self, value:tuple):
        print('call_insert_user', file=sys.stderr)
        sql = 'CALL `insert_user`(?, ?);'
        self.execute_and_commit(sql, value)
        print('end call_insert_user', file=sys.stderr)
    
    def select_new_user(self, value):
        sql = ('SELECT `id_user` FROM `user` WHERE name=? AND surname=? ORDER '
            'BY `id_user` DESC;')
        self.cursor.execute(sql, value)
        return self.cursor.next()[0]

    # depreciated
    def insert_badge(self, select_name:str, table_name:str, value:tuple):
        warnings.warn("deprecated", DeprecationWarning)
        sql = f'''INSERT INTO {table_name} ({self.format_tuple(select_name)
        }) VALUES (?, ?);'''
        self.execute_and_commit(sql, value)

    def call_insert_badge(self, value:tuple):
        '''
        call a stored procedure that insert badge
        '''
        print('call_insert_badge', file=sys.stderr)
        sql = 'CALL `insert_badge`(?, ?);'
        self.execute_and_commit(sql, value)
        print('end call_insert_badge', file=sys.stderr)

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
        '''
        print('call_insert_sync_log', file=sys.stderr)
        sql = 'CALL `insert_sync_log`(?, ?, ?, ?, ?, ?, ?, ?);'
        print(value, file=sys.stderr)
        self.execute_and_commit(sql, value)

    def call_insert_sync_user_badge(self, data:tuple):
        '''
        call a stored procedure that insert user and badge in the user_sync
        and badge_sync table 
        >>> # model = Model()
        >>> # model.call_insert_sync_user_badge(tuple([49, 8, 'a', 'b']))
        '''
        print('call_insert_sync_badge', file=sys.stderr)
        sql = 'CALL `insert_users_and_badges`(?, ?, ?, ?);'
        self.execute_and_commit(sql, data)

    def call_insert_sync_user(self, data:tuple) -> None:
        '''
        call a strored procedure that insert user in user_sync table
        >>> # model = Model()
        >>> # model.call_insert_sync_user(tuple([2, 'Name', 'Surname']))
        >>> # model.call_insert_sync_badge(tuple([88282828, 2, 3]))
        '''
        print('call_insert_sync_user', file=sys.stderr)
        sql = 'CALL `insert_user_sync`(?, ?, ?, ?, ?);'
        self.execute_and_commit(sql, data)

    def call_insert_sync_badge(self, data:tuple) -> None:
        '''
        call a strored procedure that insert badge in badge_sync table
        >>> # model = Model()
        >>> # model.call_insert_sync_badge(tuple([88282828, 2, 3]))
        '''
        print('call_insert_sync_badge', file=sys.stderr)
        sql = 'CALL `insert_badge_sync`(?, ?, ?, ?, ?);'
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
        >>> code = model.send_unsync_badges_and_users()
        >>> isinstance(code, int) or code is None
        True
        >>> model.test_del_user(ids[0])
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
        log_id = self.cursor.next()[0]
        if log_id is not None:
            return log_id
        else:
            return 0

    def get_last_badge_id(self) -> int:
        '''
        get the last id badge,
        maybe better to use last id user

        >>> model = Model()
        >>> isinstance(model.get_last_badge_id(), int)
        True
        '''
        print('get_last_badge_id', file=sys.stderr)
        sql = 'SELECT COUNT(`id_badge`) FROM `badge_sync`;'
        self.cursor.execute(sql)
        count = self.cursor.next()[0]
        print(count, file=sys.stderr)
        sql2 = (f'SELECT `id_badge` FROM `badge_sync` LIMIT {max(count-1, 0)}'
                ', 1;')
        print(sql2, file=sys.stderr)
        self.cursor.execute(sql2, count)
        try:
            badge_id = self.cursor.next()[0]
        except TypeError:
            badge_id = 0
        finally:
            print('badge_id = ', badge_id, file=sys.stderr)
            return badge_id
    
    def get_last_badge_id_via_last_user(self) -> int:
        '''
        get the last id badge,
        that is correct if the last user have the last badge
        >>> model = Model()
        >>> isinstance(model.get_last_badge_id_via_last_user(), int)
        True
        '''
        print('get_last_badge_id_via_last_user', file=sys.stderr)
        sql = ('SELECT `id_badge` '
        'FROM `badge_sync` '
        'WHERE `id_user` '
        'IN (SELECT MAX(`id_user`) FROM `user_sync`);')
        self.cursor.execute(sql)
        try:
            badge_id = self.cursor.next()[0]
        except TypeError:
            badge_id = 0
        finally:
            print('badge_id = ', badge_id, file=sys.stderr)
            return badge_id

    def get_last_badge_id_via_rowid_badge(self) -> int:
        '''
        get the last id badge, via rowid_badge that is a auto increment colomn
        >>> model = Model()
        >>> isinstance(model.get_last_badge_id_via_rowid_badge(), int)
        True
        '''
        print('get_last_badge_id_via_rowid_badge', file=sys.stderr)
        sql = (
            'SELECT `id_badge` '
            'FROM `badge_sync` '
            'WHERE `rowid_badge` IN '
            '(SELECT MAX(`rowid_badge`) FROM `badge_sync`);'
        )
        self.cursor.execute(sql)
        try:
            badge_id = self.cursor.next()[0]
            return badge_id
        except TypeError:
            return 0
        
    def get_last_badge_rowid(self) -> int:
        print('get_last_badge_rowid', file=sys.stderr)
        sql = 'SELECT MAX(`rowid_badge`) FROM `badge_sync`;'
        self.cursor.execute(sql)
        try:
            badge_id = self.cursor.next()[0]
            if badge_id is None:
                return 0
            else:
                return badge_id
        except TypeError:
            return 0


    def get_last_user_id(self) -> int:
        '''
        get the last user id of user_sync table
        >>> model = Model()
        >>> isinstance(model.get_last_user_id(), int)
        True
        '''
        print('get_last_user_id', file=sys.stderr)
        sql = ('SELECT MAX(`id_user`) '
        'FROM `user_sync`;')
        self.cursor.execute(sql)
        try:
            user_id = self.cursor.next()[0]
            if user_id is None:
                user_id = 0
        except TypeError:
            user_id = 0
        finally:
            print('user_id = ', user_id, file=sys.stderr)
            return user_id

    def get_last_updated_datetime(self, table:str):
        '''
        >>> model = Model()
        >>> isinstance(model.get_last_updated_datetime(),
        ...             datetime.datetime)
        True
        '''
        print('get_last_updated_datetime', file=sys.stderr)
        sql = ('SELECT MAX(`date_modif`) '
               'FROM `{0}`;')
        sql = sql.format(table)
        self.cursor.execute(sql)
        try:
            last_datetime = self.cursor.next()[0]
            if last_datetime is None:
                last_datetime = datetime.datetime.min
        except TypeError:
            last_datetime = datetime.datetime.min
        finally:
            print('last_datetime = ', last_datetime, file=sys.stderr)
            return last_datetime

    def get_last_updated_log_datetime(self):
        '''
        >>> model = Model()
        >>> isinstance(model.get_last_updated_log_datetime(),
        ...             datetime.datetime)
        True
        '''   
        return self.get_last_updated_datetime('log_sync')

    def invoke_receive_logs(self) -> None:
        '''
        receive all logs from remote server and insert in local database
        >>> model = Model()
        >>> model.invoke_receive_logs()
        '''
        print('model.invoke_receive_logs', file=sys.stderr)
        for log in self.api_client.receive_logs(
                self.get_last_updated_log_datetime()):
            print(log, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_log(tuple(log.values()))
        
    # depreciated
    def invoke_receive_users_and_badges(self) -> None:
        '''
        receive all users and badges from remote server and insert in local
        database
        '''
        print('invoke_receive_users_and_badges', file=sys.stderr)
        warnings.warn("use create_arg_args", DeprecationWarning)
        for badge_and_user in self.api_client.receive_users_and_badges(
                self.get_last_user_id()):
            print(badge_and_user, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_user_badge(tuple(badge_and_user.values()))
    
    def delete_badges_and_users_local(self) -> None:
        sql = 'CALL `delete_badge_and_user_write`;'
        self.cursor.execute(sql)

            
    def invoke_receive_users(self) -> None:
        '''
        receive all user from remote server and insert in local database
        '''
        print('invoke_receive_users', file=sys.stderr)
        for user in self.api_client.receive_users(
                self.get_last_updated_datetime('user_sync')):
            print(user, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_user(tuple(user.values()))
    
    def invoke_receive_badges(self) -> None:
        '''
        receive all badge from remote server and insert in local database
        >>> model = Model()
        >>> model.invoke_receive_users()
        >>> model.invoke_receive_badges()
        '''
        print('invoke_receive_badges', file=sys.stderr)
        for badge in self.api_client.receive_badges(
                self.get_last_updated_datetime('badge_sync')):
            print(badge, file=sys.stderr)
            # insert one per one in local. can be better
            self.call_insert_sync_badge(tuple(badge.values()))
        


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
    def old_calcul_work_time(logs: tuple):
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
    def calcul_work_time(cls, logs: tuple):
        print('calcul_work_time', file=sys.stderr)
        print(logs, file=sys.stderr)
        time = datetime.timedelta()
        date_in = None
        for log in logs[::-1]:
            if bool(log['inside']):
                if date_in is None:
                    date_in = log['date']
            elif date_in is not None:
                if date_in.day == log['date'].day: # ignore time with forgeting 
                    # outlog in the end of last day
                    # to text day on multi day with forteing the last
                    # first log of next day can bug
                    time += log['date'] - date_in
                date_in = None
        return time
    
    @classmethod
    def isolate_week(cls, logs: list)-> tuple:
        print('isolate_week', file=sys.stderr)
        current_week = list()
        last_week = list()
        last_monday = cls.find_last_monday(datetime.date.today())

        for log in logs:
            if cls.find_last_monday(log['date']) == last_monday:
                current_week.append(log)
            else:
                last_week.append(log)
        return tuple(last_week), tuple(current_week)

    @staticmethod
    def find_last_monday(date, n=0) -> datetime.date:
        '''
        n=0 the last monday (monday of the current week if monday is the first 
        day of the week).
        n=1 the monday before the last monday 
        '''
        print('find_last_monday', date, file=sys.stderr)
        try:
            return date.date() - datetime.timedelta(date.weekday() + 7*n)
        except:
            return date - datetime.timedelta(date.weekday() + 7*n)
    
    @staticmethod
    def is_same_day(date: datetime.date, date2: datetime.date) -> bool:
        print('is_same_day', file=sys.stderr)
        return ((date.day == date2.day) and (date.month == date2.month) and
                (date.year == date2.year))
        
    @classmethod
    def isolate_day(cls, logs:list) -> tuple:
        '''
        return a list with a list for each day.
        [id_day][id_log_in_the_day][key_of_property ex date, inside…]
        '''
        logs_per_day = list()
        logs_per_day.append(list())
        for log in logs:
            if len(logs_per_day[0]) == 0:
                logs_per_day[0].append(log)
            elif cls.is_same_day(log['date'], logs_per_day[-1][0]['date']):
                logs_per_day[-1].append(log)
            else:
                logs_per_day.append(list())
                logs_per_day[-1].append(log)
        return tuple(logs_per_day)

    @classmethod
    def get_date_and_work_time_day(cls, day_logs):
        try:
            print('model.get_work_time_day', file=sys.stderr)
            return (day_logs[0]['date'].date(), cls.calcul_work_time(day_logs))
        except IndexError:
            return None

    @classmethod
    def get_date_and_work_time_day_without_deleted(cls, day_logs):
        print('get_date_and_work_time_day_without_deleted', file=sys.stderr)
        filtered_logs = tuple(filter(lambda log: not cls.is_deleted_log(log),
                                day_logs))
        return cls.get_date_and_work_time_day(filtered_logs)

    def read_work_time_day(self, pipe:dict, last_week, current_week) -> None:
        '''
        add in dictionary in arg the date and sum work
        is a tuple. in each index there are a tuple with date [0] and sum time 
        work of the day [1]
        '''
        print('read_work_time_day', file=sys.stderr)
        pipe['last_week'] = self.isolate_day(last_week)
        pipe['current_week'] = self.isolate_day(current_week)
        pipe['day_last_week'] = tuple(map(
                self.get_date_and_work_time_day_without_deleted,
                pipe['last_week']))
        pipe['day_current_week'] = tuple(map(
                self.get_date_and_work_time_day_without_deleted,
                pipe['current_week']))

    def get_2_week_log(self, pipe:dict) -> tuple:
        '''
        >>> model = Model()
        >>> pipe = dict()
        >>> pipe['id_badge'] = 47
        >>> r = model.get_2_week_log(pipe)
        >>> isinstance(r, tuple)
        True
        '''
        id_user = self.get_user_id_with_badge(pipe['id_badge'])
        old_last_monday = self.find_last_monday(datetime.date.today(), 1)
        sql = ('SELECT `date`, `inside`, `date_badge`, `date_modif`, '
               '`date_delete` FROM `log` WHERE (`id_badge` = ? OR '
               '`id_user` = ?) AND `date` >= ? ORDER BY `date` DESC;')
        self.cursor.execute(sql, (pipe['id_badge'], id_user,
                                  old_last_monday))
        names = ('date', 'inside', 'date_badge', 'date_modif', 'date_delete')
        two_week_log = self.cursor_to_dict_in_list(names, self.cursor)
        return self.isolate_week(two_week_log)

    # deprecated
    def select_log_2_week(self, pipe: dict) -> tuple:
        warnings.warn("deprecated", DeprecationWarning)
        old_monday = self.find_last_monday(datetime.date.today(), 1)
        log2week = self.select_log_date(('date', 'inside'), 'log', 'id_badge',
                                        (pipe['id_badge'], old_monday), 'date')
        log2week = tuple(self.cursor_to_list(log2week))
        return self.isolate_week(log2week)

    # deprecated
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
        print('invoke_new_user', file=sys.stderr)
        value = (pipe['name'], pipe['surname'])
        print(value, file=sys.stderr)
        self.call_insert_user(value)
        user_id = self.select_new_user(value)
        print('user id', user_id, file=sys.stderr)
        value = (pipe['id_badge'], user_id)
        self.call_insert_badge(value)

    def test_add_user(self):
        '''
        just for unit test 
        '''
        print('test_add_user', file=sys.stderr)
        value = ('unit', 'test')
        self.call_insert_user(value)
        id = self.select_new_user(value)
        value = (51, id)
        self.call_insert_badge(value)
        return value

    def test_del_user(self, badge_id):
        '''
        just for unit test
        '''
        sql_user_id = 'SELECT `id_user` FROM `badge_write` WHERE `id_badge`=?;'
        sql_user = 'DELETE FROM `user_write` WHERE `id_user`=?;'
        sql_badge = 'DELETE FROM `badge_write` WHERE `id_badge`=?;'
        self.cursor.execute(sql_user_id, (badge_id, ))
        try:
            user_id = self.cursor.next()[0]
            self.execute_and_commit(sql_user, (user_id, ))
            self.execute_and_commit(sql_badge, (badge_id, ))
        except:
            pass







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
