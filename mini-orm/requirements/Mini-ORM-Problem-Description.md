# Mini ORM — Problem Description

## Идея

Изгради опростен ORM (Object-Relational Mapping) framework на чист Python, който позволява дефиниране на модели като класове, автоматично генериране на SQL, и извършване на CRUD операции и заявки чрез Python синтаксис, вместо суров SQL. Базата данни е SQLite (вградена в Python, не изисква инсталация на сървър).

Вдъхновение: опростена версия на Django ORM / SQLAlchemy.

---

## Технологии

- Python 3.11+
- `sqlite3` (вграден модул, за връзка с базата)
- `unittest` или `pytest` за тестове
- Без външни ORM/DB библиотеки — цялата логика се пише сама, това е смисълът на проекта

---

## Итерация 1 — Database Connection Layer

### Клас `Database`

Отговаря само за директна комуникация с базата — без никаква ORM логика.

**Атрибути:**
- `connection` — обект на връзката към SQLite базата
- `db_path: str` — път до `.db` файла

**Методи:**
- `__init__(db_path: str = ":memory:")` — отваря връзка. По подразбиране `:memory:` (база в RAM, идеална за тестове, изчезва след затваряне)
- `execute(sql: str, params: tuple = ())` — изпълнява SQL команда (INSERT/UPDATE/DELETE/CREATE), прави `commit()`
- `fetch_all(sql: str, params: tuple = ()) -> list[tuple]` — изпълнява `SELECT`, връща всички редове
- `fetch_one(sql: str, params: tuple = ()) -> tuple | None` — изпълнява `SELECT`, връща първия ред или `None`
- `close()` — затваря връзката

**Definition of Done:**
- Можеш ръчно да пишеш суров SQL през `Database` и да получаваш резултати
- Unit тест: създай таблица, вкарай ред, прочети го обратно

---

## Итерация 2 — Field Types (дескриптори)

### Базов клас `Field` (абстрактен)

**Атрибути:**
- `name: str` — име на полето (задава се автоматично от метакласа в Итерация 3)
- `primary_key: bool = False`
- `nullable: bool = True`
- `unique: bool = False`

**Методи:**
- `__set_name__(self, owner, name)` — стандартен Python dunder метод за дескриптори, автоматично улавя името на атрибута
- `__get__(self, instance, owner)` — връща стойността от `instance.__dict__`
- `__set__(self, instance, value)` — валидира стойността (`validate()`), после я записва
- `validate(self, value)` — **абстрактен**, всеки подтип имплементира собствена проверка
- `sql_type(self) -> str` — **абстрактен**, връща SQL типа (`"INTEGER"`, `"TEXT"`, и т.н.)

### Подкласове

**`IntegerField(Field)`**
- `validate()` — грешка, ако стойността не е `int`
- `sql_type()` → `"INTEGER"`

**`CharField(Field)`**
- Допълнителен атрибут `max_length: int = 255`
- `validate()` — грешка, ако не е `str`, или ако дължината надвишава `max_length`
- `sql_type()` → `f"VARCHAR({max_length})"`

**`BooleanField(Field)`**
- `validate()` — грешка, ако не е `bool`
- `sql_type()` → `"BOOLEAN"`

**`FloatField(Field)`**
- `validate()` — грешка, ако не е `int`/`float`
- `sql_type()` → `"REAL"`

**Definition of Done:**
- Unit тест: създаване на поле, валиден/невалиден assignment, проверка на хвърлените грешки
- Проверка, че `sql_type()` връща очаквания SQL низ за всеки тип

---

## Итерация 3 — Model Base Class + Metaclass

### `ModelMeta(type)` — метаклас

**Логика в `__new__`:**
- Обхожда `namespace` (атрибутите на класа по време на дефиниране)
- Събира всички атрибути, които са инстанции на `Field`, в речник `_fields: dict[str, Field]`
- Определя `table_name` — по подразбиране името на класа в snake_case и множествено число (напр. `User` → `"users"`), с възможност за override през `Meta` вложен клас

### `Model` (базов клас, ползва `ModelMeta`)

**Атрибути (клас-ниво, попълнени от метакласа):**
- `_fields: dict[str, Field]`
- `table_name: str`

**Методи:**
- `__init__(self, **kwargs)` — задава стойност на всяко поле от `kwargs`; ако липсва задължително поле (не `nullable`), хвърля грешка
- `__repr__(self)` — `"<User id=1 name='Ivan'>"` формат
- `create_table(cls)` — `classmethod`, генерира и изпълнява `CREATE TABLE IF NOT EXISTS ...` от `_fields`
- `drop_table(cls)` — `classmethod`, изпълнява `DROP TABLE IF EXISTS ...`

**Definition of Done:**
- `User.create_table()` реално създава таблица в SQLite с правилни колони/типове
- Проверка чрез `PRAGMA table_info(users)` в тест, че колоните съвпадат с дефинираните полета

---

## Итерация 4 — CRUD операции (instance-level)

Разширение на `Model`:

- `save(self)` — ако инстанцията няма `id` (или той е `None`), генерира `INSERT`; ако вече има `id`, генерира `UPDATE ... WHERE id = ?`
- `delete(self)` — генерира `DELETE FROM ... WHERE id = ?`; хвърля грешка, ако обектът няма `id` (никога не е бил запазен)
- `refresh_from_db(self)` — презарежда актуалните стойности на инстанцията от базата (полезно, ако друг процес я е променил)

**Definition of Done:**
- Тест: създай инстанция, `save()`, провери че `id` вече е зададен
- Тест: промени атрибут, `save()` отново, провери че се е обновил (не създава нов ред)
- Тест: `delete()`, провери че редът вече не съществува

---

## Итерация 5 — Query Builder / Manager

### `QuerySet` / `Manager`

Достъпен през `Model.objects` (реализирано с дескриптор или property на класа).

**Методи:**
- `all(self) -> list[Model]` — `SELECT * FROM table`, връща списък инстанции
- `get(self, **kwargs) -> Model` — очаква точно един резултат; хвърля грешка при 0 или повече от 1 резултат
- `filter(self, **kwargs) -> list[Model]` — генерира `WHERE` клауза от подадените условия

**Поддръжка на lookup оператори** (по подобие на Django):
- `field=value` → `WHERE field = ?`
- `field__gt=value` → `WHERE field > ?`
- `field__gte=value` → `WHERE field >= ?`
- `field__lt=value` / `field__lte=value`
- `field__contains=value` → `WHERE field LIKE '%value%'`

**Помощна логика:**
- Parser, който разбива `"age__gte"` на `("age", "gte")` и превежда `"gte"` в SQL оператор `">="`

**Definition of Done:**
- Тест: `User.objects.filter(age__gte=18)` връща правилните инстанции
- Тест: `User.objects.get(id=5)` връща точно един обект или хвърля грешка

---

## Итерация 6 (по избор, ако остане време) — Relations

### `ForeignKey(Field)`

- Атрибут `to: type[Model]` — сочи към друг модел
- `sql_type()` → `"INTEGER REFERENCES {to.table_name}(id)"`
- При достъп до атрибута (`order.user`), автоматично прави `SELECT` за свързания обект (lazy loading)

**Definition of Done:**
- Дефинираш два свързани модела (`User`, `Order` с `user = ForeignKey(User)`)
- `order.user` връща реален `User` обект, не просто `id`

---

## Итерация 7 — Тестове, документация, финализация

- Пълно unit test покритие за всеки клас (`Database`, всеки `Field` тип, `Model`, `QuerySet`)
- README.md с:
  - Кратко описание на проекта
  - Инсталация (`pip install -r requirements.txt` дори да е празен файл, за конвенция)
  - Примери за употреба (copy-paste-able код блокове)
  - Списък на поддържаните lookup оператори
- (По желание) GitHub Actions workflow, който пуска тестовете при всеки push

---

## Груб график (4 седмици)

| Седмица | Итерации |
|---|---|
| 1 | Итерация 1 + 2 (Database layer + Field types) |
| 2 | Итерация 3 + 4 (Model + Metaclass + CRUD) |
| 3 | Итерация 5 (Query Builder), + Итерация 6 ако остане време |
| 4 | Тестове, refactoring, README, push в GitHub |

---

## Идеи за втора итерация (следващия месец, надграждане)

- Migrations система (проследяване на промени в схемата между версии)
- Връзка с PostgreSQL като алтернатива на SQLite (абстрактен `Database` interface с няколко имплементации)
- `ManyToManyField` (връзка много-към-много, junction table)
- Прост FastAPI слой отгоре, който излага CRUD операциите като REST endpoints
- Query кеширане
- `select_related()` за eager loading на връзки (избягва N+1 проблема)
