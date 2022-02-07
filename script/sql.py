import mariadb

conn_params = {}
conn_params["user"] = "root"
conn_params["password"] = ""
conn_params["host"] = "localhost"
conn_params["database"] = "ci_crud_base"

connection = mariadb.connect(**conn_params)
cursor = connection.cursor()
cursor.execute("SELECT name from item;")

for i in cursor:
    print(i)