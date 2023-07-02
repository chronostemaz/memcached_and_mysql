import time
from functools import wraps


class TimeLogger:
    """
    Класс TimeLogger представляет собой логгер времени выполнения функций.
    """

    def __new__(cls, res: dict = {}, iterations: int = None):
        """
        Создает новый экземпляр класса TimeLogger.

        Args:
            res (dict): Словарь для хранения результатов времени выполнения функций.
            iterations (int): Количество итераций выполнения функций (необязательно).

        Returns:
            object: Экземпляр класса TimeLogger.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(TimeLogger, cls).__new__(cls)
            cls._res = res
        return cls.instance

    def __call__(self):
        """
        Метод-декоратор, который измеряет время выполнения функции и сохраняет результат.

        Returns:
            function: Обернутая функция с функциональностью измерения времени выполнения.
        """
        def timeit(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                s = round((end - start), 6)
                try:
                    self.res[func.__name__].append(s)
                except:
                    self.res[func.__name__] = [s]
                return result

            return wrapper

        return timeit

    @property
    def res(self):
        """
        Свойство для доступа к результатам времени выполнения функций.

        Returns:
            dict: Словарь с результатами времени выполнения функций.
        """
        return self._res

    @res.setter
    def res(self, res):
        """
        Сеттер для установки значений результатов времени выполнения функций.

        Args:
            res (dict): Словарь с результатами времени выполнения функций.
        """
        self._res = res
