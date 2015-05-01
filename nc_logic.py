# coding: utf-8
"""
Логическая составляющая клиента
"""
# ВЕСЬ ЭТОТ КОД ДОВОЛЬНО АБСТРАКТНЫЙ,
# ТАК КАК ПОКА НЕПОНЯТНО, КАК ВООБЩЕ
# БУДЕТ ПРОИСХОДИТЬ СВЯЗЬ

import nc_net


class WrongDataError(Exception):
    """
    Исключение, возникающее при передаче функциям неверных типов данных
    """
    # Необходимо перехватывать в nc_gui
    pass


class WrongAction(Exception):
    """
    Запрещённое действие
    """
    pass


class Game():
    def __init__(self):
        self.empty = None  # пустая ячейка
        self.cross = 0  # крестики
        self.nought = 1  # нолики
        # правила для определения выигрыша
        self.rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
                      (0, 4, 8), (2, 4, 6))  # по диагонали
        self.field = [self.empty] * 9  # игровое поле
        self.figure = -1  # фигура текущего игрока: 0 - крестик, 1 - нолик
        self.opp_figure = -1  # фигура противника
        self.sequence = -1  # очередность ходов: 0 - тек. игрок ходит первым, 1 - вторым
        self.opponent = 0  # идентификатор противника

    def start(self, opponent=0):
        """
        СОЗДАТЬ ПАРТИЮ
        Принимает:
            host (int, необязательный, равен 0 по умолчанию) - идентификатор игрока, с которым хотелось бы сыграть
        Возвращает:
            int:
                0 - партия создана, текущий игрок ходит первым, нужно выбрать фигуру
                1 - партия создана, текущий игрок ходит вторым, нужно дождаться выбора фигуры другим игроком
                2 - партия не создана, нет соединения/превышено время ожидания ответа сервера
                3 - партия не создана, превышыено время поиска игроков
                4 - партия не создана, не получилось соединиться с выбранным игроков
                5 - партия не создана, неизвестная ошибка
        """
        if not isinstance(opponent, int):
            raise WrongDataError

        # REVIEW [FChaack]
        # nc_net.make_party() возвращает кортеж из двух элементов:
        #   код (int):
        #       0 - текущий игрок ходит первым
        #       1 - текущий игрок ходит вторым
        #       2 - партия не создана, нет соединения/превышено ожидание ответа сервера
        #       3 - партия не создана, превышено время поиска игроков
        #       4 - партия не создана, не получилось соединиться с выбранным игроком
        #       5 - партия не создана, неизвестная ошибка
        #   идентификатор соперника (int) или (None) в случае неудачи
        value = nc_net.make_party(opponent)  # встать в очередь на сервере

        if value[0] in (0, 1):
            self.sequence = value[0]
            self.opponent = value[1]
            return value[0]
        elif value[0] in (2, 3, 4):
            return value[0]
        else:
            return 5

    def choose(self, figure):
        """
        ВЫБОР ФИГУРЫ
        Принимает:
            figure (int) - идентификатор фигуры (крестики или нолик)
                0 - крестик
                1 - нолик
        Возвращает:
            bool - успешен ли выбор фигуры
                True - успешен
                False - нет
        """
        if figure not in (0, 1):
            raise WrongDataError
        if self.figure != -1:  # если фигура уже была определена ранее
            raise WrongAction

        # REVIEW [FChaack] обмен данными
        # nc_net.transfer
        #   Принимает:
        #       operation (int) - код операции
        #           0 - выбор фигуры
        #   Возвращает:
        #       (bool) - успешность операции
        value = nc_net.transfer(operation=0, data=figure)

        if value is True:
            self.figure = figure
            self.opp_figure = self.nought if figure == self.cross else self.cross
            return True
        elif value is False:
            return False

    def moving(self, cell):
        """
        ХОД ИГРОКА
        Принимает:
            cell (int) - номер ячейки, выбранной игроком
                от 0 до 8
        Возвращает:
            (bool) - успешен ли выбор фигуры
                True - успешен
                False - нет
        """
        if cell not in range(0, 9):
            raise WrongDataError

        # REVIEW [FChaack]
        value = nc_net.transfer(operation=1, data=cell)

        if value is True:
            self.field[cell] = self.figure
            return True
        elif value is False:
            return False

    def check(self):
        """
        ПРОВЕРКА ВЫИГРЫША
        Проверка партии на наличие выигрышной ситуации
        Принимает:
            (None)
        Возвращает:
            (int):
                0 - в случае победы первого игрока;
                1 - в случае победы второго игрока;
                2 - в случае ничьи
                3 - выигрышная ситуация ещё не возникла
        """
        # WARN: требуется проверка работоспособности кода
        for rule in self.rules:
            # если выполняется какое-либо из правил
            if self.field[rule[0]] == self.field[rule[1]] == self.field[rule[2]] in (self.cross, self.nought):
                return 0 if self.field[rule[0]] == self.figure else 1
        if len(list(filter(lambda x: x == self.empty, self.field))) == 0:  # если нет больше пустых клеток
            return 2
        return 3

    def action(self, operation=-1, data=-1):
        """
        ПОЛУЧИТЬ ДАННЫЕ ПРОТИВНИКА
        -выбранная фигура
        -сделанный ход
        Принимает:
            operation (int) - код операции
            data (int) - данные
        """
        # REVIEW [FChaack]
        pass

    def kill(self):
        """
        ЗАВЕРШИТЬ ПАРТИЮ
        """
        nc_net.kill_party()
