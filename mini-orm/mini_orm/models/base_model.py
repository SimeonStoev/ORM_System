from mini_orm.models.meta import ModelMeta
from mini_orm.fields.integer_field import IntegerField
from mini_orm.fields.char_field import CharField
from mini_orm.database.sqlite_database import SqliteDatabase

class Model(metaclass=ModelMeta):
    _database = None
    def __init__(self, **kwargs):
        for field_name, field_ref in self._fields.items():
            value = field_ref.value
            if field_name in kwargs:
                value = kwargs[field_name]
            setattr(self, field_name, field_ref.clone(value))

    def __repr__(self):
        fields_repr = [f"{field_name}={getattr(self, field_name).value}" for field_name in self._fields]
        fields = ", ".join(fields_repr)
        return f"{type(self).__name__}({fields})"

    @classmethod
    def configure(cls, database):
        cls._database = database

    @classmethod
    def create_table(cls):
        if cls._database is None:
            raise RuntimeError(
                f"{cls.__name__}._database is not configured. "
                f"Call {cls.__name__}.configure(database) first."
            )
        columns = []
        # name type primary key not null unique, new line
        for field_name, field_ref in cls._fields.items():
            field = f"{field_name} {field_ref.sql_type()}"
            if field_ref.primary_key:
                field += f" PRIMARY KEY"
            if not field_ref.nullable:
                field += " NOT NULL"
            if field_ref.unique:
                field += f" UNIQUE"
            columns.append(field)
        sql = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({', '.join(columns)})"
        cls._database.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = f"DROP TABLE IF EXISTS {cls.table_name}"
        cls._database.execute(sql)
