
from mimesis import Schema, Field
from mimesis.locales import Locale

import Operations
import Timer
from memcached_test_client import MemcachedClient
from sql_req import MySQLTEST


class TestData:
    """
    Класс для генерации тестовых данных и выполнения тестовых операций.

    Атрибуты:
    - sql_test: Объект MySQLTEST для выполнения тестовых операций с MySQL базой данных.
    - memcached_test_client: Объект MemcachedClient для выполнения тестовых операций с Memcached.

    Методы:
    - __init__(iterations): Инициализирует объект TestData с указанным количеством итераций.
    - start_test(): Запускает выполнение тестовых операций.
    """

    sql_test = MySQLTEST()
    memcached_test_client = MemcachedClient()

    def __init__(self, iterations):
        """
        Инициализация объекта TestData.

        :param iterations: Количество итераций для генерации тестовых данных.
        """
        self.iterations = iterations
        self.field = Field(Locale.RU)

        schema = Schema(
            schema=lambda: {
                "name": self.field("full_name"),
                "age": self.field("age"),
                "city": self.field("city"),
                "email": self.field("email"),
                "id": self.field("increment"),
            },
            iterations=self.iterations,
        )
        self.test_req = [(i['name'], int(i['age']), i['city'], i['email']) for i in schema]
        updated_schema = Schema(
            schema=lambda: {
                "name": self.field("full_name"),
                "age": self.field("age"),
                "city": self.field("city"),
                "email": self.field("email"),
                "id": self.field("increment")
            },
            iterations=self.iterations,
        )
        self.test_req1 = [(i['name'], int(i['age']), i['city'], i['email'], i['id']) for i in updated_schema]

    def start_test(self):
        """
        Запускает выполнение тестовых операций.
        """
        TestData.sql_test(self.test_req, self.test_req1)
        TestData.memcached_test_client(data_original=self.test_req, data_updated=self.test_req1)


if __name__ == "__main__":
    client = Operations.MySQLTESTing()
    for i in range(100, 30101, 7000):
        data = TestData(i)
        data.start_test()
        di = Timer.TimeLogger._res
        for key in di:
            for val in di[key]:
                client((key, val, i))
        Timer.TimeLogger._res = {}
    client.select_iter()
