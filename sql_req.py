import MySQLdb
from Timer import TimeLogger


class MySQLTEST:
    """
    Класс для работы с MySQL базой данных.
    """

    def __init__(self, host="localhost", user_name="root", password="repeatafterme", db_name="clients", port=4000):
        """
        Инициализация объекта MySQLTEST.

        :param host: Хост базы данных.
        :param user_name: Имя пользователя для доступа к базе данных.
        :param password: Пароль для доступа к базе данных.
        :param db_name: Имя базы данных.
        :param port: Порт для подключения к базе данных.
        """
        self.db = MySQLdb.connect(host, user_name, password, db_name, port=port)
        self.cur: MySQLdb.cursors.Cursor = self.db.cursor()
        self.create_test_table = "CREATE TABLE IF NOT EXISTS clients_test (" \
                                 "name VARCHAR(50)," \
                                 "age INT," \
                                 "city VARCHAR(50)," \
                                 "email VARCHAR(100)," \
                                 "ID int AUTO_INCREMENT," \
                                 "PRIMARY KEY(ID));"
        self.insert_test_table = "INSERT INTO clients_test (name, age, city, email)" \
                                 "VALUES (%s, %s, %s, %s);"
        self.update_test_table = "UPDATE clients_test SET name=%s, age=%s, city=%s, email=%s WHERE ID=%s;"
        self.drop_test_table = 'DROP TABLE IF EXISTS clients_test;'

    def __call__(self, data_original, data_updated):
        """
        Метод, выполняющий операции взаимодействия с базой данных.

        :param data_original: Данные для вставки в таблицу.
        :param data_updated: Данные для обновления в таблице.
        """
        time_logger = TimeLogger()

        @time_logger()
        def drop_test_table_foo():
            """
            Метод для удаления тестовой таблицы.
            """
            self.cur.execute(self.drop_test_table)
            self.db.commit()

        @time_logger()
        def create_test_table_foo():
            """
            Метод для создания тестовой таблицы и вставки данных.
            """
            self.cur.executemany(self.insert_test_table, data_original)
            self.db.commit()

        @time_logger()
        def update_test_table_foo():
            """
            Метод для обновления данных в тестовой таблице.
            """
            self.cur.executemany(self.update_test_table, data_updated)
            self.db.commit()

        @time_logger()
        def select_all():
            """
            Метод для выборки всех данных из тестовой таблицы.
            """
            self.cur.execute("SELECT * FROM clients_test;")
            self.cur.fetchall()

        for i in range(0, 5):
            self.cur.execute(self.create_test_table)
            create_test_table_foo()
            select_all()
            update_test_table_foo()
            drop_test_table_foo()

