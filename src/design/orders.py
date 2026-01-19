from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass
class Order:
    """There is no need to describe anything here."""


class OrderInterface(ABC):
    @abstractmethod
    def total(self) -> float:
        pass


class Discount:
    @abstractmethod
    def apply(self, order: OrderInterface) -> float:
        pass


class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        return min(self.amount, order.total())


class PercentDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        return order.total() * (self.amount / 100)


class LoyalDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        if order.loyal():
            return self.amount
        return 0


class DiscountFactory:
    def __init__(self):
        self._registry: Dict[str, Callable[float, Discount]] = {}  # type: ignore

    def register(
        self, discount_type: str, constructor: Callable[[float], Discount]
    ) -> None:
        self._registry[discount_type] = constructor

    def create(self, discount_type: str, value: float) -> Optional[Discount]:
        constructor = self._registry.get(discount_type)
        if not constructor:
            return None
        return constructor(value)
