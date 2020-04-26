import sys  # sys нужен для передачи argv в QApplication
from itertools import permutations
from PyQt5 import QtWidgets
import main_form


class MainWindow(QtWidgets.QMainWindow, main_form.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.eval)

    @staticmethod
    def filter_group(data, static_num, group_name):
        result = []
        for num in static_num:
            if data[num][0] == group_name[num]:
                result.append(True)
            else:
                result.append(False)
        if False in result:
            return False
        else:
            return True

    @staticmethod
    def balance_phase(data):
        n_group = 3
        list_group = range(n_group)
        groups = []
        for i in list_group:
            group = []
            for j in range(4):
                index = i + n_group * j
                if index < len(data):
                    group.append(data[i + n_group * j][1])
                else:
                    break
            groups.append(sum(group))
        return max(groups) - min(groups)

    def eval(self):
        # Обработка входных данных
        group_name_raw = self.textGroup.toPlainText()
        power_list_raw = self.textPower.toPlainText()
        static_group_raw = self.textExc.toPlainText()

        if group_name_raw == ''or power_list_raw == '':
            return 0

        group_name = group_name_raw.strip().split('\n')
        power_list = power_list_raw.replace(',', '.').strip().split('\n')
        power_list = [float(x) for x in power_list]
        static_group = static_group_raw.strip().split('\n')

        self.textGroup.setText('\n'.join(group_name))
        self.textPower.setText('\n'.join(str(x) for x in power_list))
        self.textExc.setText('\n'.join(static_group))
        # вычислим номера исключений
        if static_group[0] == '':
            static_group = []
        static_num = [group_name.index(x) for x in static_group]
        data = list(zip(group_name, power_list))
        iters = list(permutations(data))
        
        iters = list(filter(lambda x: self.filter_group(x, static_num, group_name), iters))
        Q_dict = {i: self.balance_phase(x) for i, x in enumerate(iters)}
        best = iters[sorted(Q_dict.items(), key=lambda x: x[1])[0][0]]
        self.textResult.setText('\n'.join(str(x[0]) for x in best))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
