from .currency import Currency, rub, usd
from .exceptions import NegativeValueException, NotComparisonException


class Money:
    """Деньги"""

    def __init__(self, value: float, currency: "Currency"):
        if value < 0:
            raise NegativeValueException
        self.value = value
        self.currency = currency

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        return self.value == other.value

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException
        return Money(result, self.currency)

    def __hash__(self):
        return hash((self.value, self.currency))

    def __repr__(self):
        return f"{self.value} {self.currency}"


class Wallet:
    """Кошелек"""

    def __init__(self, initial_mony: Money):
        self.currencies = {}
        self.currencies[initial_mony.currency] = initial_mony

    def __getitem__(self, currency):
        return self.currencies.get(currency, Money(0, currency))

    def __len__(self):
        return len(self.currencies)

    def __contains__(self, currency):
        return currency in self.currencies

    def __delitem__(self, currency):
        if currency in self.currencies:
            del self.currencies[currency]

    def add(self, money: Money):
        if money.currency in self.currencies:
            curretnt = self.currencies[money.currency]
            self.currencies[money.currency] = curretnt + money
        else:
            self.currencies[money.currency] = Money(money.value, money.currency)
        return self

    def sub(self, money: Money):
        if money.currency not in self.currencies:
            curretnt = Money(0, money.currency)
        else:
            curretnt = self.currencies[money.currency]
        new_money = curretnt - money
        self.currencies[money.currency] = new_money
        return self

    def __repr__(self):
        return f"{self.currencies}"
