from mini_orm.fields.field import Field


class CharField(Field):
    def __init__(self, value: str, max_length: int = 255, **kwargs):
        self.max_length = max_length
        super().__init__(value, **kwargs)

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Value '{value}' is not a string.")
        if len(value) > self.max_length:
            raise ValueError(f"Value '{value}' exceeds maximum length of {self.max_length}.")

    def sql_type(self):
        return f"VARCHAR({self.max_length})"