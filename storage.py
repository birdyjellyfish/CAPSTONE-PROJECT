import sqlite3

class Collection:
    """
    Collection class acts as an interface with the database and its tables.

    Methods:
    add(record)
    get(name)
    update(name, record)
    delete(name)
    """
    def __init__(self, dbname, tblname):
        self._dbname = dbname
        self._tblname = tblname

    def __repr__(self):
        pass

    def _execute(self, query, values=None):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        c.execute(query, values)
        conn.commit()
        conn.close()

    def add(self, record: dict):
        """Adds a record into the table"""
        return record
        
    def get(self, name: str):
        """Returns a record with the corresponding name from collection"""
        return record

    def update(self, name: str, record: dict):
        """Updates a record with the corresponding name from collection"""
        return

    def delete(self, name: str):
        """Deletes the record with the corresponding name"""
        return

#junction table class needs to be updated to support multiple junction tables
class JunctionTable(Collection):
    """
    """
    def __init__(self):
        super().__init__("JunctionTable")

class Students(Collection):
    """
    Student Collection
    """
    def __init__(self):
        super().__init__("Webapp_Database", "Students")

    def add(self, record: dict):
        query = f"""
                INSERT INTO {self._tblname} VALUES (?, ?, ?, ?, ?)
                """
        values = tuple(record.values())
        self._execute(query, values)

class Classes(Collection):
    """
    Classes Collection
    """
    def __init__(self):
        super().__init__("Classes")


class Subjects(Collection):
    """
    Subjects Collection
    """
    def __init__(self):
        super().__init__("Subjects")


class Ccas(Collection):
    """
    CCAs Collection
    """
    def __init__(self):
        super().__init__("CCAs")


class Activities(Collection):
    """
    Activities Collection
    """
    def __init__(self):
        super().__init__("Activies")

