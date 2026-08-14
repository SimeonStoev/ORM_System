from mini_orm.fields.field import Field


class BooleanField(Field):
    def __init__(self, value: bool, **kwargs):
        super().__init__(value, **kwargs)

    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Value '{value}' is not a boolean.")

    def sql_type(self):
        return "BOOLEAN"