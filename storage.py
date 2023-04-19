import pymongo

class Collection:
    """
    Collection class acts as an interface with the database and its tables.

    Methods:
    add(record)
    get(name)
    update(name, record)
    delete(name)
    """
    def __init__(self, collection_name):
        self._client = pymongo.client('127.0.0.0', 27017)
        self._db = self.client["Moses"]
        self._collection = self.db[collection_name]

    def __repr__(self):
        pass

    def add(self, record: dict):
        """Adds a record into the collection"""
        self._collection.insert_one(record)
        return

    def get(self, name: str):
        """Returns a record with the corresponding name from collection"""
        return record

    def update(self, name: str, record: dict):
        """Updates a record with the corresponding name from collection"""
        return

    def delete(self, name: str):
        """Deletes the record with the corresponding name"""
        self._collection.delete_one({'student_name': name})
        return

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
        super().__init__("Students")

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

