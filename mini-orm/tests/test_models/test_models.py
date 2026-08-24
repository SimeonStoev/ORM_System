from unittest import TestCase
from mini_orm.database.sqlite_database import SqliteDatabase
from mini_orm.models.user_defined_models.user import User


class TestModelMeta(TestCase):
    def test_fields_are_collected(self):
        self.assertIn("id", User._fields)
        self.assertIn("name", User._fields)
        self.assertIn("age", User._fields)

    def test_default_table_name(self):
        self.assertEqual(User.table_name, "users")


class TestModelInit(TestCase):
    def test_instances_do_not_share_field_state(self):
        u1 = User(name="Ivan", age=30)
        u2 = User(name="Maria", age=25)
        u1.age.value = 99
        self.assertEqual(u1.age.value, 99)
        self.assertEqual(u2.age.value, 25)

    def test_missing_required_field_raises(self):
        with self.assertRaises(ValueError):
            # username е nullable=False, не е подаден
            user = User(id=1, name="Test")
            user.name.nullable = False
            user.name.value = None

    def test_repr_includes_all_fields(self):
        u = User(name="Ivan", age=30)
        self.assertIn("name='Ivan'", repr(u))
        self.assertIn("age=30", repr(u))


class TestCreateTable(TestCase):
    def setUp(self):
        User._database = SqliteDatabase(":memory:")

    def test_create_table_generates_correct_schema(self):
        User.create_table()
        self.assertTrue(User._database.table_exists("users"))

    def test_drop_table_removes_table(self):
        User.create_table()
        User.drop_table()
        self.assertFalse(User._database.table_exists("users"))
