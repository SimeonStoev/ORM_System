from mini_orm.fields.field import Field


class FloatField(Field):
    def __init__(self, value: float | int, **kwargs):
        super().__init__(value, **kwargs)

    def validate(self, value):
        if not isinstance(value, (float, int)) or isinstance(value, bool):
            raise ValueError(f"Value '{value}' is not a real number.")

    def sql_type(self):
        return "REAL"