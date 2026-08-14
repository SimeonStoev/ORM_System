from unittest import TestCase
from mini_orm.fields.float_field import FloatField

class TestFloatField(TestCase):
    def test_init(self):
        # Test initialization with float value
        field = FloatField(3.14)
        self.assertEqual(field.value, 3.14)
        self.assertTrue(field.nullable)
        self.assertFalse(field.primary_key)
        self.assertFalse(field.unique)

        # Test initialization with int value
        field = FloatField(5)
        self.assertEqual(field.value, 5)

        # Test initialization with None value
        field = FloatField(None, nullable=True)
        self.assertIsNone(field.value)

    def test_float_field_validation(self):
        # Test valid float value
        field = FloatField(3.14)
        self.assertEqual(field.value, 3.14)
        field.value = 3
        self.assertEqual(field.value, 3)
        field.value = 5.67
        self.assertEqual(field.value, 5.67)

        # Test invalid float value
        with self.assertRaises(ValueError) as ex:
            field.value = "not a float"
        self.assertEqual(str(ex.exception), "Value 'not a float' is not a real number.")

    def test_float_field_nullable(self):
        # Test nullable field
        field = FloatField(None, nullable=True)
        self.assertIsNone(field.value)

        # Test non-nullable field
        field = FloatField(1.23, nullable=False)
        with self.assertRaises(ValueError) as ex:
            field.value = None
        self.assertEqual(str(ex.exception), "This field cannot be null.")

    def test_float_field_sql_type(self):
        field = FloatField(1.23)
        self.assertEqual(field.sql_type(), "REAL")