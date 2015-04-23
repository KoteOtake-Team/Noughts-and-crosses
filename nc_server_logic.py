"""
Логическая составляющая сервера
"""
from random import shuffle


field = []  # поле игры
# Фигуры
empty = None  # пустая ячейка
cross = 0  # крестики
nought = 1  # нолики

player = []  # фигуры первого и второго игроков: [cross, nought] или [nought, cross]
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
            tuple:
                int - тип запроса (к какой функции он адресован)
                    0 - старт игры
                    1 - выбор фигуры
                    2 - ход
                int - данные для обрабатывающей функции
            string/int:
                информация об игроке (составляется в nc_server)
        Пример: ((1, 5),  2344)
    Возвращает:

    """
    if data[0] == 0:
        value = start()
        return True if value is True else False
    elif data[0] == 1:
        choosing(data[1])
    elif data[0] == 2:
        moving(data[1], player[0])


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


def moving(move, player):
    """
    ХОД

    """
    pass


def check():
    """
    ПРОВЕРКА ВЫИГРЫША
    Проверка партии на наличие выигрышной ситуации
    Принимает:
        ничего
    Возвращает:
        int:
            0 - в случае победы первого игрока;
            1 - в случае победы второго игрока;
            2 - в случае ничьи
            3 - выигрышная ситуация ещё не возникла
    """
    #TODO: требуется проверка работоспособности кода
    for rule in rules:
        # если выполняется какое-либо из правил
        if field[rule[0]] == field[rule[1]] == field[rule[2]] in (cross, nought):
            return 0 if field[rule[0]] == player[0] else 1
    if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
        return 2
    return 3
