def save(self):
    # database must be configured before saving
    self.is_database_configured()

    field_names = []
    placeholders = []
    values = []
    for field_name, field_ref in self._fields.items():
        field_names.append(field_name)
        placeholders.append("?")
        values.append(getattr(self, field_name).value)
    if self._fields["id"].value == -1:
        # If the primary key is -1, we assume it's a new record and perform an INSERT
        sql = f"INSERT INTO {self.table_name} ({', '.join(field_names)}) VALUES ({', '.join(placeholders)})"
        self._database.execute(sql, tuple(values))
        # After insertion, we should retrieve the last inserted ID and set it to the object's id
        self.id.value = self._database.cursor.lastrowid
    else:
        # If the primary key is not -1, we assume it's an existing record and perform an UPDATE
        set_clause = ", ".join([f"{field_name} = ?" for field_name in field_names if field_name != "id"])
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        self._database.execute(sql, tuple(values[:-1] + [self.id.value]))
