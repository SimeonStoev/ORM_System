from mini_orm.database.sqlite_database import SqliteDatabase

sqlite_obj = SqliteDatabase()

sqlite_obj.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")

result_all = sqlite_obj.fetch_all("SELECT * FROM users")
print(result_all)

sqlite_obj.execute("INSERT INTO users (name) VALUES (?)", ("Atanas",))
sqlite_obj.execute("INSERT INTO users (name) VALUES (?)", ("Mila",))

result = sqlite_obj.fetch_all("SELECT * FROM users")

result2 = sqlite_obj.fetch_all("SELECT * FROM users")

result_one = sqlite_obj.fetch_one("SELECT * FROM users WHERE name = ?", ("West park",))

print(result)
print(result2)
print(result_one)

sqlite_obj.close()


with SqliteDatabase() as db:
    db.execute("CREATE TABLE users_one (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("INSERT INTO users_one (name) VALUES (?)", ("West park",))
    result_one = db.fetch_one("SELECT * FROM users_one WHERE name = ?", ("West park",))
    print(result_one)