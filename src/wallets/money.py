'''
основное рабочее поле
Деньги
1. Неотрицательный баланс кощелька при создании
- Пополнение
- Снятие
- Минус на кошельке неприемлим, даже при снятии
'''
from currency import rub, usd
from exceptions import NegativeValueException, NotComparisonException


class Money:
    '''Деньги'''
    def __init__(self, value: float, currency: 'Currency'):
        if value < 0:
            raise NegativeValueException
        self.value = value
        self.currency = currency

    def __eq__(self, other): # Сравнение если обьект не Mony и валюты не совпадают
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        return self.value == other.value

    def __add__(self, other): # Сложение и проверка на совпадение типа и валюты
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other): # Вычитание и проверка на совпадение типа и валюты
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException
        return Money(result, self.currency)

    def __hash__(self): # чтобы пихать в словарь
        return hash((self.value, self.currency))

    def __repr__(self): # Чисто по приколу посмотреть почитать
        return f'{self.value} {self.currency}'


class Wallet:
    '''Кошелек'''
    def __init__(self, initial_mony: Money):
        self.currenceies = {}
        self.currenceies[initial_mony.currency] = initial_mony

    def __getitem__(self, currency): # Надо ли мне это
        return self.currenceies.get(currency, Money(0, currency))
    


    def add(self, money: Money): # Сложение и на всякий создание добавляемого типа валюты
        if money.currency in self.currenceies:
            curretnt = self.currenceies[money.currency]
            self.currenceies[money.currency] = curretnt + money
        else:
            self.currenceies[money.currency] = Money(money.value, money.currency)
        return self

    def sub(self, money: Money):
        if money.currency not in self.currenceies:
            curretnt = Money(0, money.currency)
        else:
            curretnt = self.currenceies[money.currency]
        new_money = curretnt - money
        self.currenceies[money.currency] = new_money
        return self

    def __repr__(self): # Чисто по приколу посмотреть почитать
        return f'{self.currenceies}'


wallet1 = Wallet(Money(100, rub))
wallet2 = Wallet(Money(50, usd))
print(wallet2)
print(wallet2.add(Money(50, usd)))
print(wallet2.sub(Money(50, usd)))