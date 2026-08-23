from mini_orm.database.sqlite_database import SqliteDatabase
from mini_orm.models.user_defined_models.user import User

u1 = User(id=1, name="Ivan", age=30)
u2 = User(id=2, name="Koko", age=40)
print(u1)
print(u2)

u1.age.value = 35
print(u1)
print(u2)

User.configure(SqliteDatabase(":memory:"))
User.create_table()
print(User.table_name)
print(User._database.fetch_all("PRAGMA table_info(users)"))
User.drop_table()