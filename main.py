import pymongo

class Collection:
    """
    """
    def __init__(self, collection_name):
        self._client = pymongo.client('127.0.0.0', 27017)
        self._db = self.client["Moses"]
        self._collection = self.db[collection_name]

    def __repr__(self):
        pass

    def add(self, record):
        self._collection.insert_one(record)
        return

    def get(self, name):
        return record

    def update(self, name, record):
        return

    def delete(self, name):
        self._collection.delete_one({'student_name': name})
        return

class JunctionTable(Collection):
    """
    """
    def __init__(self):
        super().__init__("JunctionTable")

class Students(Collection):
    """
    """
    def __init__(self):
        super().__init__("Students")

class Classes(Collection):
    """
    """
    def __init__(self):
        super().__init__("Classes")


class Subjects(Collection):
    """
    """
    def __init__(self):
        super().__init__("Subjects")


class Ccas(Collection):
    """
    """
    def __init__(self):
        super().__init__("CCAs")


class Activities(Collection):
    """
    """
    def __init__(self):
        super().__init__("Activies")

