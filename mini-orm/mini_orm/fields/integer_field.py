from mini_orm.fields.field import Field


class IntegerField(Field):
    def __init__(self, value: int, **kwargs):
        super().__init__(value, **kwargs)


    def validate(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"Value '{value}' is not an integer.")

    def sql_type(self):
        return "INTEGER"