from Timer import TimeLogger
from pymemcache.client import base


class MemcachedClient:
    """
    Класс MemcachedClient представляет собой клиент для работы с Memcached.
    """

    def __init__(self, host: str = 'localhost', port: int = 11211):
        """
        Инициализация клиента MemcachedClient.

        Args:
            host (str): Хост Memcached (по умолчанию 'localhost').
            port (int): Порт Memcached (по умолчанию 11211).
        """
        self._host = host
        self._port = port
        self.client = base.Client((self._host, self._port), encoding='utf-8')

    def __call__(self, data_original, data_updated):
        """
        Вызываемый метод класса MemcachedClient.

        Args:
            data_original: Исходные данные для сохранения в Memcached.
            data_updated: Обновленные данные для сохранения в Memcached.
        """
        time_logger = TimeLogger()

        @time_logger()
        def create_in_memcached():
            """
            Сохраняет исходные данные в Memcached.
            """
            self.client.add(key, data_original)

        @time_logger()
        def read_in_memcached():
            """
            Читает данные из Memcached.
            """
            self.client.get(key)

        @time_logger()
        def update_in_memcached():
            """
            Обновляет данные в Memcached.
            """
            self.client.replace(key, data_updated)

        @time_logger()
        def delete_in_memcached():
            """
            Удаляет данные из Memcached.
            """
            self.client.delete(key)

        key = 'test-data'
        for _ in range(0, 5):
            create_in_memcached()
            read_in_memcached()
            update_in_memcached()
            delete_in_memcached()

