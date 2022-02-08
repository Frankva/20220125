import mariadb

conn_params = {}
conn_params["user"] = "admin"
conn_params["password"] = "1806"
conn_params["host"] = "localhost"
conn_params["database"] = "timbreuse2022"

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()
cursor.execute("create table log(id int, date datetime);")

#for i in cursor:
#    print(i)