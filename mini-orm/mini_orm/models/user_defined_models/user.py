from mini_orm.fields.char_field import CharField
from mini_orm.fields.integer_field import IntegerField
from mini_orm.models.base_model import Model


class User(Model):
    id = IntegerField(value=-1, primary_key=True, nullable=False)
    name = CharField(value=None, max_length=100)
    age = IntegerField(value=None)
    descr = CharField(value=None, max_length=100)