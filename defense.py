import numpy as np
import matplotlib.pyplot as plt


class Relay:
    """
    Класс защит типа реле - аналоговых или цифровых
    """

    def __init__(self, name,  stages: list):
        """
        Задание ступеней защит

        :param stages: tuple("тип ступени", (Ir, Tr))
        """
        self.name = name
        self.stages = stages

    def response_time(self, current):
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
        """
        Независимая характеристика выдержки времени

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        response = np.piecewise(current, [current < Ir, current >= Ir], [10000, Tr])
        return response

    @staticmethod
    def rtv_4(current, settings):
        """
        Зависимая нормальная характеристика выдержки времени типа РТВ-4

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        func = lambda I: 1 / (20 * ((I / Ir - 1) / 6) ** 1.8) + Tr
        response = np.piecewise(current, [current < Ir, current >= Ir], [10000, func])
        return response

    @staticmethod
    def rtv_1(current, settings):
        """
        Зависимая характеристика выдержки времени типа РТВ-1

        :param current: numpy array
        :param settings: tuple(Ir, Tr)
        :return: response_times: numpy array
        """
        Ir, Tr = settings
        func = lambda I: 1 / (30 * (I / Ir - 1) ** 3) + Tr
        response = np.piecewise(current, [current < Ir, current >= Ir], [10000, func])
        return response


def plot_defense(scheme):
    """
    Диаграмма селективности защит
    :param scheme: список аппаратов защиты
    """
    x = np.arange(10, 10000, 0.1)
    plt.figure(figsize=(12, 8))
    [plt.plot(x, relay.response_time(x), label=relay.name) for relay in scheme]
    plt.xlabel(r'$Ток, А$', fontsize=12)
    plt.ylabel(r'$t_{с.з.}, сек$', fontsize=12)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='both')
    plt.ylim(0.01, 1000)
    plt.xlim(10, 10000)
    plt.title('ДИАГРАММА СЕЛЕКТИВНОСТИ ЗАЩИТ')
    plt.legend()
    plt.savefig('Диаграмма селективности.png', bbox_inches='tight', dpi=300)
    plt.show()


# Пример
if __name__ == '__main__':
    scheme = [Relay('Проект. КТП', [('rtv_4', (110, 9)), ('independent', (183, 0.5)), ('independent', (1377, 0.01))]),
              Relay('РТП-12 Байсад Л-2', [('independent', (220, 0.8)), ('independent', (5192, 0.01))]),
              Relay('РТП-12 Секционный', [('independent', (300, 1.1))]),
              Relay('РТП-12 ф.26 ПС-224', [('independent', (360, 1.4))]),
              Relay('ПС-224 ф.26', [('independent', (400, 1.8))])]
    plot_defense(scheme)
