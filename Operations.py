import MySQLdb
import pandas as pd


class MySQLTESTing:
    """
    Класс для работы с MySQL базой данных и выполнения запросов.
    """

    def __init__(self, host="localhost", user_name="root", password="repeatafterme", db_name="clients", port=4000):
        self.db = MySQLdb.connect(host, user_name, password, db_name, port=port)
        self.cur: MySQLdb.cursors.Cursor = self.db.cursor()
        create_test_table = "CREATE TABLE IF NOT EXISTS time_explains (" \
                                 "name VARCHAR(50)," \
                                 "time FLOAT," \
                                 "iterations INT," \
                                 "ID int AUTO_INCREMENT," \
                                 "PRIMARY KEY(ID));"
        self.cur.execute(create_test_table)
        self.insert_test_table = "INSERT INTO time_explains (name, time, iterations)" \
                                 "VALUES (%s, %s, %s);"

    def __call__(self, data):
        def create_test_table_foo():
            self.cur.execute(self.insert_test_table, data)
            self.db.commit()

        create_test_table_foo()

    def select_iter(self):
        df = pd.read_sql("SELECT * from time_explains ORDER BY iterations;", self.db)
        df.to_excel('tur.xlsx')

