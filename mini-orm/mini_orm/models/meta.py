from mini_orm.fields.field import Field


class ModelMeta(type):
    """
    Metaclass for models.
    """

    def __new__(cls, name, bases, attrs):
        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        attrs['_fields'] = fields
        if "table_name" not in attrs:
            attrs["table_name"] = f"{name.lower()}s"
        return super().__new__(cls, name, bases, attrs)