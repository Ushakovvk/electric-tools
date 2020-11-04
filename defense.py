import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


class Switch:
    """Класс аппаратов защиты"""

    def __init__(self, label: str,  stages: list):
        """Задание ступеней защиты

        Args:
            label (str): Название аппарата защиты
            stages (list): Характеристика ступени защиты
        """
        self.label = label
        self.stages = stages

    def __call__(self, current):
        """Вычисление времени срабатывания

        Args:
            current (numpy array): Массив тока

        Returns:
            numpy array: Массив времени срабатывания
        """
        current = np.array(current, dtype=float)
        response = []
        for stage in self.stages:
            func_type, settings = stage
            stage_func = getattr(self, func_type)
            stage_response = stage_func(current, settings)
            response.append(stage_response)
        return np.min(response, axis=0)

    @staticmethod
    def independent(current, settings):
        """Независимая характеристика выдержки времени

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        response = np.piecewise(
            current, [current < Ir, current >= Ir], [10000, Tr])
        return response

    @staticmethod
    def rtv_1(current, settings):
        """Зависимая характеристика выдержки времени типа РТВ-1

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        def func(I): return 1 / (30 * (I / Ir - 1) ** 3) + Tr
        response = np.piecewise(
            current, [current < Ir, current >= Ir], [10000, func])
        return response

    @staticmethod
    def rtv_4(current, settings):
        """Зависимая нормальная характеристика выдержки времени типа РТВ-4

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        def func(I): return 1 / (20 * ((I / Ir - 1) / 6) ** 1.8) + Tr
        response = np.piecewise(
            current, [current < Ir, current >= Ir], [10000, func])
        return response

    @staticmethod
    def overload(current, settings):
        """Перегрузка

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        def func(I): return ((1.5 * Ir / I)**2) * Tr
        response = np.piecewise(
            current, [current < Ir, current >= Ir], [10000, func])
        return response

    @staticmethod
    def inversely(current, settings):
        """Обратнозависимая характеристика

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        def func(I): return ((8 * Ir / I)**2) * Tr
        response = np.piecewise(
            current, [current < Ir, current >= Ir], [10000, func])
        return response

    @staticmethod
    def overload_csv(current, filename):
        """Перегрузка из файла csv """
        data = pd.read_excel(filename)
        func = interp1d(data['x'], data['y'], bounds_error=False)
        response = func(current)
        return response


def plot_defense(scheme, path_to_savefig=None):
    """Построение графика селективности защит

    Args:
        scheme (list): список аппаратов защиты
        path_to_savefig (str, optional): Путь для сохраниния графика. Defaults to None.
    """
    x_limit = 100000
    y_limit = 1000
    x = np.arange(10, x_limit, 0.1)
    plt.figure(figsize=(12, 8))
    [plt.plot(x, relay(x), label=relay.label) for relay in scheme]
    plt.xlabel(r'$Ток, А$', fontsize=12)
    plt.ylabel(r'$t_{с.з.}, сек$', fontsize=12)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='both')
    plt.ylim(0.01, y_limit)
    plt.xlim(10, x_limit)
    plt.title('ДИАГРАММА СЕЛЕКТИВНОСТИ ЗАЩИТ')
    plt.legend()
    plt.vlines([9600, 20000], 0.01, y_limit)
    if path_to_savefig:
        plt.savefig(path_to_savefig, bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == "__main__":
    """Пример работы"""
    scheme = [
        Switch('ШР', [('overload_csv', 'ВА-99 1000А.xlsx'), ('independent', (8000, 0.01))]),
        Switch('КТП-0,4-секц', [('overload', (1440, 15)), ('independent', (1900, 0.1)), ('independent', (13750, 0.01))]),
        Switch('КТП-0,4', [('overload', (1730, 15)), ('independent',(2300, 0.2)), ('independent', (16500, 0.01))]),
        Switch('Проект. КТП', [('independent', (183*15, 0.3)), ('independent', (1614*15, 0.01))]),
        Switch('РП-12 Байсад Л-2', [('independent', (220*15, 0.5)), ('independent', (5192*15, 0.01))])
    ]
    plot_defense(scheme)
