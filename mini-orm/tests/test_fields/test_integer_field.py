from unittest import TestCase
from mini_orm.fields.integer_field import IntegerField


class TestIntegerField(TestCase):
    def test_init(self):
        field = IntegerField(value=10, primary_key=True, nullable=False, unique=True)
        self.assertEqual(field.value, 10)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.nullable)
        self.assertTrue(field.unique)

    def test_valid_value_is_stored(self):
        field = IntegerField(value=10)
        self.assertEqual(field.value, 10)

    def test_invalid_value_raises(self):
        with self.assertRaises(ValueError) as ex:
            IntegerField(value="not an int")
        self.assertEqual(str(ex.exception), "Value 'not an int' is not an integer.")

    def test_none_value_is_allowed(self):
        field = IntegerField(value=None)
        self.assertIsNone(field.value)

    def test_sql_type(self):
        field = IntegerField(value=10)
        self.assertEqual(field.sql_type(), "INTEGER")

    def test_setter_rejects_invalid_value_after_construction(self):
        field = IntegerField(value=5)
        with self.assertRaises(ValueError) as ex:
            field.value = "abc"
        self.assertEqual(str(ex.exception), "Value 'abc' is not an integer.")
        self.assertEqual(field.value, 5)  # старата стойност остава непроменена
