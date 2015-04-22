"""
Логическая составляющая сервера
"""
from random import shuffle


field = []  # поле игры
# Фигуры
empty = None  # пустая ячейка
cross = 0  # крестики
nought = 1  # нолики

firstPlayer = ''  # фигура первого игрока
secondPlayer = ''  # фигура второго игрока
line = [0, 1]  # TEMP: очередность ходов

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


class WrongDataError(Exception):
    """
    Исключение, возникающее при передаче функциям неверных типов данных
    Необходимо перехватывать в nc_server_net
    """
    pass


def recieve(data):
    """
    ПРИЕМ ДАННЫХ
    Принимает данные, определяет тип запроса, передает данные функции,
    принимает от неё ответ, возвращает его клиенту
    Принимает:
        tuple:
            I элемент:
                int - тип запроса (к какой функции он адресован)
                    0 - старт игры
                    1 - выбор фигуры
                    2 - ход
            II элемент
                int - данные
    Возвращает:

    """
    if data[0] == 0:
        value = start()
        return True if value is True else False
    elif data[0] == 1:
        choosing(data[1])
    elif data[0] == 2:
        moving(data[1])


def start():
    """
    СТАРТ ИГРЫ
    """
    global field
    shuffle(line)
    field = [empty] * 9
    return True
    
    
def choosing(figure):
    """
    ВЫБОР ФИГУРЫ
    """
    pass


def moving(move):
    """
    ХОД
    """
    pass


def check():
    """
    ПРОВЕРКА ВЫИГРЫША
    check() -> int
    Проверка партии на наличие выигрышной ситуации
    Возвращает:
    0 - в случае победы игрока;
    1 - в случае победы компьютера;
    2 - в случае ничьи
    """
    # for i in range(len(rules)):
    #     if field[rules[i][0]] == field[rules[i][1]] == field[rules[i][2]] in (firPlayerFig, secPlayerFig):
    #         return 0 if field[rules[i][0]] == firPlayerFig else 1
    # if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
    #     return 2
    pass
