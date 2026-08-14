from unittest import TestCase
from mini_orm.fields.boolean_field import BooleanField

class TestBooleanField(TestCase):
    def test_init(self):
        field = BooleanField(value=True)
        self.assertEqual(field.value, True)
        self.assertFalse(field.primary_key)
        self.assertTrue(field.nullable)
        self.assertFalse(field.unique)

    def test_valid_value_is_stored(self):
        field = BooleanField(value=True)
        self.assertEqual(field.value, True)

    def test_invalid_value_raises(self):
        with self.assertRaises(ValueError) as ex:
            BooleanField(value="not a bool")
        self.assertEqual(str(ex.exception), "Value 'not a bool' is not a boolean.")

    def test_none_value_is_allowed(self):
        field = BooleanField(value=None)
        self.assertIsNone(field.value)

    def test_none_value_is_not_allowed(self):
        with self.assertRaises(ValueError) as ex:
            BooleanField(value=None, nullable=False)
        self.assertEqual(str(ex.exception), "This field cannot be null.")

    def test_sql_type(self):
        field = BooleanField(value=True)
        self.assertEqual(field.sql_type(), "BOOLEAN")

    def test_setter_rejects_invalid_value_after_construction(self):
        field = BooleanField(value=True)
        with self.assertRaises(ValueError) as ex:
            field.value = "abc"
        self.assertEqual(str(ex.exception), "Value 'abc' is not a boolean.")
        self.assertEqual(field.value, True)  # старата стойност остава непроменена