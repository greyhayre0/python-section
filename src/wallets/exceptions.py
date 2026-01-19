class NegativeValueException(Exception):
    '''при попытке получить отрицательную сумму'''
    pass


class NotComparisonException(Exception):
    '''при операциях с разными валютами'''
    pass
