from abc import ABC, abstractmethod

class Field(ABC):
    def __init__(self, value=None, primary_key=False, nullable=True, unique=False):
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is not None:
            self.validate(value)
        if not self.nullable and value is None:
            raise ValueError("This field cannot be null.")
        self._value = value

    @abstractmethod
    def validate(self, value):
        pass

    @abstractmethod
    def sql_type(self):
        pass