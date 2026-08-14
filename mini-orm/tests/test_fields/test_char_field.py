from unittest import TestCase
from mini_orm.fields.char_field import CharField

class TestCharField(TestCase):
    def test_init(self):
        field = CharField(value="test", max_length=100, primary_key=True, nullable=False, unique=True)
        self.assertEqual(field.value, "test")
        self.assertEqual(field.max_length, 100)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.nullable)
        self.assertTrue(field.unique)

    def test_valid_value_is_stored(self):
        field = CharField(value="test")
        self.assertEqual(field.value, "test")

    def test_invalid_value_raises(self):
        with self.assertRaises(ValueError) as ex:
            CharField(value=123)
        self.assertEqual(str(ex.exception), "Value '123' is not a string.")

    def test_value_exceeds_max_length_raises(self):
        with self.assertRaises(ValueError) as ex:
            CharField(value="a" * 300, max_length=255)
        self.assertEqual(str(ex.exception), f"Value '{'a' * 300}' exceeds maximum length of 255.")

    def test_sql_type(self):
        field = CharField(value="test")
        self.assertEqual(field.sql_type(), "VARCHAR(255)")