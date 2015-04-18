# coding: utf-8
"""
Логическая составляющя клиента
"""
# НЕРАБОЧАЯ ВЕРСИЯ!

import nc_net

field = []  # поле игры
# Фигуры
empty = ' '
nought = 'o'
cross = 'x'

firstPlayer = ''  # фигура первого игрока
secondPlayer = ''  # фигура второго игрока
sequence = []  # хранение очередности ходов


class FailedParty(Exception):
    """
    Исключение, возникающее при провале создания партии
    """
    pass


def start_game(**kwargs):
    """
    СОЗДАТЬ ПАРТИЮ
    Принимает:
    ничего
    Необязательные:
    идентификатор игрока, с которым хотелось бы сыграть

    Возвращает:
    кортеж:
    -очерёдность ходов

    """
    nc_net.transfer()
    return [empty] * 9
def moving(ceil):
    """
    ХОД ИГРОКА
    Принимает:
    """
    pass
def choosing():
    """
    ВЫБОР ФИГУРЫ

    """
    pass
