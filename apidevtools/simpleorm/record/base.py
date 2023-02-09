from typing import Any
from abc import ABC, abstractmethod


class BaseRecords(ABC):
    @abstractmethod
    def all(self) -> list['Record'] | list[dict[str, Any]]:
        ...

    @abstractmethod
    def first(self) -> 'Record' | dict[str, Any] | None:
        ...

    @abstractmethod
    def last(self) -> 'Record' | dict[str, Any] | None:
        ...

    @abstractmethod
    def limit(self, value: int) -> 'Records':
        ...

    @abstractmethod
    def offset(self, value: int) -> 'Records':
        ...
